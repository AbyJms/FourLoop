<<<<<<< HEAD
<<<<<<< HEAD
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
=======
import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from models import db
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
=======
from flask import Flask, request, jsonify, session, render_template, redirect
from db import mysql, init_db
>>>>>>> 8ac7fcc27165ea9f44469c6e45197487dbc9ff35

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "trash-secret-key"

<<<<<<< HEAD
<<<<<<< HEAD
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
=======
def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*').split(',')}})
    jwt = JWTManager(app)
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(collections_bp, url_prefix='/api/collections')
    app.register_blueprint(store_bp, url_prefix='/api/store')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
    
    # Health check endpoint
    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'message': 'FourLoop API is running'}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'error': 'Authorization token is missing'}, 401
    
    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
=======
init_db(app)

# --------------------
# PAGES
# --------------------

@app.get("/")
def auth_page():
    return render_template("auth.html")

@app.get("/dashboard")
def dashboard_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.get("/mission")
def mission_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("mission.html")

@app.get("/profile")
def profile_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("profile.html")

@app.get("/store")
def store_page():
    if "uid" not in session:
        return redirect("/")
    return render_template("store.html")

@app.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})

# --------------------
# AUTH
# --------------------

@app.post("/register")
def register():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
        (data["username"], data["email"], data["password"]),
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"ok": True})

@app.post("/login")
def login():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (data["username"], data["password"]),
    )
    row = cur.fetchone()
    cur.close()

    if not row:
        return jsonify({"error": "Invalid credentials"}), 401

    session["uid"] = row[0]
    return jsonify({"ok": True})

# --------------------
# DATA API
# --------------------

def compute_rank(cur, total_points):
    cur.execute(
        "SELECT COUNT(*) + 1 FROM users WHERE total_points > %s",
        (total_points,),
    )
    return cur.fetchone()[0]

@app.get("/api/dashboard")
def dashboard_data():
    if "uid" not in session:
        return jsonify({"error": "Not logged in"}), 401

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT u.username, u.points, u.credits, u.total_points, t.name
        FROM users u
        LEFT JOIN titles t ON u.title_id = t.id
        WHERE u.id = %s
    """, (session["uid"],))
    u = cur.fetchone()

    rank = compute_rank(cur, u[3])

    # update best rank if needed
    cur.execute(
        "SELECT best_rank FROM users WHERE id=%s",
        (session["uid"],),
    )
    best = cur.fetchone()[0]

    if best is None or rank < best:
        cur.execute(
            "UPDATE users SET best_rank=%s WHERE id=%s",
            (rank, session["uid"]),
        )
        mysql.connection.commit()
        best = rank

    cur.execute("""
        SELECT username, total_points
        FROM users
        ORDER BY total_points DESC
        LIMIT 10
    """)
    leaderboard = cur.fetchall()

    cur.close()

    return jsonify({
        "user": {
            "username": u[0],
            "points": u[1],
            "credits": u[2],
            "total_points": u[3],
            "title": u[4],
            "rank": rank,
            "best_rank": best
        },
        "leaderboard": [
            {"username": r[0], "points": r[1]} for r in leaderboard
        ],
        "currentZone": "Crimson Wastefront",
        "boss": {"name": "Demo-garbage", "hp": 42}
    })

@app.get("/api/profile")
def profile_data():
    if "uid" not in session:
        return jsonify({"error": "Not logged in"}), 401

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT u.username, u.points, u.credits, u.total_points, t.name, u.best_rank
        FROM users u
        LEFT JOIN titles t ON u.title_id = t.id
        WHERE u.id = %s
    """, (session["uid"],))
    u = cur.fetchone()

    rank = compute_rank(cur, u[3])

    if u[5] is None or rank < u[5]:
        cur.execute(
            "UPDATE users SET best_rank=%s WHERE id=%s",
            (rank, session["uid"]),
        )
        mysql.connection.commit()
        best = rank
    else:
        best = u[5]

    cur.close()

    return jsonify({
        "username": u[0],
        "title": u[4],
        "points": u[1],
        "total_points": u[3],
        "credits": u[2],
        "rank": rank,
        "best_rank": best
    })

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 8ac7fcc27165ea9f44469c6e45197487dbc9ff35
