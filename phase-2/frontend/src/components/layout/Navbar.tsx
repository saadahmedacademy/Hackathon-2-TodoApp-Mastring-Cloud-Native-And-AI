'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useDarkMode } from '@/contexts/DarkModeContext';
import Button from '@/components/ui/Button';
import { MoonIcon, SunIcon } from 'lucide-react';

const Navbar = () => {
  const pathname = usePathname();
  const { state, signout } = useAuth();
  const { darkMode, toggleDarkMode } = useDarkMode();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-background border-b border-border text-foreground px-4 py-3">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-10">
          <Link href="/" className="text-xl font-bold text-primary">
            TodoApp
          </Link>

          {state.isAuthenticated && (
            <div className="hidden md:flex space-x-8">
              <Link
                href="/dashboard"
                className={`font-medium ${isActive('/dashboard') ? 'text-primary' : 'text-muted-foreground hover:text-foreground'}`}
              >
                Dashboard
              </Link>
              <Link
                href="/dashboard/todos"
                className={`font-medium ${isActive('/dashboard/todos') ? 'text-primary' : 'text-muted-foreground hover:text-foreground'}`}
              >
                Todos
              </Link>
              <Link
                href="/dashboard/new"
                className={`font-medium ${isActive('/dashboard/new') ? 'text-primary' : 'text-muted-foreground hover:text-foreground'}`}
              >
                New Todo
              </Link>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {/* Dark mode toggle button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleDarkMode}
            className="p-2 rounded-full hover:bg-accent"
            aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {darkMode ? (
              <SunIcon className="h-5 w-5 text-yellow-500" />
            ) : (
              <MoonIcon className="h-5 w-5 text-foreground" />
            )}
          </Button>

          {state.isAuthenticated ? (
            <>
              <span className="text-sm text-muted-foreground hidden sm:inline">
                Welcome, {state.user?.email}
              </span>
                              <Button
                                onClick={signout}
                                variant="outline"
                                size="sm"
                                className="border-input text-foreground hover:bg-accent"
                              >                Logout
              </Button>
            </>
          ) : (
            <div className="flex space-x-3">
              <Link href="/signin">
                <Button
                  variant="outline"
                  size="sm"
                  className="border-input text-foreground hover:bg-accent"
                >
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button
                  variant="primary"
                  size="sm"
                  className="hover:bg-primary/90"
                >
                  Sign Up
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;