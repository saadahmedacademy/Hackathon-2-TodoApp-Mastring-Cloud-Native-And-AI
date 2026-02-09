'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

const Sidebar = () => {
  const pathname = usePathname();
  const { state } = useAuth();

  const isActive = (path: string) => pathname.startsWith(path);

  if (!state.isAuthenticated) {
    return null; // Don't show sidebar for non-authenticated users
  }

  return (
    <aside className="w-64 bg-background border-r border-border min-h-screen hidden md:block">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-foreground">Navigation</h2>
        <nav className="mt-6">
          <ul className="space-y-2">
            <li>
              <Link
                href="/dashboard"
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg ${
                  isActive('/dashboard') && !isActive('/dashboard/todos') && !isActive('/dashboard/new')
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`}
              >
                <span className="ml-3">Dashboard</span>
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/todos"
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg ${
                  isActive('/dashboard/todos')
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`}
              >
                <span className="ml-3">All Todos</span>
              </Link>
            </li>
            <li>
              <Link
                href="/dashboard/new"
                className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg ${
                  isActive('/dashboard/new')
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-accent hover:text-foreground'
                }`}
              >
                <span className="ml-3">Create Todo</span>
              </Link>
            </li>
          </ul>
        </nav>

        <div className="mt-8 pt-8 border-t border-border">
          <div className="px-4 py-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Account</p>
            <p className="mt-1 text-sm text-foreground truncate">{state.user?.email}</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;