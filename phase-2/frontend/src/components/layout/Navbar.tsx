'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { useDarkMode } from '@/contexts/DarkModeContext';
import Button from '@/components/ui/Button';
import { MoonIcon, SunIcon, MenuIcon } from 'lucide-react';

interface NavbarProps {
  onChatToggle?: () => void;
  chatOpen?: boolean;
  onMenuToggle?: () => void;
}

const Navbar = ({ onChatToggle, chatOpen, onMenuToggle }: NavbarProps) => {
  const pathname = usePathname();
  const { state, signout } = useAuth();
  const { darkMode, toggleDarkMode } = useDarkMode();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-background border-b border-border text-foreground px-4 py-3">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          {/* Hamburger menu button - only visible on mobile/tablet when authenticated */}
          {state.isAuthenticated && onMenuToggle && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onMenuToggle}
              className="lg:hidden p-2 rounded-md hover:bg-accent"
              aria-label="Open menu"
            >
              <MenuIcon className="h-6 w-6 text-foreground" />
            </Button>
          )}

          <Link href="/" className="text-xl font-bold text-primary">
            TodoApp
          </Link>

          {state.isAuthenticated && (
            <div className="hidden md:flex space-x-8 ml-6">
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

        <div className="flex items-center space-x-2 sm:space-x-4">
          {/* Chat toggle button — only shown when authenticated */}
          {state.isAuthenticated && onChatToggle && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onChatToggle}
              className={`p-2 rounded-full hover:bg-accent ${chatOpen ? 'bg-accent' : ''}`}
              aria-label={chatOpen ? 'Close AI chat' : 'Open AI chat'}
              aria-expanded={chatOpen}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-foreground" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </Button>
          )}

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
              <span className="text-sm text-muted-foreground hidden md:inline">
                Welcome, {state.user?.email}
              </span>
              <Button
                onClick={signout}
                variant="outline"
                size="sm"
                className="border-input text-foreground hover:bg-accent"
              >
                Logout
              </Button>
            </>
          ) : (
            <div className="flex space-x-2 sm:space-x-3">
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