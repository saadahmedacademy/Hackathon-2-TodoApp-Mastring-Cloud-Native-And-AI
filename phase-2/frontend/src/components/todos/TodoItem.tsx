'use client';

import React, { useState } from 'react';
import { Todo } from '@/types';
import { apiClient } from '@/lib/api';
import Button from '@/components/ui/Button';
import { useToast } from '@/contexts/ToastContext';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (updatedTodo: Todo) => void;
  onDelete: (id: string) => void;
}

export default function TodoItem({ todo, onUpdate, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const handleToggleComplete = async () => {
    setIsLoading(true);

    try {
      const updatedTodo = await apiClient.toggleTodoCompletion(todo.id, !todo.completed);

      if (updatedTodo.error) {
        throw new Error(updatedTodo.error);
      }

      if (updatedTodo.data) {
        onUpdate(updatedTodo.data as Todo);
        addToast(`Todo "${todo.title}" marked as ${todo.completed ? 'incomplete' : 'complete'}`, 'success');
      }
    } catch (err: any) {
      addToast(err.message || 'Failed to update todo', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = async () => {
    setIsLoading(true);

    try {
      const updatedTodo = await apiClient.updateTodo(todo.id, {
        title: editText,
        description: editDescription,
      });

      if (updatedTodo.error) {
        throw new Error(updatedTodo.error);
      }

      if (updatedTodo.data) {
        onUpdate(updatedTodo.data as Todo);
        setIsEditing(false);
        addToast('Todo updated successfully', 'success');
      }
    } catch (err: any) {
      addToast(err.message || 'Failed to update todo', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${todo.title}"?`)) {
      setIsLoading(true);

      try {
        const result = await apiClient.deleteTodo(todo.id);

        if (result.error) {
          throw new Error(result.error);
        }

        if (result.data?.success) {
          onDelete(todo.id);
          addToast('Todo deleted successfully', 'success');
        }
      } catch (err: any) {
        addToast(err.message || 'Failed to delete todo', 'error');
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleCancelEdit = () => {
    setEditText(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 transition-all ${todo.completed ? 'bg-green-50' : 'bg-white'} ${isLoading ? 'opacity-70' : ''}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Todo title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Description (optional)"
            rows={2}
          />
          <div className="flex space-x-2">
            <Button
              onClick={handleEdit}
              isLoading={isLoading}
              variant="primary"
              size="sm"
            >
              Save
            </Button>
            <Button
              onClick={handleCancelEdit}
              variant="secondary"
              size="sm"
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
              disabled={isLoading}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              aria-label={todo.completed ? `Mark "${todo.title}" as incomplete` : `Mark "${todo.title}" as complete`}
            />
            <div>
              <h3 className={`text-lg font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {todo.title}
              </h3>
              {todo.description && (
                <p className={`mt-1 text-sm ${todo.completed ? 'line-through text-gray-400' : 'text-gray-500'}`}>
                  {todo.description}
                </p>
              )}
              <p className="mt-2 text-xs text-gray-400">
                Created: {new Date(todo.createdAt).toLocaleDateString()}
                {todo.updatedAt !== todo.createdAt && ` • Updated: ${new Date(todo.updatedAt).toLocaleDateString()}`}
              </p>
            </div>
          </div>
          <div className="flex space-x-2">
            <Button
              onClick={() => setIsEditing(true)}
              variant="outline"
              size="sm"
              aria-label={`Edit todo: ${todo.title}`}
            >
              Edit
            </Button>
            <Button
              onClick={handleDelete}
              variant="outline"
              size="sm"
              className="text-red-600 hover:text-red-700"
              aria-label={`Delete todo: ${todo.title}`}
            >
              Delete
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}