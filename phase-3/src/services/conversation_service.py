from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select
from src.models.conversation import Conversation
from src.models.message import Message
from src.repositories.conversation import ConversationRepository
from src.repositories.message import MessageRepository
from src.agents.base import AIAgentBase
from src.mcp.tools.add_task import add_task_tool
from src.mcp.tools.list_tasks import list_tasks_tool
from src.mcp.tools.complete_task import complete_task_tool
from src.mcp.tools.delete_task import delete_task_tool
from src.mcp.tools.update_task import update_task_tool
import json

# Duplicate-suppression window: ignore a re-submitted identical message within this window
_DEDUP_WINDOW = timedelta(seconds=5)


def _tool_call_to_dict(tc) -> Dict[str, Any]:
    """Convert an OpenAI ChatCompletionMessageToolCall object to a plain dict."""
    return {
        "id": tc.id,
        "type": tc.type,
        "function": {
            "name": tc.function.name,
            "arguments": tc.function.arguments,
        },
    }


def _message_to_api_dict(msg: Message) -> Dict[str, Any]:
    """Serialise a persisted Message row into the API wire format."""
    out: Dict[str, Any] = {"role": msg.sender, "content": msg.content or ""}
    if msg.sender == "assistant":
        if msg.tool_calls:
            try:
                out["tool_calls"] = json.loads(msg.tool_calls)
            except (TypeError, json.JSONDecodeError):
                out["tool_calls"] = None
        else:
            out["tool_calls"] = None
    if msg.sender == "tool" and msg.tool_outputs:
        try:
            out["tool_outputs"] = json.loads(msg.tool_outputs)
        except (TypeError, json.JSONDecodeError):
            pass
    return out


