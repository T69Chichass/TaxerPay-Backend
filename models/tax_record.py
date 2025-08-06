from datetime import datetime
from bson import ObjectId
from config.database import db

class TaxRecord:
    def __init__(self):
        self.collection = db.get_collection('tax_records')
    
    def create_tax_record(self, tax_data):
        """Create a new tax record"""
        try:
            # Add timestamps
            tax_data['created_at'] = datetime.utcnow()
            tax_data['updated_at'] = datetime.utcnow()
            
            # Insert tax record into database
            result = self.collection.insert_one(tax_data)
            tax_data['_id'] = str(result.inserted_id)
            
            return tax_data
            
        except Exception as e:
            print(f"Error creating tax record: {e}")
            raise
    
    def get_tax_records_by_user(self, user_id):
        """Get all tax records for a specific user"""
        try:
            records = list(self.collection.find({'user_id': user_id}))
            for record in records:
                record['_id'] = str(record['_id'])
            return records
        except Exception as e:
            print(f"Error getting tax records: {e}")
            return []
    
    def get_tax_record_by_id(self, record_id):
        """Get a specific tax record by ID"""
        try:
            record = self.collection.find_one({'_id': ObjectId(record_id)})
            if record:
                record['_id'] = str(record['_id'])
            return record
        except Exception as e:
            print(f"Error getting tax record: {e}")
            return None
    
    def update_tax_record(self, record_id, update_data):
        """Update a tax record"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(record_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating tax record: {e}")
            return False
    
    def delete_tax_record(self, record_id):
        """Delete a tax record"""
        try:
            result = self.collection.delete_one({'_id': ObjectId(record_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting tax record: {e}")
            return False

# Create a global tax record model instance
tax_record_model = TaxRecord() 