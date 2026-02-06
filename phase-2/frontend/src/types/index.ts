// General type definitions for the Todo application

export interface User {
  id: string;
  email: string;
  createdAt: string; // ISO date string
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface TodoResponse {
  data: Todo | Todo[];
}

export interface ErrorResponse {
  message: string;
  code?: string;
  details?: Record<string, unknown>;
}