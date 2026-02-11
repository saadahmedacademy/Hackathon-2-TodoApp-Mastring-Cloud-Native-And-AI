import { apiClient } from './api';

// Authentication utility functions

/**
 * Checks if the user is currently authenticated
 * @returns boolean indicating authentication status
 */
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') {
    return false;
  }

  const token = localStorage.getItem('jwt_token');
  return token !== null && token.length > 0;
};

/**
 * Gets the current authentication token
 * @returns string token or null if not authenticated
 */
export const getToken = (): string | null => {
  if (typeof window === 'undefined') {
    return null;
  }

  return localStorage.getItem('jwt_token');
};

/**
 * Stores the authentication token and user ID
 * @param token The JWT token to store
 * @param userId The user ID to store
 */
export const setToken = (token: string, userId?: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('jwt_token', token);
    if (userId) {
      localStorage.setItem('user_id', userId);
    }
    // Update the API client's token
    apiClient.setToken(token);
  }
};

/**
 * Removes the authentication token
 */
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_id');
    // Update the API client's token
    apiClient.setToken(null);
  }
};

/**
 * Validates if the token is still valid (basic check)
 * @param token The token to validate
 * @returns boolean indicating if token is valid
 */
export const isValidToken = (token: string | null): boolean => {
  if (!token) return false;

  try {
    // Basic JWT validation - check if it has 3 parts separated by dots
    const parts = token.split('.');
    if (parts.length !== 3) return false;

    // Decode the payload to check expiration
    const payload = JSON.parse(atob(parts[1]));
    const currentTime = Math.floor(Date.now() / 1000);

    // Check if token is expired (using 'exp' claim if available)
    if (payload.exp && payload.exp < currentTime) {
      return false;
    }

    return true;
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
};

/**
 * Extracts the user ID from the JWT token
 * @param token The JWT token to extract user ID from
 * @returns The user ID or null if not found
 */
export const getUserIdFromToken = (token: string): string | null => {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;

    const payload = JSON.parse(atob(parts[1]));

    // Assuming the user ID is stored in the 'sub' (subject) field of the JWT
    // This is a common practice but could be different depending on the backend implementation
    return payload.sub || null;
  } catch (error) {
    console.error('Error extracting user ID from token:', error);
    return null;
  }
};