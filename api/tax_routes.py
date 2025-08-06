from flask import Blueprint, request, jsonify
from models.tax_record import tax_record_model
from utils.auth import auth_utils
import json

tax_bp = Blueprint('tax', __name__)

@tax_bp.route('/records', methods=['POST'])
def create_tax_record():
    """Create a new tax record"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['tax_year', 'income', 'tax_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Add user_id to the tax record
        data['user_id'] = payload['user_id']
        
        # Create tax record
        new_record = tax_record_model.create_tax_record(data)
        
        return jsonify({
            'message': 'Tax record created successfully',
            'record': new_record
        }), 201
        
    except Exception as e:
        print(f"Create tax record error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@tax_bp.route('/records', methods=['GET'])
def get_tax_records():
    """Get all tax records for the authenticated user"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get tax records for the user
        records = tax_record_model.get_tax_records_by_user(payload['user_id'])
        
        return jsonify({
            'records': records,
            'count': len(records)
        }), 200
        
    except Exception as e:
        print(f"Get tax records error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@tax_bp.route('/records/<record_id>', methods=['GET'])
def get_tax_record(record_id):
    """Get a specific tax record"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get tax record
        record = tax_record_model.get_tax_record_by_id(record_id)
        
        if not record:
            return jsonify({'error': 'Tax record not found'}), 404
        
        # Check if the record belongs to the authenticated user
        if record.get('user_id') != payload['user_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        return jsonify({'record': record}), 200
        
    except Exception as e:
        print(f"Get tax record error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@tax_bp.route('/records/<record_id>', methods=['PUT'])
def update_tax_record(record_id):
    """Update a tax record"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Check if record exists and belongs to user
        record = tax_record_model.get_tax_record_by_id(record_id)
        if not record:
            return jsonify({'error': 'Tax record not found'}), 404
        
        if record.get('user_id') != payload['user_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        # Remove fields that shouldn't be updated
        data.pop('user_id', None)
        data.pop('_id', None)
        data.pop('created_at', None)
        
        # Update tax record
        success = tax_record_model.update_tax_record(record_id, data)
        
        if success:
            updated_record = tax_record_model.get_tax_record_by_id(record_id)
            return jsonify({
                'message': 'Tax record updated successfully',
                'record': updated_record
            }), 200
        else:
            return jsonify({'error': 'Failed to update tax record'}), 500
        
    except Exception as e:
        print(f"Update tax record error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@tax_bp.route('/records/<record_id>', methods=['DELETE'])
def delete_tax_record(record_id):
    """Delete a tax record"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Check if record exists and belongs to user
        record = tax_record_model.get_tax_record_by_id(record_id)
        if not record:
            return jsonify({'error': 'Tax record not found'}), 404
        
        if record.get('user_id') != payload['user_id']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Delete tax record
        success = tax_record_model.delete_tax_record(record_id)
        
        if success:
            return jsonify({'message': 'Tax record deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete tax record'}), 500
        
    except Exception as e:
        print(f"Delete tax record error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@tax_bp.route('/calculate', methods=['POST'])
def calculate_tax():
    """Calculate tax based on income and other factors"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('income'):
            return jsonify({'error': 'Income is required'}), 400
        
        income = float(data['income'])
        tax_type = data.get('tax_type', 'federal')
        
        # Simple tax calculation (this is a basic example)
        # In a real application, you would implement proper tax brackets and calculations
        if tax_type == 'federal':
            if income <= 10275:
                tax = income * 0.10
            elif income <= 41775:
                tax = 1027.50 + (income - 10275) * 0.12
            elif income <= 89075:
                tax = 4807.50 + (income - 41775) * 0.22
            elif income <= 170050:
                tax = 15213.50 + (income - 89075) * 0.24
            elif income <= 215950:
                tax = 34647.50 + (income - 170050) * 0.32
            elif income <= 539900:
                tax = 49335.50 + (income - 215950) * 0.35
            else:
                tax = 162718 + (income - 539900) * 0.37
        else:
            # Default to 5% for other tax types
            tax = income * 0.05
        
        return jsonify({
            'income': income,
            'tax_type': tax_type,
            'calculated_tax': round(tax, 2),
            'effective_rate': round((tax / income) * 100, 2) if income > 0 else 0
        }), 200
        
    except Exception as e:
        print(f"Calculate tax error: {e}")
        return jsonify({'error': 'Internal server error'}), 500 