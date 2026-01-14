from datetime import datetime
<<<<<<< HEAD
from werkzeug.security import generate_password_hash, check_password_hash
=======
from flask_login import UserMixin
>>>>>>> origin/main
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

<<<<<<< HEAD

class User(db.Model):
=======
class User(db.Model, UserMixin):
>>>>>>> origin/main
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_type = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ EXPLICIT RELATIONSHIPS (NO AMBIGUITY)
    reports_created = db.relationship(
        "GarbageReport",
        foreign_keys="GarbageReport.reporter_id",
        backref="reporter",
        lazy="dynamic"
    )

    reports_assigned = db.relationship(
        "GarbageReport",
        foreign_keys="GarbageReport.assigned_to",
        backref="collector",
        lazy="dynamic"
    )

    collections = db.relationship(
        "Collection",
        foreign_keys="Collection.collector_id",
        backref="collector",
        lazy="dynamic"
    )

    transactions = db.relationship("Transaction", backref="user", lazy="dynamic")

    leaderboard_entry = db.relationship(
        "Leaderboard",
        backref="user",
        uselist=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

<<<<<<< HEAD
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GarbageReport(db.Model):
    __tablename__ = "garbage_reports"

    id = db.Column(db.Integer, primary_key=True)

    reporter_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    assigned_to = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    waste_type = db.Column(db.String(50))
    estimated_weight = db.Column(db.Float)
    status = db.Column(db.String(20), default="pending")
    priority = db.Column(db.String(20), default="medium")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    collected_at = db.Column(db.DateTime)


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)

    collector_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    report_id = db.Column(
        db.Integer, db.ForeignKey("garbage_reports.id")
    )

    waste_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    points_earned = db.Column(db.Integer, default=0)
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    report = db.relationship("GarbageReport", backref="collections")


class StoreItem(db.Model):
    __tablename__ = "store_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    points_cost = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    item_id = db.Column(db.Integer, db.ForeignKey("store_items.id"))
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    item = db.relationship("StoreItem", backref="transactions")
    collection = db.relationship("Collection", backref="transactions")


class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True
    )
    total_collections = db.Column(db.Integer, default=0)
    total_weight = db.Column(db.Float, default=0.0)
    total_points = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
=======
    def check_password(self, password: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)


class WasteRequest(db.Model):
    __tablename__ = "waste_requests"

    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    waste_type = db.Column(db.String(20), nullable=False)  # food | plastic | mixed
    status = db.Column(db.String(20), default="pending")  # pending | accepted | completed | flagged
    assigned_harithakarmasena_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WasteViolation(db.Model):
    __tablename__ = "waste_violations"

    id = db.Column(db.Integer, primary_key=True)
    home_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey("waste_requests.id"))
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
>>>>>>> origin/main
