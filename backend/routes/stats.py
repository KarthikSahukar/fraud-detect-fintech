from flask import Blueprint, jsonify
from database import get_db, Transaction
from sqlalchemy import func

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    db = next(get_db())

    total = db.query(Transaction).count()
    fraud_count = db.query(Transaction).filter(Transaction.is_fraud == True).count()
    legit_count = total - fraud_count

    avg_fraud_amount = db.query(func.avg(Transaction.amount)).filter(
        Transaction.is_fraud == True
    ).scalar() or 0

    avg_legit_amount = db.query(func.avg(Transaction.amount)).filter(
        Transaction.is_fraud == False
    ).scalar() or 0

    # Fraud by location
    by_location = db.query(
        Transaction.location,
        func.count(Transaction.id).label("count")
    ).filter(Transaction.is_fraud == True).group_by(Transaction.location).all()

    return jsonify({
        "total_transactions": total,
        "fraud_count": fraud_count,
        "legit_count": legit_count,
        "fraud_rate": round((fraud_count / total * 100), 2) if total > 0 else 0,
        "avg_fraud_amount": round(float(avg_fraud_amount), 2),
        "avg_legit_amount": round(float(avg_legit_amount), 2),
        "fraud_by_location": [{"location": r[0], "count": r[1]} for r in by_location]
    }), 200