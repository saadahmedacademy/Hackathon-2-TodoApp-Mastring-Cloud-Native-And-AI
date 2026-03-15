'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { PlusCircle, MessageSquare, CheckCircle2, Clock, ListTodo, Sparkles } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useChatContext } from '@/contexts/ChatContext';
import { apiClient } from '@/lib/api';
import { Todo } from '@/types';

const COLORS = ['#10b981', '#f59e0b']; // completed = green, pending = amber

function DonutChart({ completed, pending }: { completed: number; pending: number }) {
  const total = completed + pending;
  const data = [
    { name: 'Completed', value: completed },
    { name: 'Pending', value: pending },
  ];

  if (total === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-44 text-muted-foreground text-sm">
        <ListTodo className="h-12 w-12 mb-2 opacity-30" />
        <span>No tasks yet</span>
      </div>
    );
  }

  return (
    <div className="relative flex items-center justify-center h-44">
      <ResponsiveContainer width="100%" height={180}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={52}
            outerRadius={72}
            dataKey="value"
            strokeWidth={0}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i]} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              fontSize: '12px',
              borderRadius: '8px',
              border: 'none',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
            }}
          />
        </PieChart>
      </ResponsiveContainer>
      {/* Center label */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
        <span className="text-3xl font-bold bg-gradient-to-br from-blue-600 to-purple-600 bg-clip-text text-transparent">
          {total}
        </span>
        <span className="text-xs text-muted-foreground font-medium mt-1">Total Tasks</span>
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
  const completionRate = todos.length > 0 ? Math.round((completed / todos.length) * 100) : 0;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          Dashboard
        </h1>
        <p className="text-muted-foreground text-lg">
          Welcome back, <span className="font-semibold text-foreground">{state.user?.email?.split('@')[0]}</span>! 👋
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Tasks */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 p-6 text-white shadow-lg hover:shadow-xl transition-all hover:scale-105">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10" />
          <div className="relative">
            <ListTodo className="h-8 w-8 mb-3 opacity-90" />
            <div className="text-3xl font-bold">{todos.length}</div>
            <div className="text-sm text-blue-100 mt-1">Total Tasks</div>
          </div>
        </div>

        {/* Completed */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-green-500 to-emerald-600 p-6 text-white shadow-lg hover:shadow-xl transition-all hover:scale-105">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10" />
          <div className="relative">
            <CheckCircle2 className="h-8 w-8 mb-3 opacity-90" />
            <div className="text-3xl font-bold">{completed}</div>
            <div className="text-sm text-green-100 mt-1">Completed</div>
          </div>
        </div>

        {/* Pending */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-amber-500 to-orange-600 p-6 text-white shadow-lg hover:shadow-xl transition-all hover:scale-105">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10" />
          <div className="relative">
            <Clock className="h-8 w-8 mb-3 opacity-90" />
            <div className="text-3xl font-bold">{pending}</div>
            <div className="text-sm text-amber-100 mt-1">Pending</div>
          </div>
        </div>

        {/* Completion Rate */}
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 p-6 text-white shadow-lg hover:shadow-xl transition-all hover:scale-105">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-white/10" />
          <div className="relative">
            <Sparkles className="h-8 w-8 mb-3 opacity-90" />
            <div className="text-3xl font-bold">{completionRate}%</div>
            <div className="text-sm text-purple-100 mt-1">Completion</div>
          </div>
        </div>
      </div>

      {/* Action Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Card 1 — Create Todo */}
        <div className="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-2xl transition-all hover:scale-105 hover:border-blue-400 dark:hover:border-blue-500">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 h-32 w-32 rounded-full bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-2xl group-hover:scale-150 transition-transform" />
          <div className="relative p-6 flex flex-col gap-4 h-full">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-lg">
                <PlusCircle className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">Create Todo</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Add a new task
                </p>
              </div>
            </div>
            <button
              onClick={() => router.push('/dashboard/new')}
              className="mt-auto w-full rounded-xl bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-3 text-sm font-semibold text-white hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            >
              + New Todo
            </button>
          </div>
        </div>

        {/* Card 2 — Donut Chart */}
        <div className="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-2xl transition-all hover:scale-105 hover:border-purple-400 dark:hover:border-purple-500">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 h-32 w-32 rounded-full bg-gradient-to-br from-purple-400/20 to-pink-400/20 blur-2xl group-hover:scale-150 transition-transform" />
          <div className="relative p-6 flex flex-col gap-2">
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-purple-500" />
              Task Statistics
            </h2>
            {loadingTodos ? (
              <div className="flex items-center justify-center h-44 text-muted-foreground text-sm">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500" />
              </div>
            ) : (
              <DonutChart completed={completed} pending={pending} />
            )}
            <div className="flex justify-center gap-6 text-xs mt-2 font-medium text-gray-700 dark:text-gray-300">
              <span className="flex items-center gap-2">
                <span className="inline-block w-3 h-3 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 shadow" />
                Completed ({completed})
              </span>
              <span className="flex items-center gap-2">
                <span className="inline-block w-3 h-3 rounded-full bg-gradient-to-br from-amber-400 to-orange-500 shadow" />
                Pending ({pending})
              </span>
            </div>
          </div>
        </div>

        {/* Card 3 — AI Assistant */}
        <div className="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 shadow-lg hover:shadow-2xl transition-all hover:scale-105 hover:border-pink-400 dark:hover:border-pink-500">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 h-32 w-32 rounded-full bg-gradient-to-br from-pink-400/20 to-purple-400/20 blur-2xl group-hover:scale-150 transition-transform" />
          <div className="relative p-6 flex flex-col gap-4 h-full">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-gradient-to-br from-pink-500 to-purple-600 text-white shadow-lg">
                <MessageSquare className="h-6 w-6" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">AI Assistant</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Chat with AI
                </p>
              </div>
            </div>
            <button
              onClick={openChat}
              className="mt-auto w-full rounded-xl bg-gradient-to-r from-pink-500 to-purple-600 px-4 py-3 text-sm font-semibold text-white hover:from-pink-600 hover:to-purple-700 transition-all shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            >
              💬 Start Chatting
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
