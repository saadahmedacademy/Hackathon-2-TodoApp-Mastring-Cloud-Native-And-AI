'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useRouter } from 'next/navigation';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';
import ChatDrawer from '@/components/chat/ChatDrawer';
import { ChatContext } from '@/contexts/ChatContext';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { state } = useAuth();
  const router = useRouter();
  const [chatOpen, setChatOpen] = useState(false);

  useEffect(() => {
    // Redirect only when not loading and not authenticated
    if (!state.isLoading && !state.isAuthenticated) {
      router.push('/signin');
    }
  }, [state.isAuthenticated, state.isLoading, router]);

  if (state.isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p className="text-xl">Loading authentication...</p>
      </div>
    );
  }

  // Only render children if authenticated and not loading
  if (!state.isAuthenticated) {
    return null;
  }

  return (
    <ChatContext.Provider value={{ openChat: () => setChatOpen(true) }}>
      <div className="min-h-screen bg-background">
        <Navbar onChatToggle={() => setChatOpen((o) => !o)} chatOpen={chatOpen} />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-4 sm:p-6 md:p-8">
            {children}
          </main>
        </div>
        <ChatDrawer isOpen={chatOpen} onClose={() => setChatOpen(false)} />
      </div>
    </ChatContext.Provider>
  );
}