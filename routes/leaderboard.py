from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Leaderboard, User
from sqlalchemy import desc

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """Get leaderboard rankings."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    sort_by = request.args.get('sort_by', 'points')  # 'points', 'weight', 'collections'
    
    # Determine sort field
    if sort_by == 'weight':
        sort_field = Leaderboard.total_weight
    elif sort_by == 'collections':
        sort_field = Leaderboard.total_collections
    else:
        sort_field = Leaderboard.total_points
    
    query = Leaderboard.query.order_by(desc(sort_field))
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'leaderboard': [entry.to_dict() for entry in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@leaderboard_bp.route('/my-rank', methods=['GET'])
@jwt_required()
def get_my_rank():
    """Get current user's rank and stats."""
    current_user_id = get_jwt_identity()
    
    entry = Leaderboard.query.filter_by(user_id=current_user_id).first()
    
    if not entry:
        # Create entry if doesn't exist
        entry = Leaderboard(user_id=current_user_id)
        db.session.add(entry)
        db.session.commit()
    
    return jsonify({'rank_info': entry.to_dict()}), 200

@leaderboard_bp.route('/top/<int:count>', methods=['GET'])
@jwt_required()
def get_top_users(count):
    """Get top N users."""
    if count > 100:
        count = 100  # Limit to 100
    
    sort_by = request.args.get('sort_by', 'points')
    
    if sort_by == 'weight':
        sort_field = Leaderboard.total_weight
    elif sort_by == 'collections':
        sort_field = Leaderboard.total_collections
    else:
        sort_field = Leaderboard.total_points
    
    entries = Leaderboard.query.order_by(desc(sort_field)).limit(count).all()
    
    return jsonify({
        'top_users': [entry.to_dict() for entry in entries]
    }), 200

@leaderboard_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_leaderboard():
    """Refresh leaderboard rankings (admin function)."""
    from models import Collection
    
    # Get all users with collections
    users_with_collections = db.session.query(
        Collection.collector_id,
        db.func.count(Collection.id).label('total_collections'),
        db.func.sum(Collection.weight).label('total_weight'),
        db.func.sum(Collection.points_earned).label('total_points')
    ).group_by(Collection.collector_id).all()
    
    # Update or create leaderboard entries
    for user_data in users_with_collections:
        entry = Leaderboard.query.filter_by(user_id=user_data.collector_id).first()
        
        if not entry:
            entry = Leaderboard(user_id=user_data.collector_id)
            db.session.add(entry)
        
        entry.total_collections = user_data.total_collections
        entry.total_weight = float(user_data.total_weight or 0)
        entry.total_points = int(user_data.total_points or 0)
    
    # Update ranks
    all_entries = Leaderboard.query.order_by(desc(Leaderboard.total_points)).all()
    for idx, entry in enumerate(all_entries, 1):
        entry.rank = idx
    
    try:
        db.session.commit()
        return jsonify({'message': 'Leaderboard refreshed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to refresh leaderboard', 'details': str(e)}), 500

@leaderboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_leaderboard_stats():
    """Get overall leaderboard statistics."""
    total_users = Leaderboard.query.count()
    total_collections = db.session.query(
        db.func.sum(Leaderboard.total_collections)
    ).scalar() or 0
    total_weight = db.session.query(
        db.func.sum(Leaderboard.total_weight)
    ).scalar() or 0
    total_points = db.session.query(
        db.func.sum(Leaderboard.total_points)
    ).scalar() or 0
    
    return jsonify({
        'total_users': total_users,
        'total_collections': int(total_collections),
        'total_weight': float(total_weight),
        'total_points': int(total_points)
    }), 200