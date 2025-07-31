from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask import jsonify
from functools import wraps
from models.models import User, db

def generate_tokens(user_id):
    """Generate access and refresh tokens for a user"""
    # Convert user_id to string as required by Flask-JWT-Extended
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }

def get_current_user():
    """Get current user from JWT token"""
    try:
        current_user_id = get_jwt_identity()
        print(f"🔍 JWT Debug: Got user ID from token: {current_user_id}")
        if current_user_id:
            # Convert string back to int for database query
            user = User.query.get(int(current_user_id))
            print(f"🔍 JWT Debug: Found user: {user.email if user else 'None'}")
            return user
        return None
    except Exception as e:
        print(f"🔍 JWT Debug: Error getting current user: {e}")
        return None

def jwt_required_with_user(f):
    """Custom decorator that requires JWT and returns current user"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        return f(current_user, *args, **kwargs)
    return decorated

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"
