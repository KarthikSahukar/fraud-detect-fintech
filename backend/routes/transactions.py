from flask import Blueprint, request, jsonify
from database import get_db, Transaction
from datetime import datetime
import joblib
import numpy as np
import os
import random

transactions_bp = Blueprint("transactions", __name__)

# Load model, scaler, features once at startup
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../model")
model = joblib.load(os.path.join(MODEL_DIR, "fraud_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
features = joblib.load(os.path.join(MODEL_DIR, "features.pkl"))

MERCHANTS = ["Amazon", "Walmart", "Shell Gas", "Starbucks", "Apple Store",
             "Netflix", "Uber", "Zomato", "Flipkart", "BookMyShow"]
LOCATIONS = ["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai",
             "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Surat"]


@transactions_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Expect: { "amount": 150.0, "features": [v1, v2, ..., v28] }
    if not data or "amount" not in data or "features" not in data:
        return jsonify({"error": "Provide amount and features (V1-V28)"}), 400

    if len(data["features"]) != 28:
        return jsonify({"error": "Exactly 28 features (V1-V28) required"}), 400

    try:
        amount = float(data["amount"])
        v_features = data["features"]

        # Build feature array in same order as training
        time_val = float(data.get("time", 50000))  # default mid-range time
        scaled_amount = scaler.transform([[amount]])[0][0]
        scaled_time = float(time_val / 172792)  # normalize by max time in dataset

        feature_array = np.array([[scaled_time] + v_features + [scaled_amount]])

        # Predict — Isolation Forest: -1 = anomaly (fraud), 1 = normal
        raw_pred = model.predict(feature_array)[0]
        anomaly_score = model.decision_function(feature_array)[0]

        # Convert: -1 → fraud (1), 1 → legit (0)
        is_fraud = bool(raw_pred == -1)

        # Normalize score to 0-1 range (higher = more suspicious)
        fraud_score = round(float(1 - (anomaly_score + 0.5)), 4)
        fraud_score = max(0.0, min(1.0, fraud_score))

        # Save to DB
        db = next(get_db())
        transaction = Transaction(
            amount=amount,
            is_fraud=is_fraud,
            fraud_score=fraud_score,
            merchant=random.choice(MERCHANTS),
            location=random.choice(LOCATIONS),
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return jsonify({
            "id": transaction.id,
            "amount": amount,
            "is_fraud": is_fraud,
            "fraud_score": fraud_score,
            "merchant": transaction.merchant,
            "location": transaction.location,
            "timestamp": transaction.timestamp.isoformat(),
            "message": "⚠️ FRAUD DETECTED" if is_fraud else "✅ Legitimate transaction"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@transactions_bp.route("/transactions", methods=["GET"])
def get_transactions():
    db = next(get_db())
    limit = request.args.get("limit", 50, type=int)
    transactions = db.query(Transaction).order_by(
        Transaction.timestamp.desc()
    ).limit(limit).all()

    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "is_fraud": t.is_fraud,
        "fraud_score": t.fraud_score,
        "merchant": t.merchant,
        "location": t.location,
        "timestamp": t.timestamp.isoformat()
    } for t in transactions]), 200