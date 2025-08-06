from datetime import datetime
from bson import ObjectId
import bcrypt
from config.database import db

class User:
    def __init__(self):
        self.collection = db.get_collection('users')
    
    def create_user(self, user_data):
        """Create a new user"""
        try:
            # Hash the password
            password = user_data.get('password')
            if password:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                user_data['password'] = hashed_password
            
            # Add timestamps
            user_data['created_at'] = datetime.utcnow()
            user_data['updated_at'] = datetime.utcnow()
            
            # Insert user into database
            result = self.collection.insert_one(user_data)
            user_data['_id'] = str(result.inserted_id)
            
            # Remove password from response
            user_data.pop('password', None)
            
            return user_data
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            user = self.collection.find_one({'email': email})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            user = self.collection.find_one({'_id': ObjectId(user_id)})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def update_user(self, user_id, update_data):
        """Update user information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def verify_password(self, email, password):
        """Verify user password"""
        try:
            user = self.get_user_by_email(email)
            if user and user.get('password'):
                stored_password = user['password']
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
            return False
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False

# Create a global user model instance
user_model = User() 