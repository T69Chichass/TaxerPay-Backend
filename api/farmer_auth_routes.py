from flask import Blueprint, request, jsonify
from models.farmer import farmer_model
from utils.auth import auth_utils
import json

farmer_auth_bp = Blueprint('farmer_auth', __name__)

@farmer_auth_bp.route('/register', methods=['POST'])
def register_farmer():
    """Register a new farmer"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['pan_card', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if farmer already exists
        existing_farmer = farmer_model.get_farmer_by_pan(data['pan_card'])
        if existing_farmer:
            return jsonify({'error': 'Farmer with this PAN card already exists'}), 409
        
        # Create farmer
        farmer_data = {
            'pan_card': data['pan_card'].upper(),
            'password': data['password'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'address': data.get('address', {}),
            'land_details': data.get('land_details', {}),
            'bank_details': data.get('bank_details', {})
        }
        
        new_farmer = farmer_model.create_farmer(farmer_data)
        
        # Generate token
        token = auth_utils.generate_token(new_farmer)
        
        return jsonify({
            'success': True,
            'message': 'Farmer registered successfully',
            'user': new_farmer,
            'token': token
        }), 201
        
    except Exception as e:
        print(f"Farmer registration error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@farmer_auth_bp.route('/login', methods=['POST'])
def login_farmer():
    """Login farmer with PAN card and password"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('pan_card') or not data.get('password'):
            return jsonify({'success': False, 'error': 'PAN card and password are required'}), 400
        
        # Verify password
        if not farmer_model.verify_password(data['pan_card'], data['password']):
            return jsonify({'success': False, 'error': 'Invalid PAN card or password'}), 401
        
        # Get farmer data
        farmer = farmer_model.get_farmer_by_pan(data['pan_card'])
        if not farmer:
            return jsonify({'success': False, 'error': 'Farmer not found'}), 404
        
        # Generate token
        token = auth_utils.generate_token(farmer)
        
        return jsonify({
            'success': True,
            'message': 'Farmer login successful',
            'user': farmer,
            'token': token
        }), 200
        
    except Exception as e:
        print(f"Farmer login error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@farmer_auth_bp.route('/profile', methods=['GET'])
def get_farmer_profile():
    """Get farmer profile"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        token = auth_header.split(' ')[1]
        payload = auth_utils.verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        farmer = farmer_model.get_farmer_by_id(payload['user_id'])
        if not farmer:
            return jsonify({'error': 'Farmer not found'}), 404
        
        return jsonify({'success': True, 'farmer': farmer}), 200
        
    except Exception as e:
        print(f"Get farmer profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@farmer_auth_bp.route('/profile', methods=['PUT'])
def update_farmer_profile():
    """Update farmer profile"""
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
        data.pop('pan_card', None)
        data.pop('_id', None)
        
        success = farmer_model.update_farmer(payload['user_id'], data)
        
        if success:
            updated_farmer = farmer_model.get_farmer_by_id(payload['user_id'])
            return jsonify({
                'success': True,
                'message': 'Farmer profile updated successfully',
                'farmer': updated_farmer
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to update farmer profile'}), 500
        
    except Exception as e:
        print(f"Update farmer profile error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@farmer_auth_bp.route('/exists', methods=['GET'])
def farmer_exists():
    pan_card = request.args.get('pan_card', '').upper()
    if not pan_card:
        return jsonify({'exists': False, 'error': 'PAN card is required'}), 400
    farmer = farmer_model.get_farmer_by_pan(pan_card)
    return jsonify({'exists': bool(farmer)})
