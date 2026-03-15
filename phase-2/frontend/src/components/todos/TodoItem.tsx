'use client';

import React, { useState, memo } from 'react';
import { Todo } from '@/types';
import { apiClient } from '@/lib/api';
import Button from '@/components/ui/Button';
import { useToast } from '@/contexts/ToastContext';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (updatedTodo: Todo) => void;
  onDelete: (id: string) => void;
  toggleTodoCompletionLocally?: (id: string, completed: boolean) => Promise<any>;
  updateTodoLocally?: (id: string, todoData: Partial<Todo>) => Promise<any>;
  deleteTodoLocally?: (id: string) => Promise<any>;
}

const TodoItem = memo(function TodoItem({ todo, onUpdate, onDelete, toggleTodoCompletionLocally, updateTodoLocally, deleteTodoLocally }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const handleToggleComplete = async () => {
    setIsLoading(true);

    try {
      // Use the local function if available, otherwise fall back to direct API call
      let result;
      if (toggleTodoCompletionLocally) {
        result = await toggleTodoCompletionLocally(todo.id, !todo.completed);
      } else {
        result = await apiClient.toggleTodo(todo.id, !todo.completed);

        if (result.error) {
          throw new Error(result.error);
        }

        if (result.data) {
          onUpdate(result.data as Todo);
        }
      }

      addToast(`Todo "${todo.title}" marked as ${todo.completed ? 'incomplete' : 'complete'}`, 'success');
    } catch (err: any) {
      addToast(err.message || 'Failed to update todo', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = async () => {
    setIsLoading(true);

    try {
      // Use the local function if available, otherwise fall back to direct API call
      let result;
      if (updateTodoLocally) {
        result = await updateTodoLocally(todo.id, {
          title: editText,
          description: editDescription,
        });
      } else {
        result = await apiClient.updateTodo(
          todo.id,
          editText,
          editDescription
        );

        if (result.error) {
          throw new Error(result.error);
        }

        if (result.data) {
          onUpdate(result.data as Todo);
        }
      }

      setIsEditing(false);
      addToast('Todo updated successfully', 'success');
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
        // Use the local function if available, otherwise fall back to direct API call
        let result;
        if (deleteTodoLocally) {
          result = await deleteTodoLocally(todo.id);
        } else {
          result = await apiClient.deleteTodo(todo.id);

          if (result.error) {
            throw new Error(result.error);
          }

          if (result.data?.success) {
            onDelete(todo.id);
          }
        }

        addToast('Todo deleted successfully', 'success');
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
    <div className={`border-2 rounded-xl p-4 sm:p-5 transition-all duration-300 shadow-lg hover:shadow-2xl ${todo.completed ? 'bg-gradient-to-br from-green-100 to-emerald-100 border-green-400 dark:from-green-900/20 dark:to-emerald-900/20 dark:border-green-700' : 'bg-gradient-to-br from-white to-gray-50 border-gray-300 dark:from-gray-800 dark:to-gray-900 dark:border-gray-600'} ${isLoading ? 'opacity-70' : ''}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            placeholder="Todo title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full rounded-md border border-input bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 min-h-[96px] leading-relaxed"
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
        <div className="group lg:relative">
          <div className="flex items-start gap-2 sm:gap-3">
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
              disabled={isLoading}
              className="mt-1 h-5 w-5 flex-shrink-0 rounded border border-input bg-background text-primary focus:ring-offset-background focus:ring-2 focus:ring-ring"
              aria-label={todo.completed ? `Mark "${todo.title}" as incomplete` : `Mark "${todo.title}" as complete`}
            />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div
                className={`text-base sm:text-lg font-medium lg:pr-32 ${todo.completed ? 'line-through' : ''} group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors`}
                style={todo.completed ? { color: 'var(--foreground)' } : {}}
              >
                <span className="text-sm font-mono text-muted-foreground">
                  [{todo.display_id ?? '?'}]{' '}
                </span>
                <span className={!todo.completed ? 'text-gray-900 dark:text-gray-100' : ''}>
                  {todo.title}
                </span>
              </div>
              {todo.description && (
                <div
                  className={`mt-1 text-sm lg:pr-32 ${todo.completed ? 'line-through' : 'text-gray-800 dark:text-gray-300'} group-hover:text-blue-500 dark:group-hover:text-blue-300 transition-colors`}
                  style={todo.completed ? { color: 'var(--foreground)' } : {}}
                >
                  {todo.description}
                </div>
              )}
              <p className="mt-2 text-xs text-gray-600 dark:text-gray-400">
                {(() => {
                  const createdDate = todo.createdAt ? new Date(todo.createdAt) : null;
                  const updatedDate = todo.updatedAt ? new Date(todo.updatedAt) : null;

                  const isValidDate = (date: Date | null) => date && !isNaN(date.getTime());

                  const createdDateStr = isValidDate(createdDate)
                    ? createdDate!.toLocaleDateString()
                    : 'N/A';

                  let updatedDateStr = '';
                  if (isValidDate(updatedDate) && createdDate && updatedDate!.getTime() !== createdDate!.getTime()) {
                    updatedDateStr = ` • Updated: ${updatedDate!.toLocaleDateString()}`;
                  }

                  return `Created: ${createdDateStr}${updatedDateStr}`;
                })()}
              </p>
            </div>
          </div>
          <div className="flex gap-2 mt-3 lg:mt-0 lg:absolute lg:top-2 lg:right-2 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity">
            <Button
              onClick={() => setIsEditing(true)}
              variant="outline"
              size="sm"
              className="flex-1 lg:flex-none text-xs sm:text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 px-3 py-1.5"
              aria-label={`Edit todo: ${todo.title}`}
            >
              Edit
            </Button>
            <Button
              onClick={handleDelete}
              variant="outline"
              size="sm"
              className="flex-1 lg:flex-none text-xs sm:text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20 px-3 py-1.5"
              aria-label={`Delete todo: ${todo.title}`}
            >
              Delete
            </Button>
          </div>
        </div>
      )}
    </div>
  );
});

export default TodoItem;