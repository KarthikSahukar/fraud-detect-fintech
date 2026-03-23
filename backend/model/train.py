import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, f1_score
import joblib
import os

print("Loading dataset...")
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "creditcard.csv"))

print(f"Dataset shape: {df.shape}")
print(f"Fraud cases: {df['Class'].sum()} / {len(df)} ({df['Class'].mean()*100:.2f}%)")

# ── Features ──
# Drop 'Time' (not useful), keep 'Amount' and all V1-V28 PCA features
features = [col for col in df.columns if col != 'Class']
X = df[features].copy()
y = df['Class'].copy()

# Scale 'Amount' — V1-V28 are already PCA scaled
scaler = StandardScaler()
X['Amount'] = scaler.fit_transform(X[['Amount']])
X['Time'] = scaler.fit_transform(X[['Time']])

print("\nTraining Isolation Forest...")
# contamination = fraud rate in dataset (~0.17%)
model = IsolationForest(
    n_estimators=200,
    contamination=0.0017,
    random_state=42,
    n_jobs=-1
)
model.fit(X)

# Isolation Forest returns -1 for anomaly, 1 for normal
# Convert to 1 for fraud, 0 for legit (matches dataset labels)
preds_raw = model.predict(X)
preds = np.where(preds_raw == -1, 1, 0)

print("\nModel Evaluation:")
print(classification_report(y, preds, target_names=["Legit", "Fraud"]))
f1 = f1_score(y, preds)
print(f"F1 Score (fraud class): {f1:.4f}")

# ── Save model and scaler ──
model_dir = os.path.dirname(__file__)
joblib.dump(model, os.path.join(model_dir, "fraud_model.pkl"))
joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))

# Save feature names for inference
joblib.dump(features, os.path.join(model_dir, "features.pkl"))

print("\nSaved: fraud_model.pkl, scaler.pkl, features.pkl")
print("Training complete!")