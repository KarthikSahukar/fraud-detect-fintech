import React from "react";

function TransactionFeed({ transactions }) {
  if (!transactions.length)
    return <p className="empty">No transactions yet. Hit Simulate to generate one!</p>;

  return (
    <div style={{ overflowX: "auto", maxHeight: 360, overflowY: "auto" }}>
      <table className="tx-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Merchant</th>
            <th>Location</th>
            <th>Amount</th>
            <th>Fraud Score</th>
            <th>Status</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => (
            <tr key={tx.id} className={tx.is_fraud ? "fraud-row" : ""}>
              <td style={{ color: "#4a5568" }}>{tx.id}</td>
              <td>{tx.merchant}</td>
              <td>{tx.location}</td>
              <td>₹{tx.amount.toFixed(2)}</td>
              <td>
                <span className={`score ${tx.fraud_score > 0.6 ? "high" : ""}`}>
                  {(tx.fraud_score * 100).toFixed(1)}%
                </span>
              </td>
              <td>
                <span className={`badge ${tx.is_fraud ? "fraud" : "legit"}`}>
                  {tx.is_fraud ? "⚠️ Fraud" : "✅ Legit"}
                </span>
              </td>
              <td style={{ color: "#4a5568", fontSize: 12 }}>
                {new Date(tx.timestamp).toLocaleTimeString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionFeed;
