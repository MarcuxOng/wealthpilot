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
      
      const response = await fetch('/analysis_history/history/all');
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.analyses) {
        setAnalyses(data.analyses);
        const client_ids = [...new Set(data.analyses.map(a => a.client_id))];
        setStats({
          total_analyses: data.analyses.length,
          client_ids: client_ids
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

  const deleteAnalysis = async (analysisId) => {
    // Temporarily disabled
    alert("Delete functionality is temporarily disabled.");
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
          {analyses.map((analysis) => (
            <div key={analysis.id} className="analysis-card">
              <div className="analysis-header">
                <h4>Client: {analysis.client_id}</h4>
                <div className="analysis-actions">
                  <button className="delete-btn" onClick={() => deleteAnalysis(analysis.id)} title="Delete this analysis" disabled>
                    🗑️
                   </button>
                </div>
              </div>
              
              <div className="analysis-content">
                <div className="client-info">
                  <strong>Client Name:</strong> {analysis.client_name || 'N/A'}
                </div>
                <div className="analysis-status">
                  <strong>Status:</strong> 
                  <span className={`status-badge success`}>
                    Success
                  </span>
                </div>
                
                {analysis.analysis_result && (
                  <div className="ai-analysis-preview">
                    <strong>AI Analysis Summary:</strong>
                    <p className="summary-text">
                      {analysis.analysis_result.summary || analysis.analysis_result.client_summary?.profile_overview || 'No summary available'}
                    </p>
                    
                    {analysis.analysis_result.recommendations && (
                      <div className="recommendations-preview">
                        <strong>Recommendations:</strong>
                        <ul>
                          {analysis.analysis_result.recommendations.slice(0, 2).map((rec, idx) => (
                            <li key={idx}>
                              {rec.name || rec.product_name || 'Unnamed Product'}
                              {rec.confidence && ` (${(rec.confidence * 100).toFixed(1)}% confidence)`}
                            </li>
                          ))}
                          {analysis.analysis_result.recommendations.length > 2 && (
                            <li>... and {analysis.analysis_result.recommendations.length - 2} more</li>
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