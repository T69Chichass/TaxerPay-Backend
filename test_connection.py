#!/usr/bin/env python3
"""
Simple script to test MongoDB Atlas connection
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

def test_connection():
    """Test MongoDB Atlas connection"""
    print("🔍 Testing MongoDB Atlas connection...")
    print("=" * 50)
    
    # Get MongoDB URI from environment variables
    mongodb_uri = os.getenv('MONGODB_URI')
    database_name = os.getenv('DATABASE_NAME', 'taxerpay')
    
    print(f"📋 Environment check:")
    print(f"   MONGODB_URI: {'✅ Found' if mongodb_uri else '❌ Not found'}")
    print(f"   DATABASE_NAME: {database_name}")
    
    if not mongodb_uri:
        print("\n❌ MONGODB_URI not found in .env file!")
        print("   Please create a .env file with your MongoDB Atlas connection string.")
        return False
    
    try:
        # Connect to MongoDB Atlas
        print(f"\n🔌 Connecting to MongoDB Atlas...")
        client = MongoClient(mongodb_uri)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client[database_name]
        print(f"📊 Database: {database_name}")
        
        # List existing collections
        collections = db.list_collection_names()
        print(f"📁 Existing collections: {collections if collections else 'None'}")
        
        # Test farmers collection
        farmers_collection = db.get_collection('farmers')
        farmers_count = farmers_collection.count_documents({})
        print(f"🌾 Farmers in database: {farmers_count}")
        
        # Test admins collection
        admins_collection = db.get_collection('admins')
        admins_count = admins_collection.count_documents({})
        print(f"👨‍💼 Admins in database: {admins_count}")
        
        # Close connection
        client.close()
        print("\n✅ Connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error connecting to MongoDB: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Check your .env file exists and has correct MONGODB_URI")
        print("   2. Verify your MongoDB Atlas username and password")
        print("   3. Make sure your IP address is whitelisted in MongoDB Atlas")
        print("   4. Check if your cluster is running")
        return False

if __name__ == '__main__':
    test_connection()
