import { useContext } from 'react';
import { AuthContext } from '@/contexts/AuthContext';

// Export the hook that uses the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};