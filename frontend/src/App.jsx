import { useState } from 'react'
import './App.css'
import AppHeader from './components/AppHeader.jsx'
import ClientInput from './components/ClientInput.jsx'
import ErrorMessage from './components/ErrorMessage.jsx'
import ClientOverview from './components/ClientOverview.jsx'
import ProductRecommendations from './components/ProductRecommendations.jsx'

function App() {
  const [clientId, setClientId] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchAnalysis = async () => {
    try {
      setLoading(true)
      setError('')
      setAnalysis(null)
      
      if (!clientId.match(/^[a-zA-Z0-9-]+$/)) {
        throw new Error('Invalid Client ID format')
      }
      
      const response = await fetch(`http://localhost:8000/client/${encodeURIComponent(clientId)}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
      
      // Validate response structure
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid API response format');
      }
      
      if (data.status === 'error' || !data.ai_analysis) {
        throw new Error(data.ai_analysis?.error || 'Analysis unavailable');
      }
      
      // Ensure data structure integrity
      // Add debug logging to inspect API response
      console.log('Raw API Response:', data);
      
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
      console.log('Normalized Data:', normalizedData);
      setAnalysis(normalizedData);
    } catch (err) {
      setError(err.message)
      setAnalysis(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <AppHeader />

      <div className="analysis-container">
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
    </div>
  )
}

export default App
