from flask import Blueprint, request, jsonify
from models.admin import admin_model
from utils.auth import auth_utils
import json

admin_auth_bp = Blueprint('admin_auth', __name__)

@admin_auth_bp.route('/register', methods=['POST'])
def register_admin():
    """Register a new admin (restricted access)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['employee_id', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if admin already exists
        existing_admin = admin_model.get_admin_by_employee_id(data['employee_id'])
        if existing_admin:
            return jsonify({'error': 'Admin with this employee ID already exists'}), 409
        
        # Create admin
        admin_data = {
            'employee_id': data['employee_id'].upper(),
            'password': data['password'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'department': data.get('department', ''),
            'designation': data.get('designation', ''),
            'address': data.get('address', {}),
            'permissions': data.get('permissions', [])
        }
        
        new_admin = admin_model.create_admin(admin_data)
        
        # Generate token
        token = auth_utils.generate_token(new_admin)
        
        return jsonify({
            'success': True,
            'message': 'Admin registered successfully',
            'user': new_admin,
            'token': token
        }), 201
        
    except Exception as e:
        print(f"Admin registration error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@admin_auth_bp.route('/login', methods=['POST'])
def login_admin():
    """Login admin with employee ID and password"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('employee_id') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Employee ID and password are required'}), 400
        
        # Verify password
        if not admin_model.verify_password(data['employee_id'], data['password']):
            return jsonify({'success': False, 'error': 'Invalid employee ID or password'}), 401
        
        # Get admin data
        admin = admin_model.get_admin_by_employee_id(data['employee_id'])
        if not admin:
            return jsonify({'success': False, 'error': 'Admin not found'}), 404
        
        # Generate token
        token = auth_utils.generate_token(admin)
        
        return jsonify({
            'success': True,
            'message': 'Admin login successful',
            'user': admin,
            'token': token
        }), 200
        
    except Exception as e:
        print(f"Admin login error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@admin_auth_bp.route('/profile', methods=['GET'])
def get_admin_profile():
    """Get admin profile"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        admin = admin_model.get_admin_by_id(payload['user_id'])
        if not admin:
            return jsonify({'error': 'Admin not found'}), 404
        
        return jsonify({'success': True, 'admin': admin}), 200
        
    except Exception as e:
        print(f"Get admin profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@admin_auth_bp.route('/profile', methods=['PUT'])
def update_admin_profile():
    """Update admin profile"""
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
        
        # Remove sensitive fields that shouldn't be updated via this endpoint
        data.pop('password', None)
        data.pop('employee_id', None)
        data.pop('_id', None)
        
        success = admin_model.update_admin(payload['user_id'], data)
        
        if success:
            updated_admin = admin_model.get_admin_by_id(payload['user_id'])
            return jsonify({
                'success': True,
                'message': 'Admin profile updated successfully',
                'admin': updated_admin
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to update admin profile'}), 500
        
    except Exception as e:
        print(f"Update admin profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@admin_auth_bp.route('/farmers', methods=['GET'])
def get_all_farmers():
    """Get all farmers (admin only)"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Verify it's an admin
        admin = admin_model.get_admin_by_id(payload['user_id'])
        if not admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all farmers
        from models.farmer import farmer_model
        farmers = farmer_model.get_all_farmers()
        
        return jsonify({
            'success': True,
            'farmers': farmers,
            'count': len(farmers)
        }), 200
        
    except Exception as e:
        print(f"Get all farmers error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
