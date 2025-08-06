# TaxerPay Backend Setup Guide

This guide will help you set up the TaxerPay backend with Python, MongoDB Atlas, and Eel integration.

## Prerequisites

- **Python 3.8 or higher**
- **MongoDB Atlas account** (free tier available)
- **Node.js** (for frontend build)
- **Git** (for version control)

## Step 1: Environment Setup

### 1.1 Install Python Dependencies

```bash
cd TaxerPay-Backend
pip install -r requirements.txt
```

### 1.2 Set Up MongoDB Atlas

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account
   - Create a new project

2. **Create a Cluster**
   - Choose "Free" tier (M0)
   - Select your preferred cloud provider and region
   - Click "Create"

3. **Set Up Database Access**
   - Go to "Database Access" in the left sidebar
   - Click "Add New Database User"
   - Create a username and password (save these!)
   - Select "Read and write to any database"
   - Click "Add User"

4. **Set Up Network Access**
   - Go to "Network Access" in the left sidebar
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (for development)
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Database" in the left sidebar
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string

### 1.3 Configure Environment Variables

```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env with your MongoDB Atlas credentials
```

Update the `.env` file with your MongoDB Atlas connection string:

```env
# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/taxerpay?retryWrites=true&w=majority
DATABASE_NAME=taxerpay

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
JWT_ALGORITHM=HS256

# Server Configuration
HOST=localhost
PORT=8000

# Frontend Configuration
FRONTEND_PATH=../frontend/build
```

## Step 2: Frontend Setup

### 2.1 Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

### 2.2 Build Frontend (Optional)

The backend will automatically build the frontend, but you can do it manually:

```bash
npm run build
```

## Step 3: Start the Backend

### 3.1 Using the Startup Script (Recommended)

```bash
cd TaxerPay-Backend
python start.py
```

This script will:
- Check Python version
- Install dependencies if needed
- Set up environment file
- Build frontend
- Test MongoDB connection
- Start the application

### 3.2 Manual Start

```bash
cd TaxerPay-Backend
python app.py
```

## Step 4: Verify Setup

### 4.1 Test the Backend

```bash
cd TaxerPay-Backend
python test_backend.py
```

This will test all API endpoints and verify the setup.

### 4.2 Manual Testing

1. **Health Check**
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **API Info**
   ```bash
   curl http://localhost:8000/api
   ```

3. **Register a User**
   ```bash
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "password123",
       "first_name": "John",
       "last_name": "Doe"
     }'
   ```

## Step 5: Access the Application

### 5.1 Eel Mode (Recommended)
When you start the backend, it will automatically open a Chrome window with your application.

### 5.2 API Mode
Access the API directly at: `http://localhost:8000/api`

### 5.3 Frontend Only
If you want to run the frontend separately:
```bash
cd frontend
npm start
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   ```
   ❌ MongoDB connection error: Authentication failed
   ```
   **Solution**: Check your MongoDB Atlas credentials in `.env` file

2. **Port Already in Use**
   ```
   ❌ Address already in use
   ```
   **Solution**: Change the PORT in `.env` file or kill the process using the port

3. **Frontend Build Error**
   ```
   ❌ Frontend build failed
   ```
   **Solution**: 
   - Make sure Node.js is installed
   - Run `npm install` in the frontend directory
   - Check for any build errors

4. **Import Errors**
   ```
   ❌ No module named 'eel'
   ```
   **Solution**: Run `pip install -r requirements.txt`

5. **Eel Not Starting**
   ```
   ❌ Error starting Eel app
   ```
   **Solution**: 
   - Make sure Chrome is installed
   - Check if the frontend build directory exists
   - The app will fall back to Flask-only mode

### Getting Help

1. **Check Logs**: The application provides detailed logging
2. **Test Script**: Run `python test_backend.py` to diagnose issues
3. **Manual Testing**: Use curl or Postman to test individual endpoints

## Development

### Project Structure
```
TaxerPay-Backend/
├── api/                 # API routes
│   ├── auth_routes.py   # Authentication endpoints
│   └── tax_routes.py    # Tax management endpoints
├── config/              # Configuration
│   └── database.py      # Database connection
├── models/              # Data models
│   ├── user.py          # User model
│   └── tax_record.py    # Tax record model
├── utils/               # Utilities
│   └── auth.py          # Authentication utilities
├── app.py               # Main application
├── start.py             # Startup script
├── test_backend.py      # Test script
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

### Adding New Features

1. **Create Models**: Add new models in `models/` directory
2. **Add Routes**: Create new API routes in `api/` directory
3. **Update Eel**: Add new Eel functions in `app.py`
4. **Test**: Use the test script to verify functionality

## Security Notes

- **Never commit your `.env` file** to version control
- **Use strong JWT secrets** in production
- **Restrict MongoDB Atlas network access** in production
- **Use HTTPS** in production environments

## Production Deployment

For production deployment:

1. **Environment Variables**: Set proper production values
2. **Database**: Use production MongoDB Atlas cluster
3. **Security**: Enable proper authentication and authorization
4. **HTTPS**: Use SSL/TLS certificates
5. **Monitoring**: Set up logging and monitoring

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the test script: `python test_backend.py`
3. Check the application logs for error messages
4. Verify your MongoDB Atlas configuration

---

**Happy coding! 🚀** 