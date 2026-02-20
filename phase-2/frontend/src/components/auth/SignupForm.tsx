'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

// SVG Icon for a key
const KeyIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" {...props}>
    <path fillRule="evenodd" d="M8.25 6.75a3.75 3.75 0 11.269 6.612l-2.043 2.044a.75.75 0 01-1.06 0l-1.06-1.06a.75.75 0 010-1.06l2.043-2.043A3.75 3.75 0 018.25 6.75zM15 8.25a3.75 3.75 0 10-5.834 1.66L7.16 7.16a.75.75 0 01.04-.153l.362-.836a.75.75 0 01.812-.515l1.393.284a1.5 1.5 0 001.217-.432l.362-.362a1.5 1.5 0 011.217-.432h.262a.75.75 0 01.75.75v.262a1.5 1.5 0 01-.432 1.217l-.362.362a1.5 1.5 0 00-.432 1.217l.284 1.393a.75.75 0 01-.515.812l-.836.362a.75.75 0 01-.153.04z" clipRule="evenodd" />
  </svg>
);

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
      console.error('Signup error:', error); // Debug logging

      // Extract error details
      const status = error.response?.status;
      const backendMessage = error.response?.data?.detail || error.response?.data?.message;

      console.log('Error status:', status); // Debug logging
      console.log('Backend message:', backendMessage); // Debug logging

      let errorMessage = 'An error occurred during signup';

      if (status === 409) {
        // Email already exists
        errorMessage = 'Email is already registered.';
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

      console.log('Setting error message:', errorMessage); // Debug logging
      setErrors(prev => ({ ...prev, form: errorMessage }));
      // Do NOT redirect on error
    } finally {
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
              className="flex items-center text-sm leading-5"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              <KeyIcon className="h-5 w-5 text-yellow-500" />
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
              className="flex items-center text-sm leading-5"
              aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
            >
              <KeyIcon className="h-5 w-5 text-yellow-500" />
            </button>
          }
        />
        <p className="mt-2 text-sm text-muted-foreground">
          Password must be at least 8 characters
        </p>

        {errors.form && (
          <div className="rounded-md bg-destructive/10 p-4">
            <div className="text-sm text-destructive">{errors.form}</div>
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