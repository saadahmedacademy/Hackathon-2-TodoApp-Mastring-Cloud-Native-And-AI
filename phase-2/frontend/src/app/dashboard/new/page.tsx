'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import TodoForm from '@/components/todos/TodoForm';

export default function NewTodoPage() {
  const router = useRouter();

  const handleTodoCreated = () => {
    // Delay redirect to allow toast to be visible
    setTimeout(() => {
      router.push('/dashboard/todos');
    }, 1500); // 1.5 second delay
  };

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100 mb-4 sm:mb-6">Create New Todo</h1>
      <TodoForm onSuccess={handleTodoCreated} />
    </div>
  );
}