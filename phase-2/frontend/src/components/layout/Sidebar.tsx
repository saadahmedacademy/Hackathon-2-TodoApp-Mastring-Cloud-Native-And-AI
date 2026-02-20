'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { XIcon } from 'lucide-react';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

const Sidebar = ({ isOpen = false, onClose }: SidebarProps) => {
  const pathname = usePathname();
  const { state } = useAuth();

  const isActive = (path: string) => pathname.startsWith(path);

  // Close sidebar on route change (mobile)
  useEffect(() => {
    if (isOpen && onClose) {
      onClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  // Prevent body scroll when mobile sidebar is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!state.isAuthenticated) {
    return null; // Don't show sidebar for non-authenticated users
  }

  const sidebarContent = (
    <div className="p-4 h-full flex flex-col">
      {/* Mobile header with close button */}
      <div className="flex items-center justify-between mb-6 lg:hidden">
        <h2 className="text-lg font-semibold text-foreground">Navigation</h2>
        <button
          onClick={onClose}
          className="p-2 rounded-md hover:bg-accent text-foreground"
          aria-label="Close menu"
        >
          <XIcon className="h-5 w-5" />
        </button>
      </div>

      {/* Desktop header */}
      <h2 className="text-lg font-semibold text-foreground hidden lg:block">Navigation</h2>

      <nav className="mt-6 flex-1">
        <ul className="space-y-2">
          <li>
            <Link
              href="/dashboard"
              className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
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
              className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
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
              className={`flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
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
          {state.isLoading ? (
            <div className="mt-1 h-5 w-32 bg-muted animate-pulse rounded"></div>
          ) : (
            <p className="mt-1 text-sm text-foreground truncate">{state.user?.email || 'Not available'}</p>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop sidebar - always visible on large screens */}
      <aside className="w-64 bg-background border-r border-border min-h-screen hidden lg:block">
        {sidebarContent}
      </aside>

      {/* Mobile sidebar - slide-in drawer */}
      <>
        {/* Overlay */}
        {isOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-40 lg:hidden transition-opacity duration-300"
            onClick={onClose}
            aria-hidden="true"
          />
        )}

        {/* Drawer */}
        <aside
          className={`fixed top-0 left-0 h-full w-64 bg-background border-r border-border z-50 lg:hidden transform transition-transform duration-300 ease-in-out ${
            isOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          {sidebarContent}
        </aside>
      </>
    </>
  );
};

export default Sidebar;