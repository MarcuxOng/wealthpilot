import React from 'react';

const ProductRecommendations = ({ recommendations = [] }) => (
  <section className="analysis-section">
    <h2>Product Recommendations</h2>
    <ul className="recommendations-list">
      {recommendations.map((product, index) => {
        const expectedReturn = typeof product?.expected_return === 'number'
          ? `${product.expected_return}%`
          : null;
        return (
          <li key={product?.id || index} className="recommendation-item">
            <div className="recommendation-header">
              <h3 className="recommendation-title">{product?.name || `Product ${index + 1}`}</h3>
              <div className="badge-row">
                {product?.type && <span className="badge type">{product.type}</span>}
                {product?.risk_level && <span className="badge risk">Risk: {product.risk_level}</span>}
                {product?.priority && <span className={`badge priority ${product.priority}`}>{product.priority}</span>}
              </div>
            </div>
            {product?.reason && <p className="product-reason">{product.reason}</p>}
            {expectedReturn && (
              <div className="expected-return">
                <span className="value">{expectedReturn}</span>
                <span className="label">Expected Return</span>
              </div>
            )}
          </li>
        );
      })}
      {recommendations.length === 0 && (
        <li className="no-products">No recommendations available.</li>
      )}
    </ul>
  </section>
);

export default ProductRecommendations;