class ConversationService:
    def __init__(self, session: Session, ai_agent: AIAgentBase):
        self.session = session
        self.conversation_repo = ConversationRepository(session)
        self.message_repo = MessageRepository(session)
        self.ai_agent = ai_agent

        # Tool dispatch: maps tool name → callable(user_id, **kwargs)
        # session is captured via closure; user_id is threaded per request
        self._tool_dispatch = {
            "add_task_tool":      lambda user_id, **kw: add_task_tool(session, user_id, **kw),
            "list_tasks_tool":    lambda user_id, **kw: list_tasks_tool(session, user_id, **kw),
            "complete_task_tool": lambda user_id, **kw: complete_task_tool(session, user_id, **kw),
            "delete_task_tool":   lambda user_id, **kw: delete_task_tool(session, user_id, **kw),
            "update_task_tool":   lambda user_id, **kw: update_task_tool(session, user_id, **kw),
        }

    # ------------------------------------------------------------------ #
    #  Basic CRUD helpers                                                   #
    # ------------------------------------------------------------------ #

    def create_conversation(self, user_id: UUID) -> Conversation:
        conversation = Conversation(user_id=user_id)
        return self.conversation_repo.create(conversation)

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        return self.conversation_repo.get(conversation_id)

    def add_message_to_conversation(
        self,
        conversation_id: UUID,
        sender: str,
        content: str,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        tool_outputs: Optional[Dict[str, Any]] = None,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content,
            tool_calls=json.dumps(tool_calls) if tool_calls else None,
            tool_outputs=json.dumps(tool_outputs) if tool_outputs else None,
        )
        return self.message_repo.create(message)

    def get_conversation_history(self, conversation_id: UUID) -> List[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        return self.session.exec(statement).all()

    # ------------------------------------------------------------------ #
    #  Duplicate detection                                                 #
    # ------------------------------------------------------------------ #

    def _is_duplicate_message(
        self, conversation_id: UUID, sender: str, content: str
    ) -> bool:
        """Return True if the last message in this conversation is identical and recent."""
        history = self.get_conversation_history(conversation_id)
        if not history:
            return False
        last = history[-1]
        if last.sender != sender or last.content != content:
            return False
        cutoff = datetime.now(timezone.utc) - _DEDUP_WINDOW
        last_ts = last.created_at
        if last_ts.tzinfo is None:
            last_ts = last_ts.replace(tzinfo=timezone.utc)
        return last_ts >= cutoff

    # ------------------------------------------------------------------ #
    #  History → ai_messages reconstruction                                #
    # ------------------------------------------------------------------ #

    def _build_ai_messages(self, history: List[Message]) -> List[Dict[str, Any]]:
        """
        Convert persisted message rows into the list of dicts expected by the
        OpenAI chat completions API, including tool messages.
        """
        ai_messages: List[Dict[str, Any]] = []
        for msg in history:
            if msg.sender == "user":
                ai_messages.append({"role": "user", "content": msg.content or ""})

            elif msg.sender == "assistant":
                entry: Dict[str, Any] = {
                    "role": "assistant",
                    "content": msg.content or "",
                }
                if msg.tool_calls:
                    try:
                        entry["tool_calls"] = json.loads(msg.tool_calls)
                    except (TypeError, json.JSONDecodeError):
                        pass
                ai_messages.append(entry)

            elif msg.sender == "tool":
                # Reconstruct tool result message from stored tool_outputs
                tool_outputs = {}
                if msg.tool_outputs:
                    try:
                        tool_outputs = json.loads(msg.tool_outputs)
                    except (TypeError, json.JSONDecodeError):
                        pass
                tool_call_id = tool_outputs.get("tool_call_id", "")
                tool_name = tool_outputs.get("name", "")
                tool_output = tool_outputs.get("output", {})
                ai_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": json.dumps(tool_output),
                })

        return ai_messages

    # ------------------------------------------------------------------ #
    #  Main orchestration method                                           #
    # ------------------------------------------------------------------ #

    def send_message_to_agent(
        self, user_id: UUID, conversation_id: Optional[UUID], user_message_content: str
    ) -> Dict[str, Any]:
        # 1. Resolve or create conversation
        if conversation_id:
            conversation = self.get_conversation(conversation_id)
            if not conversation:
                raise ValueError(f"Conversation with ID {conversation_id} not found.")
        else:
            conversation = self.create_conversation(user_id)

        # 2. Persist user message (with duplicate guard)
        if not self._is_duplicate_message(conversation.id, "user", user_message_content):
            self.add_message_to_conversation(conversation.id, "user", user_message_content)
            self.session.commit()

        # 3. Rebuild full message history for the AI
        history = self.get_conversation_history(conversation.id)
        ai_messages = self._build_ai_messages(history)

        # 4. Tool execution loop (OpenAI function-calling pattern)
        #    Keep calling the model until it stops requesting tools.
        MAX_TOOL_ROUNDS = 5  # hard cap — prevents infinite loops and 504 timeouts
        for iteration in range(MAX_TOOL_ROUNDS):
            agent_response = self.ai_agent.get_response(ai_messages)
            raw_tool_calls = agent_response.tool_calls  # list | None
            response_content = agent_response.content or ""

            # Serialise tool calls to plain dicts for storage
            tool_calls_dicts: Optional[List[Dict[str, Any]]] = None
            if raw_tool_calls:
                tool_calls_dicts = [_tool_call_to_dict(tc) for tc in raw_tool_calls]

            # Persist assistant message (may or may not have tool_calls)
            self.add_message_to_conversation(
                conversation.id, "assistant", response_content,
                tool_calls=tool_calls_dicts,
            )
            self.session.commit()

            # Append assistant turn to in-memory history for next iteration
            assistant_entry: Dict[str, Any] = {
                "role": "assistant",
                "content": response_content,
            }
            if tool_calls_dicts:
                assistant_entry["tool_calls"] = tool_calls_dicts
            ai_messages.append(assistant_entry)

            # If no tool calls requested, we're done
            if not raw_tool_calls:
                break

            # 5. Execute each requested tool and feed results back
            for tc in raw_tool_calls:
                fn_name = tc.function.name
                try:
                    fn_args = json.loads(tc.function.arguments)
                except (TypeError, json.JSONDecodeError):
                    fn_args = {}

                # Strip server-injected params the model should never pass
                fn_args.pop("user_id", None)
                fn_args.pop("session", None)

                dispatch = self._tool_dispatch.get(fn_name)
                if dispatch:
                    tool_output = dispatch(user_id, **fn_args)
                else:
                    tool_output = {"status": "error", "message": f"Unknown tool: {fn_name}"}

                # Persist tool result message
                self.add_message_to_conversation(
                    conversation.id, "tool", json.dumps(tool_output),
                    tool_outputs={
                        "tool_call_id": tc.id,
                        "name": fn_name,
                        "output": tool_output,
                    },
                )

                # Append tool result to in-memory history for next model call
                ai_messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": fn_name,
                    "content": json.dumps(tool_output),
                })

            self.session.commit()
        else:
            # Loop exhausted all rounds without a clean (tool-free) response.
            # Persist an error assistant message so the frontend gets something useful.
            error_content = (
                "❌ I reached the maximum number of tool-call steps. "
                "Please try a simpler request."
            )
            self.add_message_to_conversation(
                conversation.id, "assistant", error_content
            )
            self.session.commit()
            raise RuntimeError(
                "Tool execution limit reached after "
                f"{MAX_TOOL_ROUNDS} rounds. Request aborted."
            )

        # 6. Return FULL conversation history to the frontend
        full_history = self.get_conversation_history(conversation.id)
        messages_out = [_message_to_api_dict(m) for m in full_history]

        return {
            "conversation_id": str(conversation.id),
            "messages": messages_out,
        }
