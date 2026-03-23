import React, { useState, useEffect } from "react";
import TransactionFeed from "./components/TransactionFeed";
import FraudAlerts from "./components/FraudAlerts";
import StatsChart from "./components/StatsChart";
import SimulateButton from "./components/SimulateButton";
import "./App.css";

function App() {
  const [transactions, setTransactions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const [txRes, statsRes] = await Promise.all([
        fetch("http://localhost:5000/api/transactions?limit=50"),
        fetch("http://localhost:5000/api/stats"),
      ]);
      const txData = await txRes.json();
      const statsData = await statsRes.json();
      setTransactions(txData);
      setStats(statsData);
    } catch (err) {
      console.error("API error:", err);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <h1>🏦 FraudShield</h1>
          <span className="subtitle">Real-Time Transaction Fraud Detection</span>
        </div>
        <div className="header-right">
          {stats && (
            <div className="stat-pills">
              <div className="pill total">Total: {stats.total_transactions}</div>
              <div className="pill fraud">Fraud: {stats.fraud_count}</div>
              <div className="pill rate">Rate: {stats.fraud_rate}%</div>
            </div>
          )}
        </div>
      </header>

      <main className="main">
        <div className="top-row">
          <SimulateButton onTransactionAdded={fetchData} setLoading={setLoading} loading={loading} />
        </div>

        <div className="grid">
          <div className="card wide">
            <h2>Transaction Feed</h2>
            <TransactionFeed transactions={transactions} />
          </div>
          <div className="card">
            <h2>⚠️ Fraud Alerts</h2>
            <FraudAlerts transactions={transactions.filter(t => t.is_fraud)} />
          </div>
          <div className="card">
            <h2>📊 Stats Overview</h2>
            <StatsChart stats={stats} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;