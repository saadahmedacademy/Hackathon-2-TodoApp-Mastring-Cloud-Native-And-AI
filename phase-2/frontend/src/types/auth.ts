import { User } from './index';

// Authentication-related type definitions

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface SignupCredentials {
  email: string;
  password: string;
}

export interface SigninCredentials {
  email: string;
  password: string;
}

export interface AuthContextType {
  state: AuthState;
  signup: (credentials: SignupCredentials) => Promise<void>;
  signin: (credentials: SigninCredentials) => Promise<void>;
  signout: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
}