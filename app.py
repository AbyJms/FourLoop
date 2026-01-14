from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def create_app():
    # serve HTML files that live in the repo root (e.g. auth.html, dashboard.html)
    # and make root URLs (e.g. `/style.css`) resolve to project files during dev.
    app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")

    # Core configuration
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    # Enable CORS for all routes
    CORS(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ------------------ API ROUTES ------------------

    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already exists"}), 400

        user = User(email=data["email"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"error": "Invalid credentials"}), 401

        login_user(user)
        return jsonify({"message": "Login successful", "email": user.email}), 200

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200

    @app.route("/dashboard", methods=["GET"])
    @login_required
    def dashboard():
        return jsonify({
            "currentZone": "Crimson Wastefront",
            "boss": {"name": "Queen of Plastics", "hp": 42},
            "mainQuests": [
                "Clear 3 hotspot alleys of plastic waste",
                "Coordinate a 10-member clean-up squad",
                "Secure recycling drop-points in 2 zones"
            ],
            "sideQuests": [
                "Photo-document the weirdest litter artifact",
                "Design a meme to recruit new players",
                "Map an undocumented dumping spot"
            ],
            "party": [
                {"name": "EchoRanger", "role": "Squad Lead", "status": "Online"},
                {"name": "NeonRecycler", "role": "Scout", "status": "In Run"},
                {"name": "GlassKnight", "role": "Heavy Lifter", "status": "Offline"},
            ],
            "leaderboard": {
                "zonal": [
                    {"team": "Crimson Sweepers", "score": 12340},
                    {"team": "Neon Nomads", "score": 11980},
                    {"team": "Waste Warriors", "score": 10420},
                ],
                "national": [
                    {"team": "Empire of Clean", "score": 120450},
                    {"team": "Redline Reclaimers", "score": 118900},
                    {"team": "ZeroWaste Union", "score": 115320},
                ]
            },
            "rewards": {
                "tierProgress": 65,
                "tokens": 3250,
                "redeemed": 7,
                "nextMilestone": "Legendary Badge"
            }
        })

    # Serve a default frontend page at root to avoid 404 on '/'.
    @app.route("/")
    def index():
        # default to the auth page; change to 'dashboard.html' if you prefer
        return app.send_static_file("auth.html")

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # creates database.db if it doesn’t exist
    app.run(debug=True)
