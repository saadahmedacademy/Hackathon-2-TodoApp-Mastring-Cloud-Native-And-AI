'use client';

export default function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-2">
      <span className="text-xs text-muted-foreground mr-1">AI is thinking</span>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="inline-block w-1.5 h-1.5 rounded-full bg-muted-foreground animate-bounce"
          style={{ animationDelay: `${i * 150}ms` }}
        />
      ))}
    </div>
  );
}
