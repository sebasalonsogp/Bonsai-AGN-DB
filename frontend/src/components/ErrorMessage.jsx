import React from 'react';

export default function ErrorMessage({ error, variant = 'default' }) {
  // Parse error message to provide more user-friendly context
  const getErrorMessage = (error) => {
    if (!error) return 'An unknown error occurred';
    
    // Extract message from error object or string
    const message = typeof error === 'string' ? error : error.message || 'An unknown error occurred';
    
    // Convert technical errors to science-friendly messages
    if (message.includes('timeout') || message.includes('ETIMEDOUT')) {
      return 'Query took too long to complete. Please try refining your search criteria to narrow the result set.';
    }
    
    if (message.includes('500')) {
      return 'The server encountered an issue processing your request. This may be due to the complexity of the query.';
    }
    
    if (message.includes('400')) {
      return 'Invalid query parameters. Please check your search criteria for errors.';
    }
    
    if (message.includes('cancelled by user')) {
      return 'Operation cancelled by user.';
    }
    
    return message;
  };
  
  const variantClasses = {
    default: 'bg-red-100 border-red-400 text-red-700',
    warning: 'bg-yellow-100 border-yellow-400 text-yellow-700',
    info: 'bg-blue-100 border-blue-400 text-blue-700'
  };
  
  const displayMessage = getErrorMessage(error);
  
  return (
    <div className={`${variantClasses[variant]} px-4 py-3 rounded flex items-start`}>
      <div className="flex-shrink-0 mr-2">
        {variant === 'default' && <span className="text-red-500">⚠️</span>}
        {variant === 'warning' && <span className="text-yellow-500">⚠️</span>}
        {variant === 'info' && <span className="text-blue-500">ℹ️</span>}
      </div>
      <div>
        <p className="font-medium">{displayMessage}</p>
        {error && error.details && <p className="text-sm mt-1">{error.details}</p>}
      </div>
    </div>
  );
} 