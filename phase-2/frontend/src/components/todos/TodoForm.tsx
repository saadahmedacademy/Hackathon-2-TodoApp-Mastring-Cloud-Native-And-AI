'use client';

import React, { useState } from 'react';
import { apiClient } from '@/lib/api';
import { Todo } from '@/types';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface TodoFormProps {
  onSuccess?: () => void;
  onCancel?: () => void;
  initialTodo?: Partial<Todo>;
  isEditing?: boolean;
}

export default function TodoForm({ onSuccess, onCancel, initialTodo, isEditing = false }: TodoFormProps) {
  const [formData, setFormData] = useState({
    title: initialTodo?.title || '',
    description: initialTodo?.description || '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.trim().length < 3) {
      newErrors.title = 'Title must be at least 3 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      let result;
      if (isEditing && initialTodo?.id) {
        // Update existing todo
        result = await apiClient.updateTodo(
          initialTodo.id,
          formData.title,
          formData.description
        );
      } else {
        // Create new todo
        result = await apiClient.createTodo(
          formData.title,
          formData.description
        );
      }

      if (result.error) {
        throw new Error(result.error);
      }

      if (result.data) {
        if (onSuccess) {
          onSuccess();
        }
        // Reset form after successful submission
        if (!isEditing) {
          setFormData({ title: '', description: '' });
        }
      }
    } catch (error: any) {
      setErrors({ form: error.message || 'An error occurred while saving the todo' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Input
            label="Title"
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
            error={errors.title}
            placeholder="What needs to be done?"
            fullWidth
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-foreground mb-1">
            Description (optional)
          </label>
          <textarea
            id="description"
            name="description"
            rows={4}
            value={formData.description}
            onChange={handleChange}
                      className={`mt-1 block w-full rounded-md border border-input bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 min-h-[96px] leading-relaxed ${
                        errors.description ? 'border-destructive text-destructive' : ''
                      }`}            placeholder="Add details..."
          />
          {errors.description && <p className="mt-2 text-sm text-red-500">{errors.description}</p>}
        </div>

        {errors.form && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{errors.form}</div>
          </div>
        )}

        <div className="flex space-x-3">
          <Button
            type="submit"
            isLoading={isLoading}
            variant="primary"
            className="flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {isEditing ? 'Update Todo' : 'Create Todo'}
          </Button>

          {onCancel && (
            <Button
              type="button"
              variant="secondary"
              onClick={onCancel}
              className="flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancel
            </Button>
          )}
        </div>
      </form>
    </div>
  );
}