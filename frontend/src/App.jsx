import { useState } from 'react'
import './styles/base.css';
import './styles/app.css';
import './styles/navbar.css';
import './styles/components.css';
import './styles/table.css';
import './styles/badge.css';
import './styles/analysis.css';
import './styles/history.css';
import './styles/responsive.css';
import AppHeader from './components/AppHeader.jsx'
import NavBar from './components/NavBar.jsx'
import ClientTable from './pages/ClientTable.jsx'
import ProductsTable from './pages/ProductsTable.jsx'
import ClientAnalysis from './pages/ClientAnalysis.jsx'
import AnalysisHistory from './pages/AnalysisHistory.jsx'

function App() {
  const [currentPage, setCurrentPage] = useState('client-analysis');

  const renderPage = () => {
    switch (currentPage) {
      case 'client-table':
        return <ClientTable />;
      case 'products-table':
        return <ProductsTable />;
      case 'client-analysis':
        return <ClientAnalysis />;
      case 'analysis-history':
        return <AnalysisHistory />;
      default:
        return <ClientAnalysis />;
    }
  };

  return (
    <div className="app-container">
      <AppHeader />
      <NavBar currentPage={currentPage} onPageChange={setCurrentPage} />
      
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  )
}

export default App
