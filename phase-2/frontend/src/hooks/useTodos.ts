'use client';

import { useState, useEffect } from 'react';
import { Todo } from '@/types';
import { apiClient } from '@/lib/api';

export const useTodos = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTodos = async () => {
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
        // If the API returns a single todo object instead of an array
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
  }, []);

  const refreshTodos = () => {
    fetchTodos();
  };

  return {
    todos,
    loading,
    error,
    refreshTodos,
  };
};