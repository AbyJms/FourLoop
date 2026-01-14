from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, GarbageReport, User, Transaction
from datetime import datetime
import os

reports_bp = Blueprint('reports', __name__)

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@reports_bp.route('', methods=['POST'])
@jwt_required()
def create_report():
    """Create a new garbage report."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    # Validate required fields
    required_fields = ['title', 'location', 'latitude', 'longitude']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Handle image upload if present
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"report_{datetime.utcnow().timestamp()}_{file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f'/uploads/{filename}'
    
    # Create report
    report = GarbageReport(
        reporter_id=current_user_id,
        title=data['title'],
        description=data.get('description'),
        location=data['location'],
        latitude=float(data['latitude']),
        longitude=float(data['longitude']),
        image_url=image_url or data.get('image_url'),
        waste_type=data.get('waste_type', 'mixed'),
        estimated_weight=float(data['estimated_weight']) if data.get('estimated_weight') else None,
        priority=data.get('priority', 'medium')
    )
    
    try:
        db.session.add(report)
        
        # Award points for reporting
        user.points += current_app.config.get('POINTS_FOR_REPORT', 5)
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user_id,
            transaction_type='earn',
            points=current_app.config.get('POINTS_FOR_REPORT', 5),
            description=f'Reported: {report.title}'
        )
        db.session.add(transaction)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Report created successfully',
            'report': report.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create report', 'details': str(e)}), 500

@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    """Get all reports with filters."""
    status = request.args.get('status')
    waste_type = request.args.get('waste_type')
    priority = request.args.get('priority')
    assigned_to_me = request.args.get('assigned_to_me', 'false').lower() == 'true'
    my_reports = request.args.get('my_reports', 'false').lower() == 'true'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    current_user_id = get_jwt_identity()
    
    query = GarbageReport.query
    
    if status:
        query = query.filter_by(status=status)
    if waste_type:
        query = query.filter_by(waste_type=waste_type)
    if priority:
        query = query.filter_by(priority=priority)
    if assigned_to_me:
        query = query.filter_by(assigned_to=current_user_id)
    if my_reports:
        query = query.filter_by(reporter_id=current_user_id)
    
    query = query.order_by(GarbageReport.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'reports': [report.to_dict() for report in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@reports_bp.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """Get a specific report."""
    report = GarbageReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify({'report': report.to_dict()}), 200

@reports_bp.route('/<int:report_id>', methods=['PUT'])
@jwt_required()
def update_report(report_id):
    """Update a report."""
    current_user_id = get_jwt_identity()
    report = GarbageReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    # Only reporter can update their own report
    if report.reporter_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update allowed fields
    updateable_fields = ['title', 'description', 'location', 'latitude', 'longitude', 
                        'waste_type', 'estimated_weight', 'priority']
    for field in updateable_fields:
        if field in data:
            setattr(report, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Report updated successfully',
            'report': report.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update report', 'details': str(e)}), 500

@reports_bp.route('/<int:report_id>/assign', methods=['POST'])
@jwt_required()
def assign_report(report_id):
    """Assign report to a collector."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    report = GarbageReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    if user.user_type != 'collector':
        return jsonify({'error': 'Only collectors can accept reports'}), 403
    
    if report.status != 'pending':
        return jsonify({'error': 'Report is not available'}), 400
    
    report.assigned_to = current_user_id
    report.status = 'assigned'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Report assigned successfully',
            'report': report.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to assign report', 'details': str(e)}), 500

@reports_bp.route('/<int:report_id>/complete', methods=['POST'])
@jwt_required()
def complete_report(report_id):
    """Mark report as collected."""
    current_user_id = get_jwt_identity()
    report = GarbageReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    if report.assigned_to != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    report.status = 'collected'
    report.collected_at = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Report marked as collected',
            'report': report.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to complete report', 'details': str(e)}), 500

@reports_bp.route('/<int:report_id>', methods=['DELETE'])
@jwt_required()
def delete_report(report_id):
    """Delete a report."""
    current_user_id = get_jwt_identity()
    report = GarbageReport.query.get(report_id)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    if report.reporter_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(report)
        db.session.commit()
        return jsonify({'message': 'Report deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete report', 'details': str(e)}), 500

@reports_bp.route('/nearby', methods=['GET'])
@jwt_required()
def get_nearby_reports():
    """Get nearby reports based on location."""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius = request.args.get('radius', 10, type=float)  # km
    status = request.args.get('status', 'pending')
    
    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and longitude are required'}), 400
    
    # Simple distance calculation (approximate)
    # For production, consider using PostGIS
    reports = GarbageReport.query.filter_by(status=status).all()
    
    nearby_reports = []
    for report in reports:
        # Approximate distance calculation
        lat_diff = abs(report.latitude - latitude)
        lon_diff = abs(report.longitude - longitude)
        distance = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111  # rough conversion to km
        
        if distance <= radius:
            report_dict = report.to_dict()
            report_dict['distance'] = round(distance, 2)
            nearby_reports.append(report_dict)
    
    # Sort by distance
    nearby_reports.sort(key=lambda x: x['distance'])
    
    return jsonify({'reports': nearby_reports}), 200