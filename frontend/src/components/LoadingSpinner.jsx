import React from 'react';

export default function LoadingSpinner({ size = 'md', message = null }) {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4'
  };
  
  return (
    <div className="flex flex-col items-center justify-center">
      <div className={`${sizeClasses[size]} rounded-full border-blue-600 border-t-transparent animate-spin`} />
      {message && <p className="mt-2 text-gray-600">{message}</p>}
    </div>
  );
} 