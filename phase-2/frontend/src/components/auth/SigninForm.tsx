import React, { useState, useEffect } from 'react'; // Import useEffect
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

// SVG Icons for eye open and eye closed
const EyeOpenIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    {...props}
  >
    <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
    <path
      fillRule="evenodd"
      d="M1.323 11.447C2.811 6.976 7.232 3.75 12 3.75c4.767 0 9.188 3.226 10.677 7.697a11.996 11.996 0 01-21.354 0zM12 17.25a5.25 5.25 0 100-10.5 5.25 5.25 0 000 10.5z"
      clipRule="evenodd"
    />
  </svg>
);

const EyeClosedIcon = (props: React.SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    {...props}
  >
    <path
      fillRule="evenodd"
      d="M.323 11.447C4.811 6.976 7.232 3.75 12 3.75c4.767 0 9.188 3.226 10.677 7.697a11.996 11.996 0 01-21.354 0zM12 12.75a1.5 1.5 0 00-1.5 1.5V15h3v-1.5a1.5 1.5 0 00-1.5-1.5zm1.5-3.75h-3a.75.75 0 000 1.5h3a.75.75 0 000-1.5z"
      clipRule="evenodd"
    />
    <path d="M14.618 18.437a5.25 5.25 0 00-7.236-7.236l-1.464-1.464a7.5 7.5 0 0110.164 10.164l-1.464-1.464z" />
    <path d="M17.25 12a5.25 5.25 0 00-7.236-7.236l-1.464-1.464A7.5 7.5 0 0119.5 13.5h-2.25a.75.75 0 000 1.5H21v-1.5a7.5 7.5 0 00-3.75-6.495V7.5a.75.75 0 000-1.5h-.75z" />
  </svg>
);

interface SigninFormProps {
  onSigninSuccess?: () => void;
}

export default function SigninForm({ onSigninSuccess }: SigninFormProps) {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [showPassword, setShowPassword] = useState(false); // State for password visibility
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

    try {
      await signin({
        email: formData.email,
        password: formData.password,
      });

      if (onSigninSuccess) {
        onSigninSuccess();
      }
    } catch (error: any) {
      setErrors({ form: error.message || state.error || 'An error occurred during sign in' });
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

        <div className="relative"> {/* Added relative positioning */}
          <Input
            label="Password"
            id="password"
            name="password"
            type={showPassword ? 'text' : 'password'} // Dynamic type
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
            error={errors.password}
            fullWidth
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-0 pr-3 flex items-center h-full"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <EyeOpenIcon className="h-5 w-5 text-gray-700 dark:text-gray-300" />
            ) : (
              <EyeClosedIcon className="h-5 w-5 text-gray-700 dark:text-gray-300" />
            )}
          </button>
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
            isLoading={state.isLoading}
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