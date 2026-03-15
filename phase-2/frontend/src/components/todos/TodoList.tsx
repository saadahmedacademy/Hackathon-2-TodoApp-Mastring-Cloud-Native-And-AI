'use client';

import React, { useCallback, memo } from 'react';
import { Todo } from '@/types';
import TodoItem from '@/components/todos/TodoItem';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import Skeleton from '@/components/ui/Skeleton';
import { Plus, FileText, Sparkles, SearchX } from 'lucide-react';

interface TodoListProps {
  todos: Todo[];
  loading: boolean;
  searchQuery?: string;
  toggleTodoCompletionLocally?: (id: string, completed: boolean) => Promise<any>;
  updateTodoLocally?: (id: string, todoData: Partial<Todo>) => Promise<any>;
  deleteTodoLocally?: (id: string) => Promise<any>;
}

const TodoList = memo(function TodoList({ todos, loading, searchQuery, toggleTodoCompletionLocally, updateTodoLocally, deleteTodoLocally }: TodoListProps) {
  const handleTodoUpdate = useCallback((updatedTodo: Todo) => {
    // This function can be used to update the todo in the parent component if needed
    console.log('Todo updated:', updatedTodo);
  }, []);

  const handleTodoDelete = useCallback((id: string) => {
    // This function can be used to remove the todo from the parent component if needed
    console.log('Todo deleted:', id);
  }, []);

  if (loading) {
    return (
      <div className="space-y-3">
        <div className="mb-6">
          <Skeleton className="h-12 w-48 rounded-lg" />
        </div>
        {[...Array(5)].map((_, index) => (
          <div key={index} className="border-2 rounded-xl p-4 mb-3 bg-white dark:bg-gray-800 shadow-md animate-pulse">
            <div className="flex items-center space-x-3">
              <Skeleton className="h-5 w-5 rounded" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-5 w-full" />
                <Skeleton className="h-4 w-3/4" />
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (todos.length === 0) {
    // Show different message if it's a search with no results
    if (searchQuery) {
      return (
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border-2 border-dashed border-gray-300 dark:border-gray-700 p-12 text-center shadow-inner">
          <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-orange-500/10 blur-2xl"></div>
          <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 rounded-full bg-red-500/10 blur-2xl"></div>

          <div className="relative">
            <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center mb-4 shadow-lg">
              <SearchX className="h-8 w-8 text-white" />
            </div>

            <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">No results found</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 max-w-sm mx-auto">
              We couldn't find any todos matching "<span className="font-semibold text-gray-800 dark:text-gray-300">{searchQuery}</span>"
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500">
              Try searching with different keywords or clear the search to see all todos.
            </p>
          </div>
        </div>
      );
    }

    // Original empty state when there are truly no todos
    return (
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900 border-2 border-dashed border-gray-300 dark:border-gray-700 p-12 text-center shadow-inner">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 h-24 w-24 rounded-full bg-blue-500/10 blur-2xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-24 w-24 rounded-full bg-purple-500/10 blur-2xl"></div>

        <div className="relative">
          <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mb-4 shadow-lg">
            <FileText className="h-8 w-8 text-white" />
          </div>

          <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">No todos yet</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-6 max-w-sm mx-auto">
            Start organizing your tasks and boost your productivity by creating your first todo!
          </p>

          <Link href="/dashboard/new">
            <Button
              variant="primary"
              className="inline-flex items-center gap-2 px-6 py-3 text-base font-semibold shadow-lg hover:shadow-xl transition-all duration-200 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
            >
              <Plus className="h-5 w-5" />
              Create Your First Todo
              <Sparkles className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex justify-between items-center">
        <Link href="/dashboard/new" className="flex-1 sm:flex-none">
          <Button
            variant="primary"
            className="w-full sm:w-auto inline-flex items-center gap-2 px-6 py-3 text-sm font-semibold shadow-lg hover:shadow-xl transition-all duration-200 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-lg"
          >
            <Plus className="h-5 w-5" />
            Add New Todo
          </Button>
        </Link>
      </div>

      <div className="space-y-3">
        {todos.map((todo, index) => (
          <div
            key={todo.id}
            className="transform transition-all duration-200 hover:scale-[1.01]"
            style={{ animationDelay: `${index * 50}ms` }}
          >
            <TodoItem
              todo={todo}
              onUpdate={handleTodoUpdate}
              onDelete={handleTodoDelete}
              toggleTodoCompletionLocally={toggleTodoCompletionLocally}
              updateTodoLocally={updateTodoLocally}
              deleteTodoLocally={deleteTodoLocally}
            />
          </div>
        ))}
      </div>
    </div>
  );
});

export default TodoList;