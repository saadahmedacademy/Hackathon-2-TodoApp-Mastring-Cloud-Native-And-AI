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
    // Redirect only when authenticated (not loading check removed to prevent unmounting)
    if (state.isAuthenticated) {
      router.push('/dashboard');
    }
  }, [state.isAuthenticated, router]);

  // Only show loading screen if authenticated (redirect in progress)
  // Don't hide form during signup/signin loading - let the form handle its own loading state
  if (state.isAuthenticated) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-xl">Redirecting to dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-6 sm:py-12 px-4 sm:px-6 lg:px-8">
      <div className="sm:mx-auto w-full max-w-sm sm:max-w-md">
        <h2 className="mt-4 sm:mt-6 text-center text-2xl sm:text-3xl font-extrabold text-gray-900 dark:text-gray-100">
          TodoApp
        </h2>
        <p className="mt-2 text-center text-xs sm:text-sm text-gray-600 dark:text-gray-400">
          {/* This conditional rendering based on children type is fragile and should be avoided.
              A better approach would be to pass a prop to the layout indicating the page type. */}
          {/* For now, keeping original logic for consistency if children is React Element with type.name */}
          {React.isValidElement(children) && typeof children.type === 'function' && (children.type as any).name === 'SignupPage'
            ? 'Create a new account'
            : 'Sign in to your account'}
        </p>
      </div>

      <div className="mt-6 sm:mt-8 sm:mx-auto w-full max-w-sm sm:max-w-md">
        <div className="bg-white dark:bg-gray-800 py-6 sm:py-8 px-4 sm:px-6 md:px-10 shadow-lg sm:rounded-lg">
          {children}
        </div>
      </div>
    </div>
  );
}