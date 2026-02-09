'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState, AuthContextType, SignupCredentials, SigninCredentials } from '@/types/auth';
import { User } from '@/types';
import { apiClient } from '@/lib/api';
import { isValidToken } from '@/lib/auth';

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
      const hasValidUser = action.payload.user && action.payload.user.email; // Keep for now as context, but not used in isAuthenticated directly.
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


  const getStoredAuth = (): { token: string | null; user: User | null } => {
    const token = localStorage.getItem('jwt_token');
    const userData = localStorage.getItem('user_data');
    let user: User | null = null;
    if (userData) {
      try {
        user = JSON.parse(userData);
      } catch (e) {
        console.error("Failed to parse stored user data:", e);
        localStorage.removeItem('user_data');
      }
    }
    return { token, user };
  };

  const setLocalAuth = (token: string | null, user: User | null) => {
    if (token) {
      localStorage.setItem('jwt_token', token);
    } else {
      localStorage.removeItem('jwt_token');
    }
    if (user) {
      localStorage.setItem('user_data', JSON.stringify(user));
    } else {
      localStorage.removeItem('user_data');
    }
    apiClient.setToken(token);
  };

  useEffect(() => {
    const initializeAuth = async () => {
      // Start loading
      dispatch({ type: 'SET_LOADING', payload: true });

      let { token, user } = getStoredAuth();

      if (token && isValidToken(token)) {
        // Token is valid. Now check user data consistency.
        if (!user || !user.email) {
          console.warn('AuthContext: Valid token found but user data is missing or malformed (no email). Clearing user data from localStorage.');
          localStorage.removeItem('user_data'); // Clear only the user data, keep token if valid
          user = null; // Ensure user is null for the next step
        }
        setLocalAuth(token, user); // Call setLocalAuth with potentially null user
        dispatch({ type: 'AUTH_INIT', payload: { user, token } });
      } else {
        // If token is invalid or not present, clear local storage and set unauthenticated state
        setLocalAuth(null, null); // Clear any invalid/expired tokens
        dispatch({ type: 'AUTH_INIT', payload: { user: null, token: null } });
      }
      // Set loading to false only after all checks are done
      dispatch({ type: 'SET_LOADING', payload: false });
    };

    initializeAuth();
  }, []); // Empty dependency array means this runs once on mount

  const signup = async (credentials: SignupCredentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null }); // Clear previous errors

    try {
      const result = await apiClient.signup(credentials);

      if (result.error) {
        throw new Error(result.error);
      }

      if (result.data) {
        // After successful registration, do NOT set auth state or store token.
        // The user should explicitly log in.
        // The calling component (e.g., SignupForm) will handle redirection to /login.
      } else {
        throw new Error('Signup failed: No user data returned');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Signup failed';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const signin = async (credentials: SigninCredentials) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    dispatch({ type: 'SET_ERROR', payload: null }); // Clear previous errors

    try {
      const result = await apiClient.signin(credentials);

      if (result.error) {
        throw new Error(result.error);
      }

      if (result.data) {
        const { user, access_token, token_type } = result.data;
        setLocalAuth(access_token, user);

        dispatch({
          type: 'SIGNIN_SUCCESS',
          payload: { user, token: access_token },
        });
      } else {
        throw new Error('Signin failed: No user data returned');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Signin failed';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const signout = async () => {
    dispatch({ type: 'SET_LOADING', payload: true }); // Indicate loading for signout
    try {
      await apiClient.signout();
    } catch (error) {
      console.error('Signout API call failed:', error);
    } finally {
      setLocalAuth(null, null);
      dispatch({ type: 'SIGNOUT_SUCCESS' });
      dispatch({ type: 'SET_LOADING', payload: false }); // Done loading after signout
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

