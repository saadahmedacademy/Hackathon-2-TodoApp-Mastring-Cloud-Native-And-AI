'use client';

import React from 'react';
import { useTodos } from '@/hooks/useTodos';
import TodoList from '@/components/todos/TodoList';

export default function TodosPage() {
  const { todos, loading, error, refreshTodos, toggleTodoCompletionLocally, updateTodoLocally, deleteTodoLocally } = useTodos();

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">My Todos</h1>
        <button
          onClick={refreshTodos}
          className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Refresh
        </button>
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-6">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <TodoList
        todos={todos}
        loading={loading}
        toggleTodoCompletionLocally={toggleTodoCompletionLocally}
        updateTodoLocally={updateTodoLocally}
        deleteTodoLocally={deleteTodoLocally}
      />
    </div>
  );
}