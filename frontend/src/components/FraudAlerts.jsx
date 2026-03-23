import React from "react";

function FraudAlerts({ transactions }) {
  if (!transactions.length)
    return <p className="empty">No fraud detected yet.</p>;

  return (
    <div className="alert-list">
      {transactions.slice(0, 10).map((tx) => (
        <div key={tx.id} className="alert-card">
          <div className="alert-amount">₹{tx.amount.toFixed(2)}</div>
          <div className="alert-meta">
            {tx.merchant} — {tx.location}
          </div>
          <div className="alert-score">
            Fraud score: {(tx.fraud_score * 100).toFixed(1)}% &nbsp;|&nbsp;
            {new Date(tx.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ))}
    </div>
  );
}

export default FraudAlerts;
