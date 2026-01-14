from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from models import db, User
from email_validator import validate_email, EmailNotValidError

auth_bp = Blueprint('auth', __name__)

# ---------------- REGISTER ----------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required = ['username', 'password', 'user_type']
    for f in required:
        if not data.get(f):
            return jsonify({'error': f'{f} is required'}), 400

    if data['user_type'] not in ['collector', 'seeker']:
        return jsonify({'error': 'Invalid user type'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409

    email = data.get('email')
    if email:
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409

    user = User(
        username=data['username'],
        email=email,
        user_type=data['user_type'],
        full_name=data.get('full_name'),
        phone=data.get('phone'),
        address=data.get('address'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )

    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'access_token': create_access_token(identity=str(user.id)),  # 🔥 FIX
        'refresh_token': create_refresh_token(identity=str(user.id)),  # 🔥 FIX
        'user': {
            'id': user.id,
            'username': user.username,
            'user_type': user.user_type
        }
    }), 201


# ---------------- LOGIN ----------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'access_token': create_access_token(identity=str(user.id)),  # 🔥 FIX
        'refresh_token': create_refresh_token(identity=str(user.id)),  # 🔥 FIX
        'user': {
            'id': user.id,
            'username': user.username,
            'user_type': user.user_type
        }
    }), 200


# ---------------- ME ----------------
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())  # 🔥 CAST BACK
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'user_type': user.user_type,
        'points': user.points
    }), 200


# ---------------- REFRESH ----------------
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return jsonify({
        'access_token': create_access_token(identity=get_jwt_identity())
    }), 200


# ---------------- CHANGE PASSWORD ----------------
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Both passwords required'}), 400

    if not user.check_password(data['old_password']):
        return jsonify({'error': 'Wrong old password'}), 401

    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify({'message': 'Password updated'}), 200
