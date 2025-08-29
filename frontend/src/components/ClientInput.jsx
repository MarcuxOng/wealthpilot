import React from 'react';

const ClientInput = ({ clientId, setClientId, fetchAnalysis, loading }) => (
  <div className="input-section">
    <input
      type="text"
      value={clientId}
      onChange={(e) => setClientId(e.target.value)}
      placeholder="Enter Client ID"
      className="hsbc-input"
    />
    <button
      onClick={fetchAnalysis}
      className="hsbc-button"
      disabled={loading || !clientId}
    >
      {loading ? 'Analyzing...' : 'Get Analysis'}
    </button>
  </div>
);

export default ClientInput;