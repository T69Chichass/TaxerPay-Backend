#!/usr/bin/env python3
"""
Script to populate the database with test data for farmers and admins
Run this script to add sample data for testing the application
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.farmer import farmer_model
from models.admin import admin_model
from config.database import db

# Load environment variables
load_dotenv()

def populate_farmers():
    """Populate farmers collection with test data"""
    print("🌾 Populating farmers database...")
    
    # Sample farmer data
    farmers_data = [
        {
            'pan_card': 'ABCDE1234F',
            'password': 'farmer123',
            'first_name': 'Rajesh',
            'last_name': 'Patel',
            'phone': '+91-9876543210',
            'email': 'rajesh.patel@email.com',
            'address': {
                'street': 'Farm House No. 45',
                'village': 'Patel Nagar',
                'district': 'Ahmedabad',
                'state': 'Gujarat',
                'pincode': '380001'
            },
            'land_details': {
                'total_acres': 25.5,
                'irrigated_acres': 20.0,
                'crop_type': 'Wheat, Cotton'
            },
            'bank_details': {
                'account_number': '1234567890',
                'bank_name': 'State Bank of India',
                'ifsc_code': 'SBIN0001234'
            }
        },
        {
            'pan_card': 'FGHIJ5678K',
            'password': 'farmer456',
            'first_name': 'Lakshmi',
            'last_name': 'Devi',
            'phone': '+91-8765432109',
            'email': 'lakshmi.devi@email.com',
            'address': {
                'street': 'Village Road No. 12',
                'village': 'Devi Gram',
                'district': 'Surat',
                'state': 'Gujarat',
                'pincode': '395001'
            },
            'land_details': {
                'total_acres': 15.0,
                'irrigated_acres': 12.5,
                'crop_type': 'Rice, Sugarcane'
            },
            'bank_details': {
                'account_number': '0987654321',
                'bank_name': 'Bank of Baroda',
                'ifsc_code': 'BARB0005678'
            }
        },
        {
            'pan_card': 'KLMNO9012P',
            'password': 'farmer789',
            'first_name': 'Suresh',
            'last_name': 'Kumar',
            'phone': '+91-7654321098',
            'email': 'suresh.kumar@email.com',
            'address': {
                'street': 'Farm Plot No. 78',
                'village': 'Kumar Colony',
                'district': 'Vadodara',
                'state': 'Gujarat',
                'pincode': '390001'
            },
            'land_details': {
                'total_acres': 30.0,
                'irrigated_acres': 25.0,
                'crop_type': 'Maize, Pulses'
            },
            'bank_details': {
                'account_number': '1122334455',
                'bank_name': 'Punjab National Bank',
                'ifsc_code': 'PUNB0009012'
            }
        },
        {
            'pan_card': 'PQRST3456U',
            'password': 'farmer012',
            'first_name': 'Meera',
            'last_name': 'Singh',
            'phone': '+91-6543210987',
            'email': 'meera.singh@email.com',
            'address': {
                'street': 'Agricultural Land No. 23',
                'village': 'Singh Village',
                'district': 'Rajkot',
                'state': 'Gujarat',
                'pincode': '360001'
            },
            'land_details': {
                'total_acres': 18.5,
                'irrigated_acres': 15.0,
                'crop_type': 'Vegetables, Fruits'
            },
            'bank_details': {
                'account_number': '5566778899',
                'bank_name': 'HDFC Bank',
                'ifsc_code': 'HDFC0003456'
            }
        },
        {
            'pan_card': 'UVWXY6789Z',
            'password': 'farmer345',
            'first_name': 'Amit',
            'last_name': 'Shah',
            'phone': '+91-5432109876',
            'email': 'amit.shah@email.com',
            'address': {
                'street': 'Farm House No. 67',
                'village': 'Shah Gram',
                'district': 'Bhavnagar',
                'state': 'Gujarat',
                'pincode': '364001'
            },
            'land_details': {
                'total_acres': 22.0,
                'irrigated_acres': 18.5,
                'crop_type': 'Groundnut, Sesame'
            },
            'bank_details': {
                'account_number': '9988776655',
                'bank_name': 'ICICI Bank',
                'ifsc_code': 'ICIC0006789'
            }
        }
    ]
    
    # Insert farmers
    for farmer_data in farmers_data:
        try:
            # Check if farmer already exists
            existing_farmer = farmer_model.get_farmer_by_pan(farmer_data['pan_card'])
            if existing_farmer:
                print(f"⚠️  Farmer with PAN {farmer_data['pan_card']} already exists, skipping...")
                continue
            
            # Create new farmer
            result = farmer_model.create_farmer(farmer_data)
            print(f"✅ Created farmer: {result['first_name']} {result['last_name']} (PAN: {result['pan_card']})")
            
        except Exception as e:
            print(f"❌ Error creating farmer {farmer_data['pan_card']}: {e}")
    
    print(f"🌾 Farmers population completed!")

def populate_admins():
    """Populate admins collection with test data"""
    print("👨‍💼 Populating admins database...")
    
    # Sample admin data
    admins_data = [
        {
            'employee_id': 'ADMIN001',
            'password': 'admin123',
            'first_name': 'Ramesh',
            'last_name': 'Kumar',
            'phone': '+91-9876543211',
            'email': 'ramesh.kumar@taxerpay.gov.in',
            'department': 'Tax Collection',
            'designation': 'Senior Tax Officer',
            'address': {
                'street': 'Government Quarters No. 15',
                'city': 'Gandhinagar',
                'state': 'Gujarat',
                'pincode': '382001'
            },
            'permissions': ['view_farmers', 'edit_farmers', 'view_taxes', 'collect_taxes', 'generate_reports']
        },
        {
            'employee_id': 'ADMIN002',
            'password': 'admin456',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'phone': '+91-8765432108',
            'email': 'priya.sharma@taxerpay.gov.in',
            'department': 'Farmer Relations',
            'designation': 'Farmer Support Officer',
            'address': {
                'street': 'Staff Quarters No. 8',
                'city': 'Ahmedabad',
                'state': 'Gujarat',
                'pincode': '380001'
            },
            'permissions': ['view_farmers', 'edit_farmers', 'view_taxes', 'support_farmers']
        },
        {
            'employee_id': 'ADMIN003',
            'password': 'admin789',
            'first_name': 'Vikram',
            'last_name': 'Patel',
            'phone': '+91-7654321097',
            'email': 'vikram.patel@taxerpay.gov.in',
            'department': 'IT Support',
            'designation': 'System Administrator',
            'address': {
                'street': 'Tech Park Quarters No. 22',
                'city': 'Surat',
                'state': 'Gujarat',
                'pincode': '395001'
            },
            'permissions': ['view_farmers', 'view_admins', 'system_admin', 'generate_reports']
        },
        {
            'employee_id': 'ADMIN004',
            'password': 'admin012',
            'first_name': 'Sunita',
            'last_name': 'Verma',
            'phone': '+91-6543210986',
            'email': 'sunita.verma@taxerpay.gov.in',
            'department': 'Finance',
            'designation': 'Finance Officer',
            'address': {
                'street': 'Finance Quarters No. 11',
                'city': 'Vadodara',
                'state': 'Gujarat',
                'pincode': '390001'
            },
            'permissions': ['view_farmers', 'view_taxes', 'collect_taxes', 'generate_reports', 'financial_reports']
        },
        {
            'employee_id': 'ADMIN005',
            'password': 'admin345',
            'first_name': 'Arjun',
            'last_name': 'Singh',
            'phone': '+91-5432100985',
            'email': 'arjun.singh@taxerpay.gov.in',
            'department': 'Field Operations',
            'designation': 'Field Officer',
            'address': {
                'street': 'Field Office Quarters No. 5',
                'city': 'Rajkot',
                'state': 'Gujarat',
                'pincode': '360001'
            },
            'permissions': ['view_farmers', 'edit_farmers', 'view_taxes', 'field_operations']
        }
    ]
    
    # Insert admins
    for admin_data in admins_data:
        try:
            # Check if admin already exists
            existing_admin = admin_model.get_admin_by_employee_id(admin_data['employee_id'])
            if existing_admin:
                print(f"⚠️  Admin with Employee ID {admin_data['employee_id']} already exists, skipping...")
                continue
            
            # Create new admin
            result = admin_model.create_admin(admin_data)
            print(f"✅ Created admin: {result['first_name']} {result['last_name']} (ID: {result['employee_id']})")
            
        except Exception as e:
            print(f"❌ Error creating admin {admin_data['employee_id']}: {e}")
    
    print(f"👨‍💼 Admins population completed!")

def main():
    """Main function to populate both databases"""
    print("🚀 Starting database population...")
    print("=" * 50)
    
    try:
        # Check database connection
        if not db.client:
            print("❌ Database connection failed!")
            return
        
        print("✅ Database connection successful")
        
        # Populate farmers
        populate_farmers()
        print()
        
        # Populate admins
        populate_admins()
        print()
        
        print("=" * 50)
        print("🎉 Database population completed successfully!")
        print()
        print("📋 Test Data Summary:")
        print("🌾 Farmers: 5 test accounts created")
        print("👨‍💼 Admins: 5 test accounts created")
        print()
        print("🔑 Test Credentials:")
        print("🌾 Farmers (Login with PAN + Password):")
        print("   - PAN: ABCDE1234F, Password: farmer123")
        print("   - PAN: FGHIJ5678K, Password: farmer456")
        print("   - PAN: KLMNO9012P, Password: farmer789")
        print("   - PAN: PQRST3456U, Password: farmer012")
        print("   - PAN: UVWXY6789Z, Password: farmer345")
        print()
        print("👨‍💼 Admins (Login with Employee ID + Password):")
        print("   - Employee ID: ADMIN001, Password: admin123")
        print("   - Employee ID: ADMIN002, Password: admin456")
        print("   - Employee ID: ADMIN003, Password: admin789")
        print("   - Employee ID: ADMIN004, Password: admin012")
        print("   - Employee ID: ADMIN005, Password: admin345")
        
    except Exception as e:
        print(f"❌ Error during database population: {e}")

if __name__ == '__main__':
    main()
