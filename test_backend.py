#!/usr/bin/env python3
"""
Test script for TaxerPay Backend
This script tests the backend setup and API endpoints.
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running.")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_info():
    """Test API info endpoint"""
    print("🔍 Testing API info...")
    try:
        response = requests.get(API_BASE)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API info: {data['name']} v{data['version']}")
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("🔍 Testing user registration...")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "123-456-7890",
        "user_type": "individual"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/register",
            headers={"Content-Type": "application/json"},
            data=json.dumps(user_data)
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ User registration successful")
            return data.get('token')
        elif response.status_code == 409:
            print("⚠️  User already exists, trying login...")
            return test_user_login()
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_user_login():
    """Test user login"""
    print("🔍 Testing user login...")
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps(login_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User login successful")
            return data.get('token')
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_tax_calculation(token):
    """Test tax calculation"""
    print("🔍 Testing tax calculation...")
    calculation_data = {
        "income": 50000,
        "tax_type": "federal"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/tax/calculate",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            data=json.dumps(calculation_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tax calculation successful: ${data['calculated_tax']} for ${data['income']} income")
            return True
        else:
            print(f"❌ Tax calculation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Tax calculation error: {e}")
        return False

def test_tax_record_creation(token):
    """Test tax record creation"""
    print("🔍 Testing tax record creation...")
    tax_data = {
        "tax_year": 2024,
        "income": 50000,
        "tax_type": "federal",
        "deductions": 5000,
        "credits": 1000
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/tax/records",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            data=json.dumps(tax_data)
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Tax record creation successful")
            return data.get('record', {}).get('_id')
        else:
            print(f"❌ Tax record creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Tax record creation error: {e}")
        return None

def test_tax_records_listing(token):
    """Test tax records listing"""
    print("🔍 Testing tax records listing...")
    
    try:
        response = requests.get(
            f"{API_BASE}/tax/records",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Tax records listing successful: {data['count']} records found")
            return True
        else:
            print(f"❌ Tax records listing failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Tax records listing error: {e}")
        return False

def test_user_profile(token):
    """Test user profile retrieval"""
    print("🔍 Testing user profile...")
    
    try:
        response = requests.get(
            f"{API_BASE}/auth/profile",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User profile retrieved: {data['user']['first_name']} {data['user']['last_name']}")
            return True
        else:
            print(f"❌ User profile failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ User profile error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TaxerPay Backend Test Suite")
    print("=" * 50)
    
    # Test basic connectivity
    if not test_health_check():
        print("\n❌ Backend is not running or not accessible")
        print("Please start the backend with: python app.py")
        sys.exit(1)
    
    if not test_api_info():
        print("\n❌ API info test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🔐 Testing Authentication...")
    
    # Test authentication
    token = test_user_registration()
    if not token:
        print("\n❌ Authentication tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🧮 Testing Tax Features...")
    
    # Test tax features
    tax_calc_ok = test_tax_calculation(token)
    tax_record_ok = test_tax_record_creation(token)
    tax_listing_ok = test_tax_records_listing(token)
    
    print("\n" + "=" * 50)
    print("👤 Testing User Features...")
    
    # Test user features
    profile_ok = test_user_profile(token)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    results = [
        ("Health Check", True),
        ("API Info", True),
        ("Authentication", bool(token)),
        ("Tax Calculation", tax_calc_ok),
        ("Tax Record Creation", tax_record_ok),
        ("Tax Records Listing", tax_listing_ok),
        ("User Profile", profile_ok)
    ]
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the backend configuration.")
        sys.exit(1)

if __name__ == '__main__':
    main() 