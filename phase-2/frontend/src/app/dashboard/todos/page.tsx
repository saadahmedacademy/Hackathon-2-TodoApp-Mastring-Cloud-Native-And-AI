'use client';

import React, { useState, useMemo, useCallback } from 'react';
import { useTodos } from '@/hooks/useTodos';
import { useDebounce } from '@/hooks/useDebounce';
import TodoList from '@/components/todos/TodoList';
import { RefreshCw, ListTodo, CheckCircle2, Clock, Search, X } from 'lucide-react';

type FilterType = 'all' | 'pending' | 'completed';

export default function TodosPage() {
  const { todos, loading, error, refreshTodos, toggleTodoCompletionLocally, updateTodoLocally, deleteTodoLocally } = useTodos();
  const [filter, setFilter] = useState<FilterType>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Debounce search query to avoid filtering on every keystroke
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  const filteredTodos = useMemo(() => {
    let result = todos;

    // Apply status filter
    if (filter === 'pending') result = result.filter(todo => !todo.completed);
    if (filter === 'completed') result = result.filter(todo => todo.completed);

    // Apply search filter (use debounced value)
    if (debouncedSearchQuery.trim()) {
      const query = debouncedSearchQuery.toLowerCase();
      result = result.filter(todo =>
        todo.title.toLowerCase().includes(query) ||
        (todo.description && todo.description.toLowerCase().includes(query))
      );
    }

    return result;
  }, [todos, filter, debouncedSearchQuery]);

  const stats = useMemo(() => ({
    total: todos.length,
    pending: todos.filter(todo => !todo.completed).length,
    completed: todos.filter(todo => todo.completed).length,
  }), [todos]);

  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true);
    await refreshTodos();
    setTimeout(() => setIsRefreshing(false), 500);
  }, [refreshTodos]);

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6">
      {/* Header Section with Gradient */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-6 sm:p-8 mb-6 shadow-xl">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 h-32 w-32 rounded-full bg-white/10 blur-2xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 h-32 w-32 rounded-full bg-white/10 blur-2xl"></div>

        <div className="relative flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <ListTodo className="h-8 w-8 text-white" />
              <h1 className="text-2xl sm:text-3xl font-bold" style={{color:"white"}}>My Todos</h1>
            </div>
            <p className="text-blue-100 text-sm">Manage and track your tasks efficiently</p>
          </div>

          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-white/20 backdrop-blur-sm border border-white/30 text-sm font-medium rounded-lg text-white hover:bg-white/30 transition-all duration-200 disabled:opacity-50 w-full sm:w-auto"
          >
            <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
        </div>

        {/* Stats Badges */}
        <div className="mt-6 grid grid-cols-3 gap-3 sm:gap-4">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
            <div className="flex items-center gap-2 mb-1">
              <ListTodo className="h-4 w-4 text-white" />
              <span className="text-xs text-blue-100">Total</span>
            </div>
            <div className="text-2xl font-bold text-white">{stats.total}</div>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
            <div className="flex items-center gap-2 mb-1">
              <Clock className="h-4 w-4 text-yellow-300" />
              <span className="text-xs text-blue-100">Pending</span>
            </div>
            <div className="text-2xl font-bold text-white">{stats.pending}</div>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-white/20">
            <div className="flex items-center gap-2 mb-1">
              <CheckCircle2 className="h-4 w-4 text-green-300" />
              <span className="text-xs text-blue-100">Done</span>
            </div>
            <div className="text-2xl font-bold text-white">{stats.completed}</div>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2 sm:gap-3 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">
          <button
            onClick={() => setFilter('all')}
            className={`flex-1 sm:flex-none px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
              filter === 'all'
                ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-md'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            All ({stats.total})
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`flex-1 sm:flex-none px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
              filter === 'pending'
                ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-md'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            Pending ({stats.pending})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`flex-1 sm:flex-none px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
              filter === 'completed'
                ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-md'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            Completed ({stats.completed})
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 sm:pl-4 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400 dark:text-gray-500" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search todos by title or description..."
            className="block w-full pl-10 sm:pl-12 pr-10 sm:pr-12 py-3 sm:py-3.5 text-sm sm:text-base border-2 border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 shadow-sm hover:shadow-md"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute inset-y-0 right-0 pr-3 sm:pr-4 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
              aria-label="Clear search"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
        {searchQuery && (
          <p className="mt-2 text-xs sm:text-sm text-gray-600 dark:text-gray-400">
            Found {filteredTodos.length} result{filteredTodos.length !== 1 ? 's' : ''} for "{searchQuery}"
          </p>
        )}
      </div>

      {error && (
        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 mb-6 shadow-sm">
          <div className="text-sm text-red-700 dark:text-red-400">{error}</div>
        </div>
      )}

      <TodoList
        todos={filteredTodos}
        loading={loading}
        searchQuery={searchQuery}
        toggleTodoCompletionLocally={toggleTodoCompletionLocally}
        updateTodoLocally={updateTodoLocally}
        deleteTodoLocally={deleteTodoLocally}
      />
    </div>
  );
}