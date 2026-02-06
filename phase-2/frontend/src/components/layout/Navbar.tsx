'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/ui/Button';

const Navbar = () => {
  const pathname = usePathname();
  const { state, signout } = useAuth();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-10">
          <Link href="/" className="text-xl font-bold text-blue-600">
            TodoApp
          </Link>

          {state.isAuthenticated && (
            <div className="hidden md:flex space-x-8">
              <Link
                href="/dashboard"
                className={`font-medium ${isActive('/dashboard') ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              >
                Dashboard
              </Link>
              <Link
                href="/dashboard/todos"
                className={`font-medium ${isActive('/dashboard/todos') ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              >
                Todos
              </Link>
              <Link
                href="/dashboard/new"
                className={`font-medium ${isActive('/dashboard/new') ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              >
                New Todo
              </Link>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          {state.isAuthenticated ? (
            <>
              <span className="text-sm text-gray-500 hidden sm:inline">
                Welcome, {state.user?.email}
              </span>
              <Button onClick={signout} variant="outline" size="sm">
                Logout
              </Button>
            </>
          ) : (
            <div className="flex space-x-3">
              <Link href="/signin">
                <Button variant="outline" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button variant="primary" size="sm">
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