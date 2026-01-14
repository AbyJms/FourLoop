from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, WasteRequest, WasteViolation

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ---------------- CONFIG ----------------
    app.config["SECRET_KEY"] = "change-this-secret-key"

    # ⚠️ Use PostgreSQL (update password accordingly)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hridya@172.17.105.182:5432/job_platform"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ---------------- EXTENSIONS ----------------
    db.init_app(app)
    CORS(app)

    login_manager = LoginManager()
    login_manager.login_view = "login_page"
    login_manager.init_app(app)

    @login_manager.user_loader
             def load_user(user_id):
              return User.query.get(int(user_id))

    # ---------------- API ROUTES ----------------

   @app.route("/register", methods=["POST"])
        def register():
            data = request.json
            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "User already exists"}), 400

            user = User(
                email=data["email"],
                role=data.get("role", "player"),
            )
            from werkzeug.security import generate_password_hash
            user.password_hash = generate_password_hash(data["password"])

            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User registered"}), 201


        @app.route("/login", methods=["POST"])
        def login():
            data = request.json
            user = User.query.filter_by(email=data["email"]).first()

            if not user or not check_password_hash(user.password_hash, data["password"]):
                return jsonify({"error": "Invalid credentials"}), 401

            login_user(user)
            return jsonify({"message": "Login successful"}), 200
