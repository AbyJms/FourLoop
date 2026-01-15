from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, StoreItem, User, Transaction
from datetime import datetime
import os

store_bp = Blueprint('store', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@store_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    """Get all store items."""
    category = request.args.get('category')
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = StoreItem.query
    
    if category:
        query = query.filter_by(category=category)
    if is_active:
        query = query.filter_by(is_active=True)
    
    query = query.order_by(StoreItem.points_cost.asc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@store_bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    """Get a specific store item."""
    item = StoreItem.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    return jsonify({'item': item.to_dict()}), 200

@store_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    """Create a new store item (admin only for now)."""
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    # Validate required fields
    if not data.get('name') or not data.get('points_cost'):
        return jsonify({'error': 'Name and points cost are required'}), 400
    
    # Handle image upload if present
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"item_{datetime.utcnow().timestamp()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f'/uploads/{filename}'
    
    # Create item
    item = StoreItem(
        name=data['name'],
        description=data.get('description'),
        category=data.get('category', 'product'),
        points_cost=int(data['points_cost']),
        image_url=image_url or data.get('image_url'),
        stock=int(data.get('stock', 0)),
        is_active=data.get('is_active', True)
    )
    
    try:
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item created successfully',
            'item': item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create item', 'details': str(e)}), 500

@store_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """Update a store item (admin only for now)."""
    item = StoreItem.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.get_json()
    
    # Update allowed fields
    updateable_fields = ['name', 'description', 'category', 'points_cost', 
                        'image_url', 'stock', 'is_active']
    for field in updateable_fields:
        if field in data:
            setattr(item, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Item updated successfully',
            'item': item.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update item', 'details': str(e)}), 500

@store_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """Delete a store item (admin only for now)."""
    item = StoreItem.query.get(item_id)
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete item', 'details': str(e)}), 500

@store_bp.route('/redeem/<int:item_id>', methods=['POST'])
@jwt_required()
def redeem_item(item_id):
    """Redeem a store item with points."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    item = StoreItem.query.get(item_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    if not item.is_active:
        return jsonify({'error': 'Item is not available'}), 400
    
    if item.stock <= 0:
        return jsonify({'error': 'Item is out of stock'}), 400
    
    if user.points < item.points_cost:
        return jsonify({'error': 'Insufficient points'}), 400
    
    # Deduct points
    user.points -= item.points_cost
    
    # Reduce stock
    item.stock -= 1
    
    # Create transaction
    transaction = Transaction(
        user_id=current_user_id,
        transaction_type='redeem',
        points=-item.points_cost,
        description=f'Redeemed: {item.name}',
        item_id=item_id
    )
    
    try:
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Item redeemed successfully',
            'transaction': transaction.to_dict(),
            'remaining_points': user.points
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to redeem item', 'details': str(e)}), 500

@store_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get user transactions."""
    current_user_id = get_jwt_identity()
    transaction_type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Transaction.query.filter_by(user_id=current_user_id)
    
    if transaction_type in ['earn', 'redeem']:
        query = query.filter_by(transaction_type=transaction_type)
    
    query = query.order_by(Transaction.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'transactions': [transaction.to_dict() for transaction in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@store_bp.route('/my-redemptions', methods=['GET'])
@jwt_required()
def get_my_redemptions():
    """Get user's redemption history."""
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Transaction.query.filter_by(
        user_id=current_user_id,
        transaction_type='redeem'
    ).order_by(Transaction.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'redemptions': [transaction.to_dict() for transaction in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200