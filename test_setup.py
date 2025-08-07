#!/usr/bin/env python3
"""
Simple test script to verify farmer and admin models
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.farmer import farmer_model
from models.admin import admin_model
from config.database import db

# Load environment variables
load_dotenv()

def test_farmer_model():
    """Test farmer model functionality"""
    print("🧪 Testing Farmer Model...")
    
    # Test data
    test_farmer = {
        'pan_card': 'TEST123456A',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'Farmer',
        'phone': '+91-1234567890',
        'email': 'test.farmer@email.com'
    }
    
    try:
        # Create farmer
        result = farmer_model.create_farmer(test_farmer)
        print(f"✅ Created farmer: {result['first_name']} {result['last_name']}")
        
        # Get farmer by PAN
        farmer = farmer_model.get_farmer_by_pan('TEST123456A')
        if farmer:
            print(f"✅ Retrieved farmer by PAN: {farmer['pan_card']}")
        
        # Test password verification
        if farmer_model.verify_password('TEST123456A', 'testpass123'):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
        
        print("✅ Farmer model test completed successfully!")
        
    except Exception as e:
        print(f"❌ Farmer model test failed: {e}")

def test_admin_model():
    """Test admin model functionality"""
    print("\n🧪 Testing Admin Model...")
    
    # Test data
    test_admin = {
        'employee_id': 'TEST001',
        'password': 'adminpass123',
        'first_name': 'Test',
        'last_name': 'Admin',
        'phone': '+91-0987654321',
        'email': 'test.admin@taxerpay.gov.in',
        'department': 'Testing',
        'designation': 'Test Officer'
    }
    
    try:
        # Create admin
        result = admin_model.create_admin(test_admin)
        print(f"✅ Created admin: {result['first_name']} {result['last_name']}")
        
        # Get admin by employee ID
        admin = admin_model.get_admin_by_employee_id('TEST001')
        if admin:
            print(f"✅ Retrieved admin by Employee ID: {admin['employee_id']}")
        
        # Test password verification
        if admin_model.verify_password('TEST001', 'adminpass123'):
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
        
        print("✅ Admin model test completed successfully!")
        
    except Exception as e:
        print(f"❌ Admin model test failed: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Model Tests...")
    print("=" * 50)
    
    try:
        # Check database connection
        if not db.client:
            print("❌ Database connection failed!")
            return
        
        print("✅ Database connection successful")
        
        # Test models
        test_farmer_model()
        test_admin_model()
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == '__main__':
    main()
