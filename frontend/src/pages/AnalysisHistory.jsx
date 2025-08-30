import React, { useState, useEffect } from 'react';

const AnalysisHistory = () => {
  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchAnalysisHistory();
  }, []);

  const fetchAnalysisHistory = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch('/client_analysis/history/all');
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.analyses) {
        // Convert the analyses object to a flat array for easier rendering
        const analysesArray = [];
        Object.entries(data.analyses).forEach(([clientId, clientData]) => {
          if (Array.isArray(clientData)) {
            // Multiple analyses per client
            clientData.forEach(analysis => {
              analysesArray.push({
                clientId,
                ...analysis
              });
            });
          } else {
            // Single analysis per client (legacy format)
            analysesArray.push({
              clientId,
              ...clientData
            });
          }
        });
        
        // Sort by timestamp (newest first)
        analysesArray.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        setAnalyses(analysesArray);
        setStats({
          total_analyses: analysesArray.length,
          client_ids: Object.keys(data.analyses)
        });
      } else {
        setAnalyses([]);
        setStats({ total_analyses: 0, client_ids: [] });
      }
    } catch (err) {
      setError(err.message);
      setAnalyses([]);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch (e) {
      return timestamp;
    }
  };

  const deleteAnalysis = async (clientId, timestamp) => {
    if (!window.confirm(`Are you sure you want to delete this specific analysis for client ${clientId}?`)) {
      return;
    }

    try {
      const response = await fetch(`/client_analysis/${clientId}/history/${encodeURIComponent(timestamp)}`, {
        method: 'DELETE'
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // Refresh the list after deletion
      fetchAnalysisHistory();
    } catch (err) {
      setError(`Failed to delete analysis: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="analysis-history-container">
        <h2>Analysis History</h2>
        <div className="loading">Loading analysis history...</div>
      </div>
    );
  }

  return (
    <div className="analysis-history-container">
      <h2>Analysis History</h2>
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      {stats && (
        <div className="stats-section">
          <h3>Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Total Analyses:</span>
              <span className="stat-value">{stats.total_analyses}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Unique Clients:</span>
              <span className="stat-value">{stats.client_ids.length}</span>
            </div>
          </div>
        </div>
      )}

      {analyses.length === 0 ? (
        <div className="no-analyses">
          <p>No analysis history found.</p>
          <p>Run some client analyses to see them here.</p>
        </div>
      ) : (
        <div className="analyses-list">
          <h3>All Analyses</h3>
          {analyses.map((analysis, index) => (
            <div key={analysis.clientId} className="analysis-card">
              <div className="analysis-header">
                <h4>Client: {analysis.clientId}</h4>
                <div className="analysis-actions">
                  <span className="timestamp">
                    {formatTimestamp(analysis.timestamp)}
                  </span>
                                     <button
                     className="delete-btn"
                     onClick={() => deleteAnalysis(analysis.clientId, analysis.timestamp)}
                     title="Delete this analysis"
                   >
                     🗑️
                   </button>
                </div>
              </div>
              
              <div className="analysis-content">
                <div className="client-info">
                  <strong>Client Name:</strong> {analysis.analysis_data?.client?.name || 'N/A'}
                </div>
                <div className="analysis-status">
                  <strong>Status:</strong> 
                  <span className={`status-badge ${analysis.analysis_data?.status || 'unknown'}`}>
                    {analysis.analysis_data?.status || 'Unknown'}
                  </span>
                </div>
                
                {analysis.analysis_data?.ai_analysis && (
                  <div className="ai-analysis-preview">
                    <strong>AI Analysis Summary:</strong>
                    <p className="summary-text">
                      {analysis.analysis_data.ai_analysis.summary || 
                       analysis.analysis_data.ai_analysis.client_summary?.profile_overview ||
                       'No summary available'}
                    </p>
                    
                    {analysis.analysis_data.ai_analysis.recommendations && (
                      <div className="recommendations-preview">
                        <strong>Recommendations:</strong>
                        <ul>
                          {analysis.analysis_data.ai_analysis.recommendations.slice(0, 2).map((rec, idx) => (
                            <li key={idx}>
                              {rec.name || rec.product_name || 'Unnamed Product'}
                              {rec.confidence && ` (${(rec.confidence * 100).toFixed(1)}% confidence)`}
                            </li>
                          ))}
                          {analysis.analysis_data.ai_analysis.recommendations.length > 2 && (
                            <li>... and {analysis.analysis_data.ai_analysis.recommendations.length - 2} more</li>
                          )}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AnalysisHistory;
