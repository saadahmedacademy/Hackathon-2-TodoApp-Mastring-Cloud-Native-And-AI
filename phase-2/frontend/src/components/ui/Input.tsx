import React, { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
  rightAdornment?: React.ReactNode; // New prop for adornment
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, fullWidth = false, className = '', rightAdornment, ...props }, ref) => {
    const widthClass = fullWidth ? 'w-full' : '';
    // Adjust padding-right if an adornment is present
    const inputPaddingClass = rightAdornment ? 'pr-10' : '';

    return (
      <div className={`space-y-1 ${widthClass}`}>
        {label && (
          <label htmlFor={props.id} className="block text-sm font-medium text-primary">
            {label}
          </label>
        )}
        <div className="relative flex items-center"> {/* New wrapper for input and adornment */}
          <input
            ref={ref}
            className={`flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
              error ? 'border-destructive text-destructive' : ''
            } ${inputPaddingClass} ${className}`} // Added inputPaddingClass
            aria-invalid={!!error}
            aria-describedby={error ? `${props.id}-error` : helperText ? `${props.id}-helper` : undefined}
            {...props}
          />
          {rightAdornment && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              {rightAdornment}
            </div>
          )}
        </div>
        {error && <p id={`${props.id}-error`} className="text-sm text-red-500 dark:text-red-400">{error}</p>}
        {helperText && !error && <p id={`${props.id}-helper`} className="text-sm text-gray-500 dark:text-gray-400">{helperText}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;