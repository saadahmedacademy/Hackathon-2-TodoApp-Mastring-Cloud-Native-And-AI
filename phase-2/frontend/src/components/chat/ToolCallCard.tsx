'use client';

interface RawToolCall {
  id: string;
  type: string;
  function: { name: string; arguments: string };
}

interface ToolCallCardProps {
  toolCall: RawToolCall;
}

export default function ToolCallCard({ toolCall }: ToolCallCardProps) {
  let parsedArgs: Record<string, unknown> = {};
  try {
    parsedArgs = JSON.parse(toolCall.function.arguments);
  } catch {
    // keep empty
  }

  return (
    <details className="text-xs rounded-lg border border-border bg-muted/50 overflow-hidden">
      <summary className="cursor-pointer select-none px-3 py-2 font-medium text-foreground">
        ⚙ {toolCall.function.name}
      </summary>
      <div className="px-3 py-2 space-y-1 border-t border-border">
        <p>
          <span className="font-medium text-foreground">Arguments: </span>
          <span className="text-muted-foreground font-mono">
            {JSON.stringify(parsedArgs, null, 2)}
          </span>
        </p>
      </div>
    </details>
  );
}
