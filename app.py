from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

# ---------------- APP SETUP ----------------
app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ---------------- CONFIG ----------------
app.config["SECRET_KEY"] = "dev-secret-key"  # dev only
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:AibinJames%402006@localhost:3307/testdash"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class User(db.Model):
    __tablename__ = "user"  # YOU wanted singular — DONE

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="player")  # player | seeker | admin
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()

# ---------------- STATIC FILE SERVING ----------------
@app.route("/")
def root():
    return send_from_directory(".", "auth.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# ---------------- DEBUG ----------------
@app.route("/api/debug/users")
def debug_users():
    users = User.query.all()
    return jsonify({
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "role": u.role
            } for u in users
        ]
    })

# ---------------- AUTH ----------------
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "player")

    if not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered successfully"}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "email": user.email,
        "role": user.role
    }), 200

# ---------------- HEALTH ----------------
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "FourLoop API is running"
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
