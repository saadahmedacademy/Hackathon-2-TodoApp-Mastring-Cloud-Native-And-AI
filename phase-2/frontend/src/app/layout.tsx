import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from '@/contexts/AuthContext';
import { ToastProvider } from '@/contexts/ToastContext';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "TodoApp - Manage Your Tasks",
    template: "%s | TodoApp",
  },
  description: "A secure todo application with authentication",
  keywords: ["todo", "productivity", "task management", "authentication"],
  authors: [{ name: "TodoApp Team" }],
  creator: "TodoApp Team",
  publisher: "TodoApp Team",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://todoapp.example.com",
    title: "TodoApp - Manage Your Tasks",
    description: "A secure todo application with authentication",
    siteName: "TodoApp",
  },
  twitter: {
    card: "summary_large_image",
    title: "TodoApp - Manage Your Tasks",
    description: "A secure todo application with authentication",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <AuthProvider>
          <ToastProvider>
            {children}
          </ToastProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
