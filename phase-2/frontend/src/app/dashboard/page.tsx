'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { useAuth } from '@/hooks/useAuth';
import { useChatContext } from '@/contexts/ChatContext';
import { apiClient } from '@/lib/api';
import { Todo } from '@/types';

const COLORS = ['#22c55e', '#f97316']; // completed = green, pending = orange

function DonutChart({ completed, pending }: { completed: number; pending: number }) {
  const total = completed + pending;
  const data = [
    { name: 'Completed', value: completed },
    { name: 'Pending', value: pending },
  ];

  if (total === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-40 text-muted-foreground text-sm">
        No tasks yet
      </div>
    );
  }

  return (
    <div className="relative flex items-center justify-center h-40">
      <ResponsiveContainer width="100%" height={160}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={48}
            outerRadius={68}
            dataKey="value"
            strokeWidth={0}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i]} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ fontSize: '12px' }} />
        </PieChart>
      </ResponsiveContainer>
      {/* Center label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span className="text-2xl font-bold text-foreground">{total}</span>
        <span className="text-xs text-muted-foreground">Total</span>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const { state } = useAuth();
  const { openChat } = useChatContext();
  const router = useRouter();

  const [todos, setTodos] = useState<Todo[]>([]);
  const [loadingTodos, setLoadingTodos] = useState(true);

  useEffect(() => {
    apiClient.getTodos().then((res) => {
      if (res.data) setTodos(res.data);
      setLoadingTodos(false);
    });
  }, []);

  const completed = todos.filter((t) => t.completed).length;
  const pending = todos.length - completed;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-foreground mb-2">Dashboard</h1>
      <p className="text-muted-foreground mb-6">
        Welcome back, {state.user?.email}!
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Card 1 — Create Todo */}
        <div className="rounded-2xl shadow-md p-6 bg-card hover:shadow-lg transition flex flex-col gap-4">
          <div>
            <h2 className="text-lg font-semibold text-foreground">Create Todo</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Add a new task to your list.
            </p>
          </div>
          <button
            onClick={() => router.push('/dashboard/new')}
            className="mt-auto rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            + New Todo
          </button>
        </div>

        {/* Card 2 — Donut Chart */}
        <div className="rounded-2xl shadow-md p-6 bg-card hover:shadow-lg transition flex flex-col gap-2">
          <h2 className="text-lg font-semibold text-foreground">Todo Stats</h2>
          {loadingTodos ? (
            <div className="flex items-center justify-center h-40 text-muted-foreground text-sm">
              Loading…
            </div>
          ) : (
            <DonutChart completed={completed} pending={pending} />
          )}
          <div className="flex justify-center gap-6 text-xs mt-1">
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-green-500" />
              Completed ({completed})
            </span>
            <span className="flex items-center gap-1">
              <span className="inline-block w-2.5 h-2.5 rounded-full bg-orange-400" />
              Pending ({pending})
            </span>
          </div>
        </div>

        {/* Card 3 — Start Chatting */}
        <div className="rounded-2xl shadow-md p-6 bg-card hover:shadow-lg transition flex flex-col gap-4">
          <div>
            <h2 className="text-lg font-semibold text-foreground">AI Assistant</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Manage your tasks using natural language. Just ask!
            </p>
          </div>
          <button
            onClick={openChat}
            className="mt-auto rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            💬 Start Chatting
          </button>
        </div>

      </div>
    </div>
  );
}
