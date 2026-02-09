'use client';

import React, { useEffect } from 'react'; // Import useEffect
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { state } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Redirect only when not loading and authenticated
    if (!state.isLoading && state.isAuthenticated) {
      router.push('/dashboard');
    }
  }, [state.isAuthenticated, state.isLoading, router]); // Depend on isAuthenticated and isLoading

  // If still loading, or if authenticated and redirect is pending, show nothing
  if (state.isLoading || state.isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-xl">Loading authentication...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          TodoApp
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          {/* This conditional rendering based on children type is fragile and should be avoided.
              A better approach would be to pass a prop to the layout indicating the page type. */}
          {/* For now, keeping original logic for consistency if children is React Element with type.name */}
          {React.isValidElement(children) && typeof children.type === 'function' && (children.type as any).name === 'SignupPage'
            ? 'Create a new account'
            : 'Sign in to your account'}
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {children}
        </div>
      </div>
    </div>
  );
}