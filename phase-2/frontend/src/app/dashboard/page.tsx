'use client';

import React from 'react';
import { useAuth } from '@/hooks/useAuth';

export default function DashboardPage() {
  const { state } = useAuth();

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Dashboard</h1>
      <div className="bg-white shadow rounded-lg p-6">
        <p className="text-gray-700">
          Welcome back, {state.user?.email}! This is your personalized dashboard.
        </p>
        <p className="mt-2 text-gray-600">
          From here you can manage your todos, track your productivity, and customize your settings.
        </p>
      </div>
    </div>
  );
}