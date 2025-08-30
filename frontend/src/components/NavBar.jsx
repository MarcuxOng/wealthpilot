import React from 'react';

const NavBar = ({ currentPage, onPageChange }) => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <div className="nav-brand">
          <h2>HSBC</h2>
        </div>
        <ul className="nav-menu">
          <li className="nav-item">
            <button 
              className={`nav-link ${currentPage === 'client-table' ? 'active' : ''}`}
              onClick={() => onPageChange('client-table')}
            >
              Client Table
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${currentPage === 'products-table' ? 'active' : ''}`}
              onClick={() => onPageChange('products-table')}
            >
              Products Table
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${currentPage === 'client-analysis' ? 'active' : ''}`}
              onClick={() => onPageChange('client-analysis')}
            >
              Client Analysis
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;