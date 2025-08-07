# 🌾 Farmer Land Tax Payment System

A comprehensive system for farmers to pay their land taxes with separate authentication for farmers and administrators.

## 🎯 **System Overview**

### **User Types:**
1. **🌾 Farmers (Taxpayers)** - Login with PAN Card ID + Password
2. **👨‍💼 Admins** - Login with Employee ID + Password

### **Database Collections:**
- `farmers` - Farmer accounts and details
- `admins` - Admin accounts and permissions
- `tax_records` - Tax payment records

## 🚀 **Quick Start**

### **1. Setup Environment**
```bash
cd TaxerPay-Backend
pip install -r requirements.txt
```

### **2. Configure Database**
Create a `.env` file with your MongoDB Atlas credentials:
```env
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=taxerpay
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
HOST=localhost
PORT=8000
```

### **3. Populate Test Data**
```bash
python populate_test_data.py
```

### **4. Start Backend**
```bash
python app.py
```

## 📋 **Test Credentials**

### **🌾 Farmers (PAN + Password):**
| PAN Card | Password | Name |
|----------|----------|------|
| ABCDE1234F | farmer123 | Rajesh Patel |
| FGHIJ5678K | farmer456 | Lakshmi Devi |
| KLMNO9012P | farmer789 | Suresh Kumar |
| PQRST3456U | farmer012 | Meera Singh |
| UVWXY6789Z | farmer345 | Amit Shah |

### **👨‍💼 Admins (Employee ID + Password):**
| Employee ID | Password | Name | Department |
|-------------|----------|------|------------|
| ADMIN001 | admin123 | Ramesh Kumar | Tax Collection |
| ADMIN002 | admin456 | Priya Sharma | Farmer Relations |
| ADMIN003 | admin789 | Vikram Patel | IT Support |
| ADMIN004 | admin012 | Sunita Verma | Finance |
| ADMIN005 | admin345 | Arjun Singh | Field Operations |

## 🔗 **API Endpoints**

### **Farmer Authentication**
- `POST /api/farmer/register` - Register new farmer
- `POST /api/farmer/login` - Farmer login (PAN + Password)
- `GET /api/farmer/profile` - Get farmer profile
- `PUT /api/farmer/profile` - Update farmer profile

### **Admin Authentication**
- `POST /api/admin/register` - Register new admin
- `POST /api/admin/login` - Admin login (Employee ID + Password)
- `GET /api/admin/profile` - Get admin profile
- `PUT /api/admin/profile` - Update admin profile
- `GET /api/admin/farmers` - Get all farmers (admin only)

### **Tax Management**
- `POST /api/tax/records` - Create tax record
- `GET /api/tax/records` - Get tax records
- `PUT /api/tax/records/<id>` - Update tax record
- `DELETE /api/tax/records/<id>` - Delete tax record
- `POST /api/tax/calculate` - Calculate tax

### **System**
- `GET /` - Backend status
- `GET /api` - API documentation
- `GET /api/health` - Health check

## 📊 **Database Schema**

### **Farmers Collection**
```json
{
  "_id": "ObjectId",
  "pan_card": "ABCDE1234F",
  "password": "hashed_password",
  "first_name": "Rajesh",
  "last_name": "Patel",
  "phone": "+91-9876543210",
  "email": "rajesh.patel@email.com",
  "address": {
    "street": "Farm House No. 45",
    "village": "Patel Nagar",
    "district": "Ahmedabad",
    "state": "Gujarat",
    "pincode": "380001"
  },
  "land_details": {
    "total_acres": 25.5,
    "irrigated_acres": 20.0,
    "crop_type": "Wheat, Cotton"
  },
  "bank_details": {
    "account_number": "1234567890",
    "bank_name": "State Bank of India",
    "ifsc_code": "SBIN0001234"
  },
  "user_type": "farmer",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### **Admins Collection**
```json
{
  "_id": "ObjectId",
  "employee_id": "ADMIN001",
  "password": "hashed_password",
  "first_name": "Ramesh",
  "last_name": "Kumar",
  "phone": "+91-9876543211",
  "email": "ramesh.kumar@taxerpay.gov.in",
  "department": "Tax Collection",
  "designation": "Senior Tax Officer",
  "address": {
    "street": "Government Quarters No. 15",
    "city": "Gandhinagar",
    "state": "Gujarat",
    "pincode": "382001"
  },
  "permissions": ["view_farmers", "edit_farmers", "view_taxes", "collect_taxes", "generate_reports"],
  "user_type": "admin",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🧪 **Testing**

### **Test Models**
```bash
python test_setup.py
```

### **Test API Endpoints**

#### **Farmer Login:**
```bash
curl -X POST http://localhost:8000/api/farmer/login \
  -H "Content-Type: application/json" \
  -d '{
    "pan_card": "ABCDE1234F",
    "password": "farmer123"
  }'
```

#### **Admin Login:**
```bash
curl -X POST http://localhost:8000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "ADMIN001",
    "password": "admin123"
  }'
```

#### **Get All Farmers (Admin Only):**
```bash
curl -X GET http://localhost:8000/api/admin/farmers \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## 🔒 **Security Features**

- **Password Hashing** - bcrypt for secure password storage
- **JWT Tokens** - Secure authentication tokens
- **CORS Support** - Cross-origin resource sharing
- **Input Validation** - Request data validation
- **Role-based Access** - Different permissions for farmers and admins

## 🎨 **Frontend Integration**

The frontend can now use these endpoints:

### **Farmer Login:**
```javascript
const response = await fetch('/api/farmer/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    pan_card: 'ABCDE1234F',
    password: 'farmer123'
  })
});
```

### **Admin Login:**
```javascript
const response = await fetch('/api/admin/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    employee_id: 'ADMIN001',
    password: 'admin123'
  })
});
```

## 📁 **Project Structure**

```
TaxerPay-Backend/
├── api/
│   ├── auth_routes.py          # General authentication
│   ├── farmer_auth_routes.py   # Farmer authentication
│   ├── admin_auth_routes.py    # Admin authentication
│   └── tax_routes.py           # Tax management
├── models/
│   ├── user.py                 # General user model
│   ├── farmer.py               # Farmer model
│   ├── admin.py                # Admin model
│   └── tax_record.py           # Tax record model
├── config/
│   └── database.py             # Database connection
├── utils/
│   └── auth.py                 # Authentication utilities
├── app.py                      # Main application
├── populate_test_data.py       # Test data population
├── test_setup.py               # Model testing
└── requirements.txt            # Dependencies
```

## 🚀 **Next Steps**

1. **Frontend Integration** - Connect React frontend to these APIs
2. **Tax Calculation** - Implement land tax calculation logic
3. **Payment Integration** - Add payment gateway integration
4. **Reports** - Generate tax reports and analytics
5. **Notifications** - Add email/SMS notifications

## 🆘 **Troubleshooting**

### **Database Connection Issues:**
- Check MongoDB Atlas connection string
- Ensure IP is whitelisted in Atlas
- Verify network connectivity

### **Authentication Issues:**
- Check JWT secret key configuration
- Verify password hashing is working
- Ensure proper token format in requests

### **API Issues:**
- Check CORS configuration
- Verify request format and headers
- Check server logs for detailed errors

---

**🎉 Your Farmer Tax Payment System is ready!**
