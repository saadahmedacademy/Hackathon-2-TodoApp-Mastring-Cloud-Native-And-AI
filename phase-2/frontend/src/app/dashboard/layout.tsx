'use client';

import React, { useEffect } from 'react'; // Import useEffect
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { state } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Redirect only when not loading and not authenticated
    if (!state.isLoading && !state.isAuthenticated) {
      router.push('/signin');
    }
  }, [state.isAuthenticated, state.isLoading, router]); // Depend on isAuthenticated and isLoading

  if (state.isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-xl">Loading authentication...</p>
      </div>
    );
  }

  // Only render children if authenticated and not loading
  if (!state.isAuthenticated) {
    return null; // Return null if not authenticated and redirecting
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-4 sm:p-6 md:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}