import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AuthUtils:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
    
    def generate_token(self, user_data):
        """Generate JWT token for user"""
        try:
            payload = {
                'user_id': user_data.get('_id'),
                'email': user_data.get('email'),
                'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
            
        except Exception as e:
            print(f"Error generating token: {e}")
            return None
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None
    
    def decode_token(self, token):
        """Decode JWT token without verification (for debugging)"""
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None

# Create a global auth utils instance
auth_utils = AuthUtils() 