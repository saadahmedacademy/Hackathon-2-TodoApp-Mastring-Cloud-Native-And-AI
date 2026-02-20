'use client';

import { useState, useEffect } from 'react';
import { User } from '@/types';

interface Session {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
}

interface UseSessionReturn {
  data: { user: User | null } | null;
  isPending: boolean;
  error: Error | null;
}

/**
 * Custom session hook that works with the existing FastAPI backend
 * Stores tokens in sessionStorage (cleared on tab close, persists on refresh)
 * Provides BetterAuth-like API: { data: { user }, isPending }
 */

const SESSION_KEY = 'app_session';

function getStoredSession(): Session | null {
  if (typeof window === 'undefined') return null;

  try {
    const stored = sessionStorage.getItem(SESSION_KEY);
    if (!stored) return null;
    return JSON.parse(stored);
  } catch (e) {
    console.error('Failed to parse session:', e);
    return null;
  }
}

function storeSession(session: Session | null) {
  if (typeof window === 'undefined') return;

  if (session) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
  } else {
    sessionStorage.removeItem(SESSION_KEY);
  }
}

export function useSession(): UseSessionReturn {
  const [session, setSession] = useState<Session | null>(null);
  const [isPending, setIsPending] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Initialize session from sessionStorage
    const storedSession = getStoredSession();
    setSession(storedSession);
    setIsPending(false);
  }, []);

  return {
    data: session?.user ? { user: session.user } : null,
    isPending,
    error,
  };
}

/**
 * Update the session (called after successful login/signup)
 */
export function setSessionData(user: User, accessToken: string, refreshToken: string) {
  const session = { user, accessToken, refreshToken };
  storeSession(session);

  // Trigger storage event for other tabs/windows
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event('session-changed'));
  }
}

/**
 * Clear the session (called on logout)
 */
export function clearSessionData() {
  storeSession(null);

  // Trigger storage event for other tabs/windows
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event('session-changed'));
  }
}

/**
 * Get current access token
 */
export function getAccessToken(): string | null {
  const session = getStoredSession();
  return session?.accessToken || null;
}

/**
 * Get current user
 */
export function getCurrentUser(): User | null {
  const session = getStoredSession();
  return session?.user || null;
}
