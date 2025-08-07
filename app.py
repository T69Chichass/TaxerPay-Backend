import os
import eel
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from api.auth_routes import auth_bp
from api.farmer_auth_routes import farmer_auth_bp
from api.admin_auth_routes import admin_auth_bp
from api.tax_routes import tax_bp
from config.database import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(farmer_auth_bp, url_prefix='/api/farmer')
app.register_blueprint(admin_auth_bp, url_prefix='/api/admin')
app.register_blueprint(tax_bp, url_prefix='/api/tax')

# Configuration
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'TaxerPay Backend is running',
        'database': 'connected' if db.client else 'disconnected'
    }), 200

@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'TaxerPay API',
        'version': '1.0.0',
        'description': 'Farmer Land Tax Management System',
        'endpoints': {
            'farmer_auth': {
                'register': 'POST /api/farmer/register',
                'login': 'POST /api/farmer/login',
                'profile': 'GET /api/farmer/profile',
                'update_profile': 'PUT /api/farmer/profile'
            },
            'admin_auth': {
                'register': 'POST /api/admin/register',
                'login': 'POST /api/admin/login',
                'profile': 'GET /api/admin/profile',
                'update_profile': 'PUT /api/admin/profile',
                'get_all_farmers': 'GET /api/admin/farmers'
            },
            'general_auth': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login',
                'profile': 'GET /api/auth/profile',
                'update_profile': 'PUT /api/auth/profile'
            },
            'tax': {
                'create_record': 'POST /api/tax/records',
                'get_records': 'GET /api/tax/records',
                'get_record': 'GET /api/tax/records/<id>',
                'update_record': 'PUT /api/tax/records/<id>',
                'delete_record': 'DELETE /api/tax/records/<id>',
                'calculate_tax': 'POST /api/tax/calculate'
            }
        }
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - redirect to API info"""
    return jsonify({
        'message': 'TaxerPay Backend is running!',
        'status': 'healthy',
        'api_docs': '/api',
        'health_check': '/api/health',
        'frontend': 'Start the frontend with: cd ../frontend && npm start'
    }), 200

# Eel functions for frontend communication
@eel.expose
def python_function():
    """Example Python function exposed to JavaScript"""
    return "Hello from Python!"

@eel.expose
def get_user_data(user_id):
    """Get user data from Python"""
    from models.user import user_model
    return user_model.get_user_by_id(user_id)

@eel.expose
def create_tax_record_python(tax_data):
    """Create tax record from Python"""
    from models.tax_record import tax_record_model
    try:
        result = tax_record_model.create_tax_record(tax_data)
        return {'success': True, 'data': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@eel.expose
def calculate_tax_python(income, tax_type='federal'):
    """Calculate tax from Python"""
    try:
        income = float(income)
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
            tax = income * 0.05
        
        return {
            'success': True,
            'income': income,
            'tax_type': tax_type,
            'calculated_tax': round(tax, 2),
            'effective_rate': round((tax / income) * 100, 2) if income > 0 else 0
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def start_eel_app():
    """Start the Eel application"""
    try:
        # Set the web files directory
        web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'build')
        
        # Check if build directory exists, otherwise use src
        if not os.path.exists(web_dir):
            web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'src')
        
        # Check if index.html exists in the web directory
        index_path = os.path.join(web_dir, 'index.html')
        if not os.path.exists(index_path):
            print(f"⚠️  index.html not found in {web_dir}")
            print("🔄 Falling back to Flask-only mode...")
            start_flask_only()
            return
        
        # Initialize Eel
        eel.init(web_dir)
        
        # Start the application
        host = os.getenv('HOST', 'localhost')
        port = int(os.getenv('PORT', 8000))
        
        print(f"🚀 Starting TaxerPay Backend with Eel...")
        print(f"📁 Web directory: {web_dir}")
        print(f"🌐 Server: http://{host}:{port}")
        print(f"🔗 API: http://{host}:{port}/api")
        
        # Start Eel with Flask
        eel.start('index.html', 
                  host=host, 
                  port=port, 
                  mode='chrome',
                  size=(1200, 800),
                  position=(100, 100))
        
    except Exception as e:
        print(f"❌ Error starting Eel app: {e}")
        # Fallback to Flask only
        start_flask_only()

def start_flask_only():
    """Start Flask app without Eel (fallback)"""
    try:
        host = os.getenv('HOST', 'localhost')
        port = int(os.getenv('PORT', 8000))
        
        print(f"🚀 Starting TaxerPay Backend (Flask only)...")
        print(f"🌐 Server: http://{host}:{port}")
        print(f"🔗 API: http://{host}:{port}/api")
        
        app.run(host=host, port=port, debug=True)
        
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")

if __name__ == '__main__':
    try:
        # Test database connection
        if db.client:
            print("✅ Database connection successful")
            start_eel_app()
        else:
            print("❌ Database connection failed")
            start_flask_only()
    except KeyboardInterrupt:
        print("\n👋 Shutting down TaxerPay Backend...")
        db.close()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        db.close() 