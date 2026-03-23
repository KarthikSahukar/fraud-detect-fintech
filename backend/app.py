from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.transactions import transactions_bp
from routes.stats import stats_bp

app = Flask(__name__)
CORS(app)  # allows React frontend to call this API

# Register blueprints
app.register_blueprint(transactions_bp, url_prefix="/api")
app.register_blueprint(stats_bp, url_prefix="/api")

# Initialize DB tables on startup
with app.app_context():
    init_db()

@app.route("/")
def health():
    return {"status": "Fraud Detection API is running"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)