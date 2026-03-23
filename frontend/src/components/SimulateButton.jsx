import React from "react";
import axios from "axios";

// Generates a random transaction and sends it to the Flask API
function SimulateButton({ onTransactionAdded, setLoading, loading }) {

  const randomFeatures = () =>
    Array.from({ length: 28 }, () => parseFloat((Math.random() * 4 - 2).toFixed(4)));

  // Occasionally generate a suspicious transaction (high amount, extreme features)
  const randomTransaction = () => {
    const isSuspicious = Math.random() < 0.15; // 15% chance of suspicious tx
    return {
      amount: isSuspicious
        ? parseFloat((Math.random() * 5000 + 1000).toFixed(2))  // large amount
        : parseFloat((Math.random() * 200 + 1).toFixed(2)),      // normal amount
      features: isSuspicious
        ? Array.from({ length: 28 }, () => parseFloat((Math.random() * 10 - 5).toFixed(4))) // extreme values
        : randomFeatures(),
      time: Math.floor(Math.random() * 172792),
    };
  };

  const simulate = async () => {
    setLoading(true);
    try {
      const tx = randomTransaction();
      await axios.post("http://localhost:5000/api/predict", tx);
      onTransactionAdded();
    } catch (err) {
      console.error("Simulation error:", err);
    } finally {
      setLoading(false);
    }
  };

  const simulateMany = async () => {
    setLoading(true);
    try {
      for (let i = 0; i < 20; i++) {
        await axios.post("http://localhost:5000/api/predict", randomTransaction());
      }
      onTransactionAdded();
    } catch (err) {
      console.error("Simulation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <button className="simulate-btn" onClick={simulate} disabled={loading}>
        {loading ? "Processing..." : "⚡ Simulate Transaction"}
      </button>
      <button className="simulate-btn" onClick={simulateMany} disabled={loading}
        style={{ background: "#2d3748" }}>
        {loading ? "Processing..." : "🚀 Simulate 20 Transactions"}
      </button>
      <span className="simulate-note">Randomly generates transactions and runs them through the fraud model</span>
    </div>
  );
}

export default SimulateButton;
