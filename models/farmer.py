from datetime import datetime
from bson import ObjectId
import bcrypt
from config.database import db

class Farmer:
    def __init__(self):
        self.collection = db.get_collection('farmers')
    
    def create_farmer(self, farmer_data):
        """Create a new farmer account"""
        try:
            # Hash the password
            password = farmer_data.get('password')
            if password:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                farmer_data['password'] = hashed_password
            
            # Add timestamps and user type
            farmer_data['user_type'] = 'farmer'
            farmer_data['created_at'] = datetime.utcnow()
            farmer_data['updated_at'] = datetime.utcnow()
            
            # Insert farmer into database
            result = self.collection.insert_one(farmer_data)
            farmer_data['_id'] = str(result.inserted_id)
            
            # Remove password from response
            farmer_data.pop('password', None)
            
            return farmer_data
            
        except Exception as e:
            print(f"Error creating farmer: {e}")
            raise
    
    def get_farmer_by_pan(self, pan_card, include_password=False):
        """Get farmer by PAN card ID"""
        try:
            farmer = self.collection.find_one({'pan_card': pan_card.upper()})
            if farmer:
                farmer['_id'] = str(farmer['_id'])
                # Remove password unless specifically requested
                if not include_password and 'password' in farmer:
                    del farmer['password']
            return farmer
        except Exception as e:
            print(f"Error getting farmer by PAN: {e}")
            return None
    
    def get_farmer_by_id(self, farmer_id):
        """Get farmer by ID"""
        try:
            farmer = self.collection.find_one({'_id': ObjectId(farmer_id)})
            if farmer:
                farmer['_id'] = str(farmer['_id'])
            return farmer
        except Exception as e:
            print(f"Error getting farmer by ID: {e}")
            return None
    
    def update_farmer(self, farmer_id, update_data):
        """Update farmer information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(farmer_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating farmer: {e}")
            return False
    
    def verify_password(self, pan_card, password):
        """Verify farmer password"""
        try:
            farmer = self.get_farmer_by_pan(pan_card, include_password=True)
            if farmer and farmer.get('password'):
                stored_password = farmer['password']
                # Convert stored password to bytes if it's a string
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_password)
            return False
        except Exception as e:
            print(f"Error verifying farmer password: {e}")
            return False
    
    def get_all_farmers(self):
        """Get all farmers (for admin use)"""
        try:
            farmers = list(self.collection.find({}))
            for farmer in farmers:
                farmer['_id'] = str(farmer['_id'])
                farmer.pop('password', None)  # Remove password from response
            return farmers
        except Exception as e:
            print(f"Error getting all farmers: {e}")
            return []

    def update_farmer_password(self, farmer_id, new_password):
        """Update farmer password"""
        try:
            # Hash the new password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # Update the farmer's password
            result = self.collection.update_one(
                {'_id': ObjectId(farmer_id)},
                {'$set': {'password': hashed_password.decode('utf-8'), 'updated_at': datetime.utcnow()}}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating farmer password: {e}")
            return False

# Create a global farmer model instance
farmer_model = Farmer()
