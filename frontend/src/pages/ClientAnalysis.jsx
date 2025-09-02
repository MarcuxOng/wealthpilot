import React, { useState } from 'react';
import ClientInput from '../components/ClientInput.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';
import ClientOverview from '../components/ClientOverview.jsx';
import ProductRecommendations from '../components/ProductRecommendations.jsx';

const ClientAnalysis = () => {
  const [clientId, setClientId] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchAnalysis = async () => {
    try {
      setLoading(true);
      setError('');
      
      if (!clientId.match(/^[a-zA-Z0-9-]+$/)) {
        throw new Error('Invalid Client ID format');
      }
      
      const response = await fetch(`/client_analysis/${encodeURIComponent(clientId)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid API response format');
      }
      
      if (data.status === 'error' || !data.ai_analysis) {
        throw new Error(data.ai_analysis?.error || 'Analysis unavailable');
      }
      
      // Ensure data structure integrity
      // Add debug logging to inspect API response
      
      const normalizedData = {
        ...data,
        client: {
          name: data.client?.name || 'Unknown Client',
          risk_profile: data.client?.risk_profile?.toString() || 'Not specified',
          investment_horizon: data.client?.investment_horizon || 'N/A',
          ...data.client
        },
        ai_analysis: {
          ...data.ai_analysis,
          client_summary: {
            profile_overview: data.ai_analysis?.client_summary?.profile_overview || 'No profile overview available',
            key_insights: data.ai_analysis?.client_summary?.key_insights || [],
            risk_assessment: data.ai_analysis?.client_summary?.risk_assessment || 'No risk assessment available',
            ...data.ai_analysis?.client_summary
          },
          summary: data.ai_analysis?.summary || 'No analysis summary available',
          recommendations: (Array.isArray(data.ai_analysis?.recommendations) ? data.ai_analysis.recommendations : [])
            .filter(p => p && (p.id || p.name || p.product_id || p.product_name))
            .map(p => ({
              id: p.id || p.product_id || Math.random().toString(36).substr(2, 9),
              name: p.name || p.product_name || 'Unnamed Product',
              type: p.type || 'General Investment',
              risk_level: p.risk_level || 'Not rated',
              ...p
            }))
        }
      };
      setAnalysis(normalizedData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analysis-container">
      <h2>Client Analysis</h2>
      <ClientInput
        clientId={clientId}
        setClientId={setClientId}
        fetchAnalysis={fetchAnalysis}
        loading={loading}
      />

      <ErrorMessage error={error} />

      {analysis && (
        <div className="analysis-results">
          <ClientOverview client_summary={analysis.ai_analysis?.client_summary} client={analysis.client} />
          <ProductRecommendations recommendations={analysis.ai_analysis?.recommendations} />
        </div>
      )}
    </div>
  );
};

export default ClientAnalysis;
