'use client';

import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, AlertTriangle, Info, X } from 'lucide-react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose?: () => void;
}

export default function Toast({ message, type = 'info', duration = 5000, onClose }: ToastProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    // Slide in animation
    setTimeout(() => setIsVisible(true), 10);

    // Progress bar animation
    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, 100 - (elapsed / duration) * 100);
      setProgress(remaining);
    }, 50);

    // Auto-close
    if (duration > 0) {
      const timer = setTimeout(() => {
        handleClose();
      }, duration);

      return () => {
        clearTimeout(timer);
        clearInterval(interval);
      };
    }

    return () => clearInterval(interval);
  }, [duration]);

  const handleClose = () => {
    setIsLeaving(true);
    setTimeout(() => {
      setIsVisible(false);
      if (onClose) onClose();
    }, 300);
  };

  if (!isVisible && !isLeaving) return null;

  const typeConfig = {
    success: {
      icon: CheckCircle2,
      bg: 'bg-black',
      border: 'border-green-500',
      text: 'text-green-400',
      iconColor: 'text-green-500',
      progressBg: 'bg-green-500',
      shadow: 'shadow-green-500/30',
    },
    error: {
      icon: XCircle,
      bg: 'bg-black',
      border: 'border-green-500',
      text: 'text-green-400',
      iconColor: 'text-green-500',
      progressBg: 'bg-green-500',
      shadow: 'shadow-green-500/30',
    },
    warning: {
      icon: AlertTriangle,
      bg: 'bg-black',
      border: 'border-green-500',
      text: 'text-green-400',
      iconColor: 'text-green-500',
      progressBg: 'bg-green-500',
      shadow: 'shadow-green-500/30',
    },
    info: {
      icon: Info,
      bg: 'bg-black',
      border: 'border-green-500',
      text: 'text-green-400',
      iconColor: 'text-green-500',
      progressBg: 'bg-green-500',
      shadow: 'shadow-green-500/30',
    },
  };

  const config = typeConfig[type];
  const Icon = config.icon;

  return (
    <div
      className={`
        relative overflow-hidden rounded-xl border-2 shadow-2xl backdrop-blur-sm
        ${config.bg} ${config.border} ${config.shadow}
        transform transition-all duration-300 ease-out
        ${isVisible && !isLeaving ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
        min-w-[320px] max-w-md
      `}
    >
      {/* Progress bar */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-200 dark:bg-gray-700">
        <div
          className={`h-full ${config.progressBg} transition-all duration-100 ease-linear`}
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="flex items-start gap-3 p-4 pr-12">
        {/* Icon */}
        <div className={`flex-shrink-0 ${config.iconColor}`}>
          <Icon className="h-6 w-6" />
        </div>

        {/* Message */}
        <div className={`flex-1 ${config.text} text-sm font-medium leading-relaxed pt-0.5`}>
          {message}
        </div>

        {/* Close button */}
        <button
          onClick={handleClose}
          className={`
            absolute top-3 right-3 p-1 rounded-lg
            ${config.iconColor} hover:bg-black/5 dark:hover:bg-white/5
            transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1
            focus:ring-current
          `}
          aria-label="Close notification"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}