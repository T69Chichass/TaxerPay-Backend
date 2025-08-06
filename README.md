# TaxerPay Backend

A Python-based backend for the TaxerPay application with MongoDB Atlas integration and Eel for frontend communication.

## Features

- 🔐 **Authentication System** - JWT-based user authentication
- 💾 **MongoDB Atlas Integration** - Cloud database for data persistence
- 🧮 **Tax Calculation Engine** - Federal tax bracket calculations
- 📊 **Tax Record Management** - CRUD operations for tax records
- 🌐 **Eel Integration** - Seamless Python-JavaScript communication
- 🔌 **RESTful API** - Flask-based API endpoints
- 🔒 **Security** - Password hashing, JWT tokens, CORS support

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account
- Node.js (for frontend)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TaxerPay-Backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your MongoDB Atlas credentials
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/taxerpay?retryWrites=true&w=majority
   DATABASE_NAME=taxerpay
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   HOST=localhost
   PORT=8000
   FRONTEND_PATH=../frontend/build
   ```

4. **Set up MongoDB Atlas**
   - Create a MongoDB Atlas account
   - Create a new cluster
   - Get your connection string
   - Update the `MONGODB_URI` in your `.env` file

## Running the Application

### Development Mode
```bash
python app.py
```

### Production Mode
```bash
# Set environment variables for production
export FLASK_ENV=production
python app.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Tax Management
- `POST /api/tax/records` - Create a new tax record
- `GET /api/tax/records` - Get all tax records for user
- `GET /api/tax/records/<id>` - Get specific tax record
- `PUT /api/tax/records/<id>` - Update tax record
- `DELETE /api/tax/records/<id>` - Delete tax record
- `POST /api/tax/calculate` - Calculate tax based on income

### System
- `GET /api/health` - Health check
- `GET /api` - API information

## Eel Functions

The backend exposes several Python functions to the frontend via Eel:

- `python_function()` - Example function
- `get_user_data(user_id)` - Get user data
- `create_tax_record_python(tax_data)` - Create tax record
- `calculate_tax_python(income, tax_type)` - Calculate tax

## Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "password": "hashed_string",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "address": "object",
  "tax_id": "string",
  "user_type": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Tax Records Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "tax_year": "number",
  "income": "number",
  "tax_type": "string",
  "deductions": "number",
  "credits": "number",
  "calculated_tax": "number",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Frontend Integration

The backend is designed to work with the React frontend. To connect:

1. **Build the frontend**
   ```bash
   cd ../frontend
   npm run build
   ```

2. **Start the backend**
   ```bash
   cd ../TaxerPay-Backend
   python app.py
   ```

3. **Access the application**
   - Eel mode: Automatically opens in Chrome
   - API mode: Access via `http://localhost:8000/api`

## Security Features

- **Password Hashing** - bcrypt for secure password storage
- **JWT Tokens** - Secure authentication tokens
- **CORS Support** - Cross-origin resource sharing
- **Input Validation** - Request data validation
- **Error Handling** - Comprehensive error management

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
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. **Create new models** in the `models/` directory
2. **Add API routes** in the `api/` directory
3. **Update Eel functions** in `app.py` if needed
4. **Test endpoints** using tools like Postman or curl

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Check your MongoDB Atlas connection string
   - Ensure your IP is whitelisted in Atlas
   - Verify network connectivity

2. **Eel Not Starting**
   - Ensure the frontend build directory exists
   - Check if Chrome is installed
   - Try running in Flask-only mode

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment

### Logs

The application provides detailed logging for debugging:
- Database connection status
- API request/response logs
- Error messages with stack traces

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 