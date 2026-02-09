'use client';

import { useState, useEffect } from 'react';
import { Todo } from '@/types';
import { apiClient } from '@/lib/api';
import { useAuth } from '@/hooks/useAuth'; // Import useAuth

export const useTodos = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { state: authState } = useAuth(); // Get auth state

  const fetchTodos = async () => {
    // Only fetch if authenticated and not loading auth
    if (!authState.isAuthenticated || authState.isLoading) {
      setLoading(false); // Ensure loading is false if not authenticated
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await apiClient.getTodos();

      if (result.error) {
        throw new Error(result.error);
      }

      if (Array.isArray(result.data)) {
        setTodos(result.data as Todo[]);
      } else {
        setTodos([]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch todos');
      setTodos([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTodos();
  }, [authState.isAuthenticated, authState.isLoading]); // Depend on auth state

  const refreshTodos = () => {
    fetchTodos();
  };

  const updateTodoLocally = async (id: string, todoData: Partial<Todo>) => {
    try {
      // Optimistically update the UI before API call
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === id ? { ...todo, ...todoData } : todo
        )
      );

      const result = await apiClient.updateTodo(
        id,
        todoData.title,
        todoData.description,
        todoData.completed
      );

      if (result.error) {
        throw new Error(result.error);
      }

      // If API call fails, we could rollback here, but for now just refetch
      if (!result.data) {
        fetchTodos(); // Refetch if update didn't return data
      }

      return result;
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
      fetchTodos(); // Refetch to revert optimistic update
      throw err;
    }
  };

  const toggleTodoCompletionLocally = async (id: string, completed: boolean) => {
    try {
      // Optimistically update the UI before API call
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === id ? { ...todo, completed } : todo
        )
      );

      const result = await apiClient.toggleTodo(id, completed);

      if (result.error) {
        throw new Error(result.error);
      }

      // If API call fails, we could rollback here, but for now just refetch
      if (!result.data) {
        fetchTodos(); // Refetch if update didn't return data
      }

      return result;
    } catch (err: any) {
      setError(err.message || 'Failed to toggle todo completion');
      fetchTodos(); // Refetch to revert optimistic update
      throw err;
    }
  };

  const deleteTodoLocally = async (id: string) => {
    try {
      // Optimistically remove the todo from UI before API call
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));

      const result = await apiClient.deleteTodo(id);

      if (result.error) {
        throw new Error(result.error);
      }

      return result;
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
      fetchTodos(); // Refetch to revert optimistic update
      throw err;
    }
  };

  return {
    todos,
    loading,
    error,
    refreshTodos,
    updateTodoLocally,
    toggleTodoCompletionLocally,
    deleteTodoLocally,
  };
};