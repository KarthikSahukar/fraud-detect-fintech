import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#68d391", "#fc8181"];

function StatsChart({ stats }) {
  if (!stats || stats.total_transactions === 0)
    return <p className="empty">No data yet.</p>;

  const pieData = [
    { name: "Legitimate", value: stats.legit_count },
    { name: "Fraud", value: stats.fraud_count },
  ];

  return (
    <div>
      <div className="stats-grid">
        <div className="stat-box">
          <div className="val">{stats.total_transactions}</div>
          <div className="lbl">Total Transactions</div>
        </div>
        <div className="stat-box">
          <div className="val" style={{ color: "#fc8181" }}>{stats.fraud_count}</div>
          <div className="lbl">Fraud Detected</div>
        </div>
        <div className="stat-box">
          <div className="val">₹{stats.avg_fraud_amount}</div>
          <div className="lbl">Avg Fraud Amount</div>
        </div>
        <div className="stat-box">
          <div className="val" style={{ color: "#68d391" }}>{stats.fraud_rate}%</div>
          <div className="lbl">Fraud Rate</div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={180}>
        <PieChart>
          <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80}
            paddingAngle={4} dataKey="value">
            {pieData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
          </Pie>
          <Tooltip
            contentStyle={{ background: "#1a1d27", border: "1px solid #2d3748", borderRadius: 8 }}
            labelStyle={{ color: "#e2e8f0" }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default StatsChart;
