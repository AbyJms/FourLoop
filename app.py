from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user
from models import db, User

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config
    app.config["SECRET_KEY"] = "change-this-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init extensions
    db.init_app(app)
    CORS(app)

    login_manager = LoginManager()
    login_manager.login_view = "home"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---------------- AUTH API ----------------

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
        return jsonify({"message": "Login successful"}), 200

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Logged out"}), 200

    # ---------------- HTML PAGES ----------------

    @app.route("/")
    def home():
        return render_template("auth.html")

    @app.route("/dashboard-page")
    @login_required
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/mission-page")
    @login_required
    def mission_page():
        return render_template("mission.html")

    @app.route("/profile-page")
    @login_required
    def profile_page():
        return render_template("profile.html")

    @app.route("/store-page")
    @login_required
    def store_page():
        return render_template("store.html")

    @app.route("/seeker/post")
    @login_required
    def seeker_post():
        return render_template("seeker_post.html")

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
