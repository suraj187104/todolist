from google.auth.transport import requests
from google.oauth2 import id_token
import requests as http_requests
from flask import current_app

def verify_google_token(token):
    """Verify Google OAuth token and return user info"""
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            current_app.config['GOOGLE_CLIENT_ID']
        )
        
        # Check if token is valid and from correct issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        # Extract user information
        user_info = {
            'google_id': idinfo['sub'],
            'email': idinfo['email'],
            'first_name': idinfo.get('given_name', ''),
            'last_name': idinfo.get('family_name', ''),
            'profile_picture': idinfo.get('picture', ''),
            'email_verified': idinfo.get('email_verified', False)
        }
        
        return user_info
        
    except ValueError as e:
        print(f"Token verification failed: {e}")
        return None
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        return None

def get_google_user_info(access_token):
    """Get user info from Google using access token"""
    try:
        response = http_requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                'google_id': user_data.get('id'),
                'email': user_data.get('email'),
                'first_name': user_data.get('given_name', ''),
                'last_name': user_data.get('family_name', ''),
                'profile_picture': user_data.get('picture', ''),
                'email_verified': user_data.get('verified_email', False)
            }
        else:
            print(f"Failed to get user info: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error getting Google user info: {e}")
        return None
