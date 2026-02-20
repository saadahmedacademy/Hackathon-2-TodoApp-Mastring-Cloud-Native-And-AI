from typing import List, Dict, Any, Optional
import openai
from ..config.llm import get_gemini_openai_client

SYSTEM_MESSAGE = """\
You are a task management AI assistant.
You help users create, list, update, complete, and delete their tasks.
When the user asks to perform an action, always use the available tools.
After every tool call succeeds, summarise the result concisely.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT OUTPUT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. NEVER expose internal database IDs, UUIDs, or raw primary-key numbers.
   Always reference tasks by their display_id as "#N" (e.g. Task #3).
2. Keep every response under 5 lines.
3. Use emojis to signal action type.
4. Never refuse to call a tool when the user's intent clearly maps to one.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TODO CREATION RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When user creates a todo:

Step 1 — Strip command words (case-insensitive):
  Remove: "add todo", "create todo", "add task", "create task"
  Only keep the meaningful content that follows.

Step 2 — Determine title vs description:
  Case A — User provides explicit title:
    Input:  "add title: Grocery, description: buy milk"
    →  Call add_task_tool(title="Grocery", description="buy milk")

  Case B — User provides only a sentence (no explicit title):
    Input:  "add todo buy milk"
    →  Call add_task_tool(description="buy milk")
          (title is omitted — system auto-generates "Task {display_id}")

  Case C — Separator patterns that signal explicit title:
    "add TITLE - DESCRIPTION"  →  title="TITLE", description="DESCRIPTION"
    "add TITLE: DESCRIPTION"   →  title="TITLE", description="DESCRIPTION"

Step 3 — Never store the raw command sentence as title.
Step 4 — Always pass structured arguments to the tool.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMAND PARSING RULES (delete / update / complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parse the display_id from natural language commands:

  "delete id 2 todo"     → delete_task_tool(display_id=2)
  "mark id 3 done"       → complete_task_tool(display_id=3)
  "edit id 1"            → update_task_tool(display_id=1, ...)
  "remove task #5"       → delete_task_tool(display_id=5)
  "complete number 4"    → complete_task_tool(display_id=4)

All operations use WHERE user_id = current_user AND display_id = N.
Never use the database primary key for user interactions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESPONSE FORMAT EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Add (no explicit title):  ✅ Task #4 added — buy milk
Add (explicit title):     ✅ Task #4 added: Grocery — buy milk
List:
  📋 Your Tasks:
  #1 Buy milk (Pending)
  #2 Finish report (Done)
Update:  ✏️ Task #2 updated.
Delete:  🗑️ Task #3 deleted.
Complete: ✅ Task #1 marked as done.
Error:   ❌ Task #5 not found.
"""


class AgentRateLimitError(Exception):
    """Raised when the upstream LLM API returns a 429 rate-limit response."""
    pass


class AIAgentBase:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = get_gemini_openai_client()
        self.model = model
        self.tools: List[Dict[str, Any]] = []
        self.tool_map: Dict[str, Any] = {}

    def register_tool(self, tool_function: Any, tool_schema: Dict[str, Any]):
        self.tools.append(tool_schema)
        self.tool_map[tool_function.__name__] = tool_function

    def get_response(self, messages: List[Dict[str, Any]]) -> Any:
        full_messages = [{"role": "system", "content": SYSTEM_MESSAGE}] + messages

        kwargs: Dict[str, Any] = {}
        if self.tools:
            kwargs["tools"] = self.tools
            kwargs["tool_choice"] = "auto"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                timeout=20,  # hard cap per model call — prevents 504s
                **kwargs,
            )
            return response.choices[0].message
        except openai.RateLimitError as exc:
            raise AgentRateLimitError(
                "AI rate limit exceeded. Please try again later."
            ) from exc

    def call_tool(self, tool_name: str, **kwargs) -> Any:
        tool_function = self.tool_map.get(tool_name)
        if not tool_function:
            raise ValueError(f"Tool '{tool_name}' not registered.")
        return tool_function(**kwargs)
