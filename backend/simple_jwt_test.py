#!/usr/bin/env python3
"""
Simple JWT token test
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_jwt_simple():
    """Test JWT with a simple approach"""
    print("🔧 Simple JWT Test\n")
    
    # 1. Login to get token
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    
    print("1. Getting JWT token...")
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            print(response.json())
            return
        
        data = response.json()
        token = data.get('access_token')
        print(f"✅ Got token: {token[:20]}...")
        
        # 2. Test /health endpoint (no auth needed)
        print("\n2. Testing health endpoint...")
        health_response = requests.get(f'{BASE_URL}/health')
        print(f"Health status: {health_response.status_code}")
        
        # 3. Test protected endpoint with token
        print("\n3. Testing protected endpoint...")
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Try the /api/auth/me endpoint
        me_response = requests.get(f'{BASE_URL}/api/auth/me', headers=headers)
        print(f"Auth/me status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"✅ Success! User: {user_data.get('user', {}).get('email')}")
        else:
            print(f"❌ Failed: {me_response.json()}")
            
            # 4. Check what the server sees
            print("\n4. Server debug info:")
            print(f"Token length: {len(token)}")
            print(f"Token starts with: {token[:50]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_jwt_simple()
