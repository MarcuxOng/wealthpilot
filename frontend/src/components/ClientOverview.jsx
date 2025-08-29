import React from 'react';

const ClientOverview = ({ client_summary = {}, client = {} }) => (
  <section className="client-section">
    <h2>Client Overview</h2>
    <div className="client-grid">
      <div className="client-kv-list">
        <div className="client-kv">
          <span className="kv-label">
            Name
          </span>
          <span className="kv-value">
            {client?.name || client_summary?.name || 'Unknown Client'}
          </span>
        </div>
        <div className='client-kv'>
          <span className='kv-label'>
            Age
          </span>
          <span className='kv-value'>
            {client?.age || client_summary?.age || 'N/A'}
          </span>
        </div>
        <div className='client-kv'>
          <span className='kv-label'>
            Annual Income
          </span>
          <span className='kv-value'>
            {client?.annual_income ? `$${client.annual_income.toLocaleString()}` : (client_summary?.annual_income ? `$${client_summary.annual_income.toLocaleString()}` : 'N/A')}
          </span>
        </div>
        <div className="client-kv">
          <span className="kv-label">
            Risk Profile
          </span>
          <span className="kv-value">
            {client?.risk_profile || client_summary?.risk_profile || 'Not specified'}
          </span>
        </div>
      </div>
      
      {client_summary && (
        <div className="insights-section">
          <h3>Key Insights</h3>
          <ul className="insights-list">
            {(client_summary.key_insights || []).map((insight, index) => (
              <li key={index}>{insight || 'No insight available'}</li>
            ))}
          </ul>
          <h4>Risk Assessment</h4>
          <p className="analysis-text">{client_summary.risk_assessment || 'Risk assessment not available'}</p>
        </div>
      )}
    </div>
  </section>
);

export default ClientOverview;