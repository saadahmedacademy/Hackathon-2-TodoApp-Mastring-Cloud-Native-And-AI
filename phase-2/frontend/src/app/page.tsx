'use client';

import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';

export default function HomePage() {
  const { state } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-center min-h-[80vh] py-12">
          <div className="text-center">
            <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
              <span className="block">Manage Your Tasks</span>
              <span className="block text-blue-600 mt-2">With TodoApp</span>
            </h1>
            <p className="mt-4 text-xl text-gray-500 max-w-3xl mx-auto">
              A secure, responsive todo application that helps you organize your daily tasks efficiently.
            </p>

            <div className="mt-10 flex justify-center gap-4">
              {!state.isAuthenticated ? (
                <>
                  <Link
                    href="/signin"
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-blue-700 bg-blue-100 hover:bg-blue-200"
                  >
                    Sign Up
                  </Link>
                </>
              ) : (
                <Link
                  href="/dashboard"
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                >
                  Go to Dashboard
                </Link>
              )}
            </div>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 max-w-5xl w-full">
            <div className="pt-6">
              <div className="flow-root bg-white rounded-lg px-6 pb-8 shadow-lg">
                <div className="-mt-6">
                  <h3 className="text-lg font-medium text-gray-900">Task Management</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Easily create, update, and manage your tasks with our intuitive interface.
                  </p>
                </div>
              </div>
            </div>

            <div className="pt-6">
              <div className="flow-root bg-white rounded-lg px-6 pb-8 shadow-lg">
                <div className="-mt-6">
                  <h3 className="text-lg font-medium text-gray-900">Secure Authentication</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Your data is protected with industry-standard security measures.
                  </p>
                </div>
              </div>
            </div>

            <div className="pt-6">
              <div className="flow-root bg-white rounded-lg px-6 pb-8 shadow-lg">
                <div className="-mt-6">
                  <h3 className="text-lg font-medium text-gray-900">Responsive Design</h3>
                  <p className="mt-2 text-base text-gray-500">
                    Access your tasks anywhere, on any device with our responsive design.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
