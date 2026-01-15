from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Collection, User, Transaction, Leaderboard
from datetime import datetime
import os

collections_bp = Blueprint('collections', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@collections_bp.route('', methods=['POST'])
@jwt_required()
def create_collection():
    """Create a new collection entry."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.user_type != 'collector':
        return jsonify({'error': 'Only collectors can create collections'}), 403
    
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    # Validate required fields
    if not data.get('waste_type') or not data.get('weight'):
        return jsonify({'error': 'Waste type and weight are required'}), 400
    
    weight = float(data['weight'])
    
    # Calculate points
    points_per_kg = current_app.config.get('POINTS_PER_KG', 10)
    points_earned = int(weight * points_per_kg)
    
    # Handle image upload if present
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"collection_{datetime.utcnow().timestamp()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f'/uploads/{filename}'
    
    # Create collection
    collection = Collection(
        collector_id=current_user_id,
        report_id=data.get('report_id'),
        waste_type=data['waste_type'],
        weight=weight,
        points_earned=points_earned,
        location=data.get('location'),
        latitude=float(data['latitude']) if data.get('latitude') else None,
        longitude=float(data['longitude']) if data.get('longitude') else None,
        image_url=image_url or data.get('image_url'),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(collection)
        
        # Update user points
        user.points += points_earned
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user_id,
            transaction_type='earn',
            points=points_earned,
            description=f'Collected {weight}kg of {data["waste_type"]}',
            collection_id=collection.id
        )
        db.session.add(transaction)
        
        # Update leaderboard
        update_leaderboard(current_user_id, weight, points_earned)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Collection created successfully',
            'collection': collection.to_dict(),
            'points_earned': points_earned
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create collection', 'details': str(e)}), 500

def update_leaderboard(user_id, weight, points):
    """Update leaderboard entry for user."""
    entry = Leaderboard.query.filter_by(user_id=user_id).first()
    
    if not entry:
        entry = Leaderboard(user_id=user_id)
        db.session.add(entry)
    
    entry.total_collections += 1
    entry.total_weight += weight
    entry.total_points += points
    
    # Update ranks (simple implementation)
    all_entries = Leaderboard.query.order_by(Leaderboard.total_points.desc()).all()
    for idx, e in enumerate(all_entries, 1):
        e.rank = idx

@collections_bp.route('', methods=['GET'])
@jwt_required()
def get_collections():
    """Get collections with filters."""
    waste_type = request.args.get('waste_type')
    verified = request.args.get('verified')
    my_collections = request.args.get('my_collections', 'false').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    current_user_id = get_jwt_identity()
    
    query = Collection.query
    
    if waste_type:
        query = query.filter_by(waste_type=waste_type)
    if verified is not None:
        query = query.filter_by(verified=verified.lower() == 'true')
    if my_collections:
        query = query.filter_by(collector_id=current_user_id)
    
    query = query.order_by(Collection.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'collections': [collection.to_dict() for collection in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@collections_bp.route('/<int:collection_id>', methods=['GET'])
@jwt_required()
def get_collection(collection_id):
    """Get a specific collection."""
    collection = Collection.query.get(collection_id)
    
    if not collection:
        return jsonify({'error': 'Collection not found'}), 404
    
    return jsonify({'collection': collection.to_dict()}), 200

@collections_bp.route('/<int:collection_id>', methods=['PUT'])
@jwt_required()
def update_collection(collection_id):
    """Update a collection."""
    current_user_id = get_jwt_identity()
    collection = Collection.query.get(collection_id)
    
    if not collection:
        return jsonify({'error': 'Collection not found'}), 404
    
    # Only the collector can update their own collection
    if collection.collector_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    updateable_fields = ['notes', 'location', 'latitude', 'longitude']
    for field in updateable_fields:
        if field in data:
            setattr(collection, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Collection updated successfully',
            'collection': collection.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update collection', 'details': str(e)}), 500

@collections_bp.route('/<int:collection_id>/verify', methods=['POST'])
@jwt_required()
def verify_collection(collection_id):
    """Verify a collection (admin only - for now any user can verify)."""
    collection = Collection.query.get(collection_id)
    
    if not collection:
        return jsonify({'error': 'Collection not found'}), 404
    
    collection.verified = True
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Collection verified successfully',
            'collection': collection.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to verify collection', 'details': str(e)}), 500

@collections_bp.route('/<int:collection_id>', methods=['DELETE'])
@jwt_required()
def delete_collection(collection_id):
    """Delete a collection."""
    current_user_id = get_jwt_identity()
    collection = Collection.query.get(collection_id)
    
    if not collection:
        return jsonify({'error': 'Collection not found'}), 404
    
    if collection.collector_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Refund points
    user = User.query.get(current_user_id)
    user.points -= collection.points_earned
    
    # Update leaderboard
    entry = Leaderboard.query.filter_by(user_id=current_user_id).first()
    if entry:
        entry.total_collections -= 1
        entry.total_weight -= collection.weight
        entry.total_points -= collection.points_earned
    
    try:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({'message': 'Collection deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete collection', 'details': str(e)}), 500

@collections_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_collection_stats():
    """Get collection statistics."""
    # Overall stats
    total_collections = Collection.query.count()
    total_weight = db.session.query(db.func.sum(Collection.weight)).scalar() or 0
    verified_collections = Collection.query.filter_by(verified=True).count()
    
    # Waste type breakdown
    waste_stats = db.session.query(
        Collection.waste_type,
        db.func.count(Collection.id).label('count'),
        db.func.sum(Collection.weight).label('total_weight')
    ).group_by(Collection.waste_type).all()
    
    waste_breakdown = [
        {
            'waste_type': stat[0],
            'count': stat[1],
            'total_weight': float(stat[2] or 0)
        }
        for stat in waste_stats
    ]
    
    return jsonify({
        'total_collections': total_collections,
        'total_weight': float(total_weight),
        'verified_collections': verified_collections,
        'waste_breakdown': waste_breakdown
    }), 200