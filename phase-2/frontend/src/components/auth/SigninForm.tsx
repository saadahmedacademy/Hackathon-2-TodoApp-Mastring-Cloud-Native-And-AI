import React, { useState, useEffect } from 'react'; // Import useEffect
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

interface SigninFormProps {
  onSigninSuccess?: () => void;
}

export default function SigninForm({ onSigninSuccess }: SigninFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const { state, signin } = useAuth(); // Destructure state from useAuth
  const router = useRouter();

  useEffect(() => {
    // Only redirect if authentication is successful AND there's no custom success handler
    // And only after loading is false (auth state is stable)
    if (state.isAuthenticated && !onSigninSuccess && !state.isLoading) {
      router.push('/dashboard');
    }
  }, [state.isAuthenticated, state.isLoading, onSigninSuccess, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Set loading state from AuthContext
    // setIsLoading(true); // No longer needed, AuthContext manages loading

    try {
      await signin({
        email: formData.email,
        password: formData.password,
      });

      if (onSigninSuccess) {
        onSigninSuccess();
      }
      // Redirect logic is now handled by the useEffect above
    } catch (error: any) {
      setErrors({ form: error.message || state.error || 'An error occurred during sign in' }); // Use state.error if available
    } finally {
      // setIsLoading(false); // No longer needed
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <Input
            label="Email address"
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            fullWidth
          />
        </div>

        <div>
          <Input
            label="Password"
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            fullWidth
          />
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 rounded border border-input bg-background text-primary focus:ring-offset-background focus:ring-2 focus:ring-ring"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-foreground">
              Remember me
            </label>
          </div>

          <div className="text-sm">
            <a href="#" className="font-medium text-primary hover:text-primary/90">
              Forgot your password?
            </a>
          </div>
        </div>

        {errors.form && (
          <div className="rounded-md bg-destructive/10 p-4">
            <div className="text-sm text-destructive">{errors.form}</div>
          </div>
        )}

        <div>
          <Button
            type="submit"
            fullWidth
            isLoading={state.isLoading} // Use state.isLoading from AuthContext
            className="flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
          >
            Sign in
          </Button>
        </div>
      </form>

      <div className="mt-4 text-center">
        <p className="text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link href="/signup" className="font-medium text-primary hover:text-primary/90">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}