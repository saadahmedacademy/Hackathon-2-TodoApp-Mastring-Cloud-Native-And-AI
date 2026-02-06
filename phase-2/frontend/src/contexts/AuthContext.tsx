'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState, AuthContextType, SignupCredentials, SigninCredentials } from '@/types/auth';
import { User } from '@/types';
import { apiClient } from '@/lib/api';
import { isValidToken, setToken, removeToken } from '@/lib/auth';

// Initial state
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null,
  isLoading: true,
  error: null,
};

// Action types
type AuthAction =
  | { type: 'AUTH_INIT'; payload: { user: User | null; token: string | null } }
  | { type: 'SIGNUP_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'SIGNIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'SIGNOUT_SUCCESS' }
  | { type: 'UPDATE_USER'; payload: Partial<User> }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

// Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_INIT':
      return {
        ...state,
        isAuthenticated: !!action.payload.token && isValidToken(action.payload.token),
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false,
        error: null,
      };
    case 'SIGNUP_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false,
        error: null,
      };
    case 'SIGNIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false,
        error: null,
      };
    case 'SIGNOUT_SUCCESS':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        error: null,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: state.user ? { ...state.user, ...action.payload } : null,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };
    default:
      return state;
  }
};

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    // Initialize auth state from localStorage on mount
    const token = localStorage.getItem('jwt_token');

    if (token && isValidToken(token)) {
      // If we have a valid token, try to get user info
      const fetchUser = async () => {
        dispatch({ type: 'SET_LOADING', payload: true });

        try {
          // We'll need to update the API client to have a method to get user info
          // For now, we'll just validate the token exists and is valid
          // The actual user data can be retrieved separately if needed

          // For this implementation, we'll just initialize with the token
          // and set a temporary user object - in a real app, we'd call an API to get user details
          const tempUser = { id: 'temp', email: 'temp@example.com', createdAt: new Date().toISOString() }; // Placeholder

          dispatch({
            type: 'AUTH_INIT',
            payload: { user: tempUser, token }
          });
        } catch (error) {
          console.error('Failed to initialize auth:', error);
          dispatch({ type: 'SET_ERROR', payload: 'Failed to initialize authentication' });
          removeToken(); // Remove invalid token
        }
      };

      fetchUser();
    } else {
      // No valid token, set loading to false
      dispatch({ type: 'AUTH_INIT', payload: { user: null, token: null } });
    }
  }, []);

  const signup = async (credentials: SignupCredentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const result = await apiClient.signup(credentials);

      if (result.error) {
        throw new Error(result.error);
      }

      if (result.data) {
        const { user, token } = result.data;
        setToken(token);

        dispatch({
          type: 'SIGNUP_SUCCESS',
          payload: { user, token }
        });
      } else {
        throw new Error('Signup failed: No user data returned');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Signup failed';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  const signin = async (credentials: SigninCredentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const result = await apiClient.signin(credentials);

      if (result.error) {
        throw new Error(result.error);
      }

      if (result.data) {
        const { user, token } = result.data;
        setToken(token);

        dispatch({
          type: 'SIGNIN_SUCCESS',
          payload: { user, token }
        });
      } else {
        throw new Error('Signin failed: No user data returned');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Signin failed';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    }
  };

  const signout = async () => {
    try {
      // Call the API to sign out (this might be needed for server-side session cleanup)
      await apiClient.signout();
    } catch (error) {
      // Even if the API call fails, we should still clear the local state
      console.error('Signout API call failed:', error);
    } finally {
      removeToken();
      dispatch({ type: 'SIGNOUT_SUCCESS' });
    }
  };

  const updateUser = (userData: Partial<User>) => {
    dispatch({ type: 'UPDATE_USER', payload: userData });
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

