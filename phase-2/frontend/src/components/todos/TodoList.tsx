'use client';

import React from 'react';
import { Todo } from '@/types';
import TodoItem from '@/components/todos/TodoItem';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import Skeleton from '@/components/ui/Skeleton';

interface TodoListProps {
  todos: Todo[];
  loading: boolean;
  toggleTodoCompletionLocally?: (id: string, completed: boolean) => Promise<any>;
  updateTodoLocally?: (id: string, todoData: Partial<Todo>) => Promise<any>;
  deleteTodoLocally?: (id: string) => Promise<any>;
}

export default function TodoList({ todos, loading, toggleTodoCompletionLocally, updateTodoLocally, deleteTodoLocally }: TodoListProps) {
  const handleTodoUpdate = (updatedTodo: Todo) => {
    // This function can be used to update the todo in the parent component if needed
    console.log('Todo updated:', updatedTodo);
  };

  const handleTodoDelete = (id: string) => {
    // This function can be used to remove the todo from the parent component if needed
    console.log('Todo deleted:', id);
  };

  if (loading) {
    return (
      <div className="space-y-3">
        <div className="mb-6">
          <Skeleton className="h-10 w-40" />
        </div>
        {[...Array(5)].map((_, index) => (
          <div key={index} className="border rounded-lg p-4 mb-3 bg-white">
            <div className="flex items-center space-x-3">
              <Skeleton className="h-5 w-5 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-3 w-3/4" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            vectorEffect="non-scaling-stroke"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No todos</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new todo.</p>
        <div className="mt-6">
          <Link href="/dashboard/new">
            <Button variant="primary">
              Create New Todo
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <Link href="/dashboard/new">
          <Button variant="primary">
            + Add New Todo
          </Button>
        </Link>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {todos.map((todo) => (
            <li key={todo.id}>
              <TodoItem
                todo={todo}
                onUpdate={handleTodoUpdate}
                onDelete={handleTodoDelete}
                toggleTodoCompletionLocally={toggleTodoCompletionLocally}
                updateTodoLocally={updateTodoLocally}
                deleteTodoLocally={deleteTodoLocally}
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}