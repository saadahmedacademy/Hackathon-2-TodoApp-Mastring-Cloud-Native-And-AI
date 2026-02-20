import axios from 'axios';
import { SigninCredentials, SignupCredentials } from '@/types/auth';
import { ApiResponse, AuthResponse } from '@/types';
import { Todo } from '@/types';
import { getAccessToken } from '@/hooks/useSession';

function normalizeTodo(todo: any): Todo {
  return {
    ...todo,
    createdAt: todo.created_at,
    updatedAt: todo.updated_at,
    display_id: todo.display_id ?? undefined,
  };
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

class ApiClient {
  constructor() {
    axios.defaults.baseURL = API_BASE_URL;
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Inject token from session (in-memory)
    axios.interceptors.request.use(config => {
      const token = getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle 401 responses
    axios.interceptors.response.use(
      response => response,
      error => {
        if (error.response?.status === 401) {
          // Session expired - redirect to signin
          console.warn('Unauthorized - session expired');
          window.location.href = '/signin';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth Endpoints (legacy - use AuthContext methods instead)
  async signup(credentials: SignupCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      const response = await axios.post(`/auth/register`, credentials);
      return { data: response.data, error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Signup failed', status: error.response?.status || 500 };
    }
  }

  async signin(credentials: SigninCredentials): Promise<ApiResponse<AuthResponse>> {
    try {
      const response = await axios.post(`/auth/login`, credentials);
      return { data: response.data, error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Signin failed', status: error.response?.status || 500 };
    }
  }

  async signout(): Promise<ApiResponse<any>> {
    try {
      const response = await axios.post(`/auth/logout`);
      return { data: { success: true }, error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Signout failed', status: error.response?.status || 500 };
    }
  }

  // Todo Endpoints
  async getTodos(): Promise<ApiResponse<Todo[]>> {
    try {
      // Use Next.js proxy with token from session
      const token = getAccessToken();
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch('/api/todos', { headers });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        return {
          data: undefined,
          error: err?.error || err?.detail || 'Failed to fetch todos',
          status: response.status,
        };
      }

      const data = await response.json();
      return { data: Array.isArray(data) ? data.map(normalizeTodo) : [], error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: 'Failed to fetch todos', status: 500 };
    }
  }

  async createTodo(title: string, description?: string): Promise<ApiResponse<Todo>> {
    try {
      const response = await axios.post(`/api/tasks`, { title, description });
      return { data: normalizeTodo(response.data), error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Failed to create todo', status: error.response?.status || 500 };
    }
  }

  async updateTodo(id: string, title?: string, description?: string, completed?: boolean): Promise<ApiResponse<Todo>> {
    try {
      const response = await axios.put(`/api/tasks/${id}`, { title, description, completed });
      return { data: normalizeTodo(response.data), error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Failed to update todo', status: error.response?.status || 500 };
    }
  }

  async deleteTodo(id: string): Promise<ApiResponse<any>> {
    try {
      const response = await axios.delete(`/api/tasks/${id}`);
      return { data: { success: true }, error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Failed to delete todo', status: error.response?.status || 500 };
    }
  }

  async toggleTodo(id: string, completed: boolean): Promise<ApiResponse<Todo>> {
    try {
      const response = await axios.patch(`/api/tasks/${id}/complete`, { completed });
      return { data: normalizeTodo(response.data), error: null, status: response.status };
    } catch (error: any) {
      return { data: undefined, error: error.response?.data?.detail || 'Failed to toggle todo status', status: error.response?.status || 500 };
    }
  }
}

export const apiClient = new ApiClient();
