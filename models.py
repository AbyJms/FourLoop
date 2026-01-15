from datetime import datetime
<<<<<<< HEAD
from flask_login import UserMixin
=======
from werkzeug.security import generate_password_hash, check_password_hash
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

<<<<<<< HEAD
class User(db.Model, UserMixin):
    __tablename__ = "users"

=======
class User(db.Model):
    __tablename__ = 'users'
    
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
<<<<<<< HEAD

    # NEW
    role = db.Column(db.String(20), nullable=False, default="player")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
=======
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_type = db.Column(db.String(20), nullable=False)  # 'collector', 'seeker'
    points = db.Column(db.Integer, default=0)
    profile_image = db.Column(db.String(255))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    collections = db.relationship('Collection', backref='collector', lazy='dynamic', foreign_keys='Collection.collector_id')
    reports = db.relationship('GarbageReport', backref='reporter', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    
    def set_password(self, password):
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'email': self.email if include_sensitive else None,
            'username': self.username,
            'full_name': self.full_name,
            'phone': self.phone if include_sensitive else None,
            'address': self.address if include_sensitive else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_type': self.user_type,
            'points': self.points,
            'profile_image': self.profile_image,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        return {k: v for k, v in data.items() if v is not None or include_sensitive}

<<<<<<< HEAD
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
=======
class GarbageReport(db.Model):
    __tablename__ = 'garbage_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    waste_type = db.Column(db.String(50))  # 'plastic', 'paper', 'metal', 'organic', 'electronic', 'mixed'
    estimated_weight = db.Column(db.Float)  # in kg
    status = db.Column(db.String(20), default='pending')  # 'pending', 'assigned', 'collected', 'cancelled'
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    collected_at = db.Column(db.DateTime)
    
    # Relationship to assigned collector
    collector = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_reports')
    
    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'reporter_username': self.reporter.username if self.reporter else None,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'waste_type': self.waste_type,
            'estimated_weight': self.estimated_weight,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'collector_username': self.collector.username if self.collector else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'collected_at': self.collected_at.isoformat() if self.collected_at else None
        }

class Collection(db.Model):
    __tablename__ = 'collections'
    
    id = db.Column(db.Integer, primary_key=True)
    collector_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('garbage_reports.id'))
    waste_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # in kg
    points_earned = db.Column(db.Integer, default=0)
    location = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    image_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    report = db.relationship('GarbageReport', backref='collections')
    
    def to_dict(self):
        return {
            'id': self.id,
            'collector_id': self.collector_id,
            'collector_username': self.collector.username if self.collector else None,
            'report_id': self.report_id,
            'waste_type': self.waste_type,
            'weight': self.weight,
            'points_earned': self.points_earned,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'notes': self.notes,
            'verified': self.verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StoreItem(db.Model):
    __tablename__ = 'store_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # 'voucher', 'product', 'donation'
    points_cost = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    stock = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'points_cost': self.points_cost,
            'image_url': self.image_url,
            'stock': self.stock,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'earn', 'redeem'
    points = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    item_id = db.Column(db.Integer, db.ForeignKey('store_items.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    item = db.relationship('StoreItem', backref='transactions')
    collection = db.relationship('Collection', backref='transactions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'points': self.points,
            'description': self.description,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'collection_id': self.collection_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    total_collections = db.Column(db.Integer, default=0)
    total_weight = db.Column(db.Float, default=0.0)
    total_points = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='leaderboard_entry')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'profile_image': self.user.profile_image if self.user else None,
            'total_collections': self.total_collections,
            'total_weight': self.total_weight,
            'total_points': self.total_points,
            'rank': self.rank,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
>>>>>>> 04da2d01ffe9acadffbb6189fda4a30b9b647ac9
