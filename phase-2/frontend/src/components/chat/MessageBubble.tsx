'use client';

import { useState } from 'react';
import { ChatMessage } from '@/types/chat';

interface MessageBubbleProps {
  message: ChatMessage;
}

function ToolCallBadge({ name }: { name: string }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
      ⚙ {name}
    </span>
  );
}

function ToolResultBubble({ message }: { message: ChatMessage }) {
  const [expanded, setExpanded] = useState(false);
  const toolName = message.toolOutputs?.name ?? 'tool';
  let output = message.content;
  try {
    const parsed = JSON.parse(message.content);
    output = parsed.message ?? parsed.status ?? JSON.stringify(parsed, null, 2);
  } catch {
    // keep raw content
  }

  return (
    <div className="flex justify-start mb-1">
      <div className="max-w-[80%] rounded-2xl px-3 py-2 text-xs bg-muted/60 border border-border text-muted-foreground">
        <button
          onClick={() => setExpanded((v) => !v)}
          className="flex items-center gap-1 font-medium hover:text-foreground transition-colors"
        >
          <span>{expanded ? '▾' : '▸'}</span>
          <span>⚙ {toolName}</span>
        </button>
        {expanded && (
          <p className="mt-1 whitespace-pre-wrap break-words font-mono">{output}</p>
        )}
      </div>
    </div>
  );
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  // Render tool result messages inline (collapsible)
  if (message.role === 'tool') {
    return <ToolResultBubble message={message} />;
  }

  const isUser = message.role === 'user';

  const bubbleClass = isUser
    ? 'bg-primary text-primary-foreground ml-auto'
    : message.isError
    ? 'bg-destructive/10 text-destructive border border-destructive/30'
    : 'bg-muted text-foreground';

  const timestamp = new Date(message.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });

  // Extract tool call names from assistant messages
  const toolNames =
    message.role === 'assistant' && message.toolCalls
      ? message.toolCalls.map((tc) => tc.function.name)
      : [];

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-1`}>
      <div className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${bubbleClass}`}>
        {toolNames.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-1.5">
            {toolNames.map((name) => (
              <ToolCallBadge key={name} name={name} />
            ))}
          </div>
        )}
        {message.content && (
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
        )}
        <p className={`text-xs mt-1 ${isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'}`}>
          {timestamp}
        </p>
      </div>
    </div>
  );
}
