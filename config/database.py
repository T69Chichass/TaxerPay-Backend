import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            # Get MongoDB URI from environment variables
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('DATABASE_NAME', 'taxerpay')
            
            if not mongodb_uri:
                raise ValueError("MONGODB_URI not found in environment variables")
            
            # Connect to MongoDB Atlas
            self.client = MongoClient(mongodb_uri)
            self.db = self.client[database_name]
            
            # Test the connection
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB Atlas")
            
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise
    
    def get_collection(self, collection_name):
        """Get a specific collection from the database"""
        return self.db[collection_name]
    
    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            print("Database connection closed")

# Create a global database instance
db = Database() 