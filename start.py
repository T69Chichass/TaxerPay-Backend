#!/usr/bin/env python3
"""
TaxerPay Backend Startup Script
This script handles environment setup and starts the backend server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import eel
        import pymongo
        import flask
        import dotenv
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("Creating .env file from template...")
        
        # Copy from env_example.txt if it exists
        example_file = Path('env_example.txt')
        if example_file.exists():
            with open(example_file, 'r') as f:
                content = f.read()
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please update .env with your MongoDB Atlas credentials")
            return False
        else:
            print("❌ env_example.txt not found")
            return False
    
    print("✅ .env file found")
    return True

def check_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from config.database import db
        if db.client:
            print("✅ MongoDB connection successful")
            return True
        else:
            print("❌ MongoDB connection failed")
            return False
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return False

def build_frontend():
    """Build the React frontend"""
    frontend_path = Path('../frontend')
    if not frontend_path.exists():
        print("⚠️  Frontend directory not found")
        return False
    
    print("🔨 Building frontend...")
    try:
        # Change to frontend directory
        os.chdir(frontend_path)
        
        # Check if node_modules exists
        if not Path('node_modules').exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Build the frontend
        print("🏗️  Building React app...")
        subprocess.run(['npm', 'run', 'build'], check=True)
        
        # Change back to backend directory
        os.chdir('../TaxerPay-Backend')
        
        print("✅ Frontend built successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend build failed: {e}")
        os.chdir('../TaxerPay-Backend')  # Change back to backend directory
        return False
    except Exception as e:
        print(f"❌ Frontend build error: {e}")
        os.chdir('../TaxerPay-Backend')  # Change back to backend directory
        return False

def main():
    """Main startup function"""
    print("🚀 TaxerPay Backend Startup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
            print("✅ Dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Check environment file
    env_ok = check_env_file()
    
    # Try to build frontend
    frontend_ok = build_frontend()
    
    # Check MongoDB connection (only if env file exists)
    if env_ok:
        mongodb_ok = check_mongodb_connection()
    else:
        mongodb_ok = False
    
    print("\n" + "=" * 40)
    
    if not env_ok:
        print("⚠️  Please configure your .env file with MongoDB Atlas credentials")
        print("Then run this script again")
        sys.exit(1)
    
    if not mongodb_ok:
        print("⚠️  MongoDB connection failed")
        print("Please check your MongoDB Atlas credentials in .env file")
        print("Starting in Flask-only mode...")
    
    if not frontend_ok:
        print("⚠️  Frontend build failed")
        print("Starting in Flask-only mode...")
    
    # Start the application
    print("\n🎯 Starting TaxerPay Backend...")
    try:
        from app import start_eel_app, start_flask_only
        
        if mongodb_ok and frontend_ok:
            start_eel_app()
        else:
            start_flask_only()
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 