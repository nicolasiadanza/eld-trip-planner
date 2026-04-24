import React from 'react';

const ErrorMessage = ({ message }) => {
  return (
    <div className="error-message">
      <span>⚠️</span> {message}
    </div>
  );
};

export default ErrorMessage;
