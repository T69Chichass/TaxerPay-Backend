from datetime import datetime
from bson import ObjectId
import bcrypt
from config.database import db

class Admin:
    def __init__(self):
        self.collection = db.get_collection('admins')
    
    def create_admin(self, admin_data):
        """Create a new admin account"""
        try:
            # Hash the password
            password = admin_data.get('password')
            if password:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                admin_data['password'] = hashed_password
            
            # Add timestamps and user type
            admin_data['user_type'] = 'admin'
            admin_data['created_at'] = datetime.utcnow()
            admin_data['updated_at'] = datetime.utcnow()
            
            # Insert admin into database
            result = self.collection.insert_one(admin_data)
            admin_data['_id'] = str(result.inserted_id)
            
            # Remove password from response
            admin_data.pop('password', None)
            
            return admin_data
            
        except Exception as e:
            print(f"Error creating admin: {e}")
            raise
    
    def get_admin_by_employee_id(self, employee_id):
        """Get admin by employee ID"""
        try:
            admin = self.collection.find_one({'employee_id': employee_id.upper()})
            if admin:
                admin['_id'] = str(admin['_id'])
            return admin
        except Exception as e:
            print(f"Error getting admin by employee ID: {e}")
            return None
    
    def get_admin_by_id(self, admin_id):
        """Get admin by ID"""
        try:
            admin = self.collection.find_one({'_id': ObjectId(admin_id)})
            if admin:
                admin['_id'] = str(admin['_id'])
            return admin
        except Exception as e:
            print(f"Error getting admin by ID: {e}")
            return None
    
    def update_admin(self, admin_id, update_data):
        """Update admin information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(admin_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating admin: {e}")
            return False
    
    def verify_password(self, employee_id, password):
        """Verify admin password"""
        try:
            admin = self.get_admin_by_employee_id(employee_id)
            if admin and admin.get('password'):
                stored_password = admin['password']
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
            return False
        except Exception as e:
            print(f"Error verifying admin password: {e}")
            return False
    
    def get_all_admins(self):
        """Get all admins"""
        try:
            admins = list(self.collection.find({}))
            for admin in admins:
                admin['_id'] = str(admin['_id'])
                admin.pop('password', None)  # Remove password from response
            return admins
        except Exception as e:
            print(f"Error getting all admins: {e}")
            return []

# Create a global admin model instance
admin_model = Admin()
