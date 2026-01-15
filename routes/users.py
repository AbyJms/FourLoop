from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, User
import os

users_bp = Blueprint('users', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID."""
    current_user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Include sensitive data only for own profile
    include_sensitive = (current_user_id == user_id)
    return jsonify({'user': user.to_dict(include_sensitive=include_sensitive)}), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    updateable_fields = ['full_name', 'phone', 'address', 'latitude', 'longitude']
    for field in updateable_fields:
        if field in data:
            setattr(user, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'details': str(e)}), 500

@users_bp.route('/profile/image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    """Upload profile image."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{user.id}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        user.profile_image = f'/uploads/{filename}'
        
        try:
            db.session.commit()
            return jsonify({
                'message': 'Profile image uploaded successfully',
                'image_url': user.profile_image
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to save image', 'details': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    from models import Collection, GarbageReport, Transaction
    
    if user.user_type == 'collector':
        total_collections = Collection.query.filter_by(collector_id=user.id).count()
        total_weight = db.session.query(db.func.sum(Collection.weight)).filter_by(
            collector_id=user.id
        ).scalar() or 0
        verified_collections = Collection.query.filter_by(
            collector_id=user.id, verified=True
        ).count()
        
        stats = {
            'total_collections': total_collections,
            'total_weight': float(total_weight),
            'verified_collections': verified_collections,
            'points': user.points
        }
    else:  # seeker
        total_reports = GarbageReport.query.filter_by(reporter_id=user.id).count()
        pending_reports = GarbageReport.query.filter_by(
            reporter_id=user.id, status='pending'
        ).count()
        collected_reports = GarbageReport.query.filter_by(
            reporter_id=user.id, status='collected'
        ).count()
        
        stats = {
            'total_reports': total_reports,
            'pending_reports': pending_reports,
            'collected_reports': collected_reports,
            'points': user.points
        }
    
    # Common stats
    total_transactions = Transaction.query.filter_by(user_id=user.id).count()
    total_redeemed = db.session.query(db.func.sum(Transaction.points)).filter_by(
        user_id=user.id, transaction_type='redeem'
    ).scalar() or 0
    
    stats.update({
        'total_transactions': total_transactions,
        'total_points_redeemed': abs(int(total_redeemed))
    })
    
    return jsonify({'stats': stats}), 200

@users_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    """Search users by username."""
    query = request.args.get('q', '')
    user_type = request.args.get('type', '')
    
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    users_query = User.query.filter(User.username.ilike(f'%{query}%'))
    
    if user_type in ['collector', 'seeker']:
        users_query = users_query.filter_by(user_type=user_type)
    
    users = users_query.limit(20).all()
    
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200