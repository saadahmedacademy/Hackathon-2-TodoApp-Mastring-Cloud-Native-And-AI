'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import TodoForm from '@/components/todos/TodoForm';

export default function NewTodoPage() {
  const router = useRouter();

  const handleTodoCreated = () => {
    // Optionally redirect to the todos list after creation
    router.push('/dashboard/todos');
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Create New Todo</h1>
      <TodoForm onSuccess={handleTodoCreated} />
    </div>
  );
}