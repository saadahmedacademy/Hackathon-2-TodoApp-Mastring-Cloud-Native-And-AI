'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useSession, setSessionData, clearSessionData } from '@/hooks/useSession';
import { AuthState, AuthContextType, SignupCredentials, SigninCredentials } from '@/types/auth';
import { User } from '@/types';
import axios from 'axios';

/**
 * AuthContext - Session-based auth using sessionStorage
 * Works with existing FastAPI backend endpoints
 */

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Use custom session hook
  const sessionHook = useSession();
  const [localLoading, setLocalLoading] = useState(false);

  // Re-render when session changes
  const [, setRefresh] = useState(0);

  useEffect(() => {
    const handleSessionChange = () => {
      setRefresh(prev => prev + 1);
    };

    window.addEventListener('session-changed', handleSessionChange);
    return () => window.removeEventListener('session-changed', handleSessionChange);
  }, []);

  // Derive auth state from session
  const state: AuthState = {
    isAuthenticated: !!sessionHook.data?.user,
    user: sessionHook.data?.user || null,
    token: null,
    isLoading: sessionHook.isPending || localLoading,
    error: sessionHook.error?.message || null,
  };

  /**
   * Signup - calls /auth/register endpoint
   * Returns: { user, access_token, refresh_token }
   */
  const signup = async (credentials: SignupCredentials) => {
    setLocalLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, {
        email: credentials.email,
        password: credentials.password,
        name: credentials.email.split('@')[0],
      });

      const { user, access_token, refresh_token } = response.data;

      // Store session
      setSessionData(user, access_token, refresh_token);

      // Redirect using Next.js router (no full reload)
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 100);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Signup failed';
      throw new Error(errorMessage);
    } finally {
      setLocalLoading(false);
    }
  };

  /**
   * Signin - calls /auth/login endpoint
   * Returns: { access_token, refresh_token } (NO USER!)
   * We need to decode JWT to get user info
   */
  const signin = async (credentials: SigninCredentials) => {
    setLocalLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        email: credentials.email,
        password: credentials.password,
      });

      const { access_token, refresh_token } = response.data;

      // Decode JWT to get user ID (basic decode)
      const payload = JSON.parse(atob(access_token.split('.')[1]));

      // Create user object from JWT and credentials
      const user: User = {
        id: payload.sub || payload.user_id,
        email: credentials.email,
        createdAt: new Date().toISOString(),
      };

      // Store session
      setSessionData(user, access_token, refresh_token);

      // Redirect
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 100);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Signin failed';
      throw new Error(errorMessage);
    } finally {
      setLocalLoading(false);
    }
  };

  /**
   * Signout - calls /auth/logout endpoint
   */
  const signout = async () => {
    try {
      await axios.post(`${API_BASE_URL}/auth/logout`);
    } catch (error) {
      console.error('Logout API failed:', error);
    } finally {
      // Clear session
      clearSessionData();
      // Redirect to signin
      window.location.href = '/signin';
    }
  };

  /**
   * Update user
   */
  const updateUser = (userData: Partial<User>) => {
    console.warn('updateUser not implemented');
  };

  const value = {
    state,
    signup,
    signin,
    signout,
    updateUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext };
