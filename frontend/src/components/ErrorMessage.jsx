import React from 'react';

const ErrorMessage = ({ error }) => (
  error && <div className="error-message">{error}</div>
);

export default ErrorMessage;