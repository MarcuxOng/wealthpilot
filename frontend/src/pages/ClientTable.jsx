import React, { useState, useEffect } from 'react';

const ClientTable = () => {
  const [clients, setClients] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchClients = async () => {
      try {
        setLoading(true);
        const response = await fetch('/clients');
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setClients(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchClients();
  }, []);

  if (loading) {
    return <div className="loading">Loading clients...</div>;
  }

  if (error) {
    return <div className="error">Error loading clients: {error}</div>;
  }

  const clientList = Object.values(clients);

  return (
    <div className="client-table-container">
      <h2>Client Database</h2>
      <div className="table-wrapper">
        <table className="client-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Annual Income</th>
              <th>Risk Profile</th>
              <th>Investment Goals</th>
              <th>Time Horizon</th>
              <th>Current Savings</th>
              <th>Monthly Surplus</th>
              <th>Dependents</th>
              <th>Employment Status</th>
              <th>Investment Experience</th>
            </tr>
          </thead>
          <tbody>
            {clientList.map((client) => (
              <tr key={client.id}>
                <td>{client.id}</td>
                <td>{client.name}</td>
                <td>{client.age}</td>
                <td>${client.annual_income?.toLocaleString()}</td>
                <td>
                  <span className={`risk-badge risk-${client.risk_profile}`}>
                    {client.risk_profile}
                  </span>
                </td>
                <td>
                  <ul className="goals-list">
                    {client.investment_goals?.map((goal, index) => (
                      <li key={index}>{goal}</li>
                    ))}
                  </ul>
                </td>
                <td>{client.time_horizon}</td>
                <td>${client.current_savings?.toLocaleString()}</td>
                <td>${client.monthly_surplus?.toLocaleString()}</td>
                <td>{client.dependents}</td>
                <td>{client.employment_status}</td>
                <td>{client.investment_experience}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ClientTable;
