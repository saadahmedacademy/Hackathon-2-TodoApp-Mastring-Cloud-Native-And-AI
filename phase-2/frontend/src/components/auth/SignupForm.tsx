'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface SignupFormProps {
  onSignupSuccess?: () => void;
}

export default function SignupForm({ onSignupSuccess }: SignupFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // State for password visibility
  const [showConfirmPassword, setShowConfirmPassword] = useState(false); // State for confirm password visibility

  const { signup } = useAuth();
  const router = useRouter();

  // Debug: Log when errors change (can be removed in production)
  useEffect(() => {
    if (errors.form || errors.email) {
      console.log('📊 Errors state changed:', errors);
    }
  }, [errors]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
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

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Clear any previous form error
    const { form, ...fieldErrors } = errors;
    if (form) {
      setErrors(fieldErrors);
    }

    setIsLoading(true);

    try {
      await signup({
        email: formData.email,
        password: formData.password,
      });

      // Only redirect on successful signup
      if (onSignupSuccess) {
        onSignupSuccess();
      } else {
        router.push('/signin'); // Redirect to signin page after successful registration
      }
    } catch (error: any) {
      // Extract error details
      const status = error.response?.status;
      const backendMessage = error.response?.data?.detail || error.response?.data?.message;

      let errorMessage = 'An error occurred during signup';

      if (status === 409) {
        // Email already exists - use backend message or fallback
        errorMessage = backendMessage || 'This email is already in use. Please use a different email or sign in.';

        // Set both errors and loading state together
        setErrors({
          form: errorMessage,
          email: 'This email is already registered'
        });
        setIsLoading(false);
        return;
      } else if (status === 400) {
        // Bad request - use backend validation message if available
        errorMessage = backendMessage || 'Invalid input. Please check your data.';
      } else if (status === 500 || status >= 500) {
        // Server error
        errorMessage = 'Something went wrong. Please try again.';
      } else if (backendMessage) {
        // Use backend message if available
        errorMessage = backendMessage;
      } else if (error.message) {
        // Fallback to error message
        errorMessage = error.message;
      }

      setErrors(prev => ({ ...prev, form: errorMessage }));
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Input
            label="Email address"
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            fullWidth
          />
        </div>

        <Input
          label="Password"
          id="password"
          name="password"
          type={showPassword ? 'text' : 'password'} // Dynamic type
          autoComplete="new-password"
          value={formData.password}
          onChange={handleChange}
          error={errors.password}
          fullWidth
          rightAdornment={ // Pass toggle button as rightAdornment
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="flex items-center text-sm leading-5 text-gray-500 hover:text-gray-700 transition-colors"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
              title={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5" />
              ) : (
                <Eye className="h-5 w-5" />
              )}
            </button>
          }
        />

        <Input
          label="Confirm Password"
          id="confirmPassword"
          name="confirmPassword"
          type={showConfirmPassword ? 'text' : 'password'} // Dynamic type
          autoComplete="new-password"
          value={formData.confirmPassword}
          onChange={handleChange}
          error={errors.confirmPassword}
          fullWidth
          rightAdornment={ // Pass toggle button as rightAdornment
            <button
              type="button"
              onClick={() => setShowConfirmPassword(!showConfirmPassword)}
              className="flex items-center text-sm leading-5 text-gray-500 hover:text-gray-700 transition-colors"
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
              title={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              {showConfirmPassword ? (
                <EyeOff className="h-5 w-5" />
              ) : (
                <Eye className="h-5 w-5" />
              )}
            </button>
          }
        />
        <p className="mt-2 text-sm text-muted-foreground">
          Password must be at least 8 characters
        </p>

        {errors.form && (
          <div
            className="rounded-md bg-destructive/10 border border-destructive/20 p-4 mb-4"
            style={{
              backgroundColor: '#fee2e2',
              borderColor: '#fca5a5',
              borderWidth: '1px'
            }}
            role="alert"
            aria-live="assertive"
          >
            <div className="flex items-start gap-3">
              <svg
                className="h-5 w-5 flex-shrink-0 mt-0.5"
                style={{ color: '#dc2626' }}
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                  clipRule="evenodd"
                />
              </svg>
              <div
                className="text-sm font-medium"
                style={{ color: '#dc2626' }}
              >
                {errors.form}
              </div>
            </div>
          </div>
        )}

        <div>
          <Button
            type="submit"
            fullWidth
            isLoading={isLoading}
            className="flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          >
            Sign up
          </Button>
        </div>
      </form>

      <div className="mt-4 text-center">
        <p className="text-sm text-muted-foreground">
          Already have an account?{' '}
          <Link href="/signin" className="font-medium text-primary hover:text-primary/90">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}