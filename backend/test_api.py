#!/usr/bin/env python3
"""
Simple API test script
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_api():
    """Test basic API endpoints"""
    print("🧪 Testing TODO App API...\n")
    
    # Test health check
    print("1. Testing health check...")
    try:
        response = requests.get(f'{BASE_URL}/health')
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"API Version: {data.get('version')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test user registration or login
    print("\n3. Testing user authentication...")
    test_user = {
        'email': 'test@example.com',  # Use the sample user from setup_db.py
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    # Try registration first
    try:
        response = requests.post(
            f'{BASE_URL}/api/auth/register',
            json=test_user,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 201:
            print("✅ User registration successful")
            data = response.json()
            return data.get('access_token')
        elif response.status_code == 409:
            print("ℹ️ User already exists, trying login...")
            # User exists, try login
            login_data = {
                'email': test_user['email'],
                'password': test_user['password']
            }
            response = requests.post(
                f'{BASE_URL}/api/auth/login',
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print("✅ User login successful")
                data = response.json()
                token = data.get('access_token')
                print(f"🔍 Debug: Received token: {token[:50] if token else 'None'}...")
                return token
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(response.json())
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Authentication error: {e}")
    
    return None

def test_authenticated_endpoints(token):
    """Test endpoints that require authentication"""
    if not token:
        print("\nSkipping authenticated tests - no token available")
        return
    
    print(f"🔍 Debug: Using token: {token[:50] if token else 'None'}...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"🔍 Debug: Authorization header: {headers['Authorization'][:70]}...")
    
    # Test getting current user info
    print("\n4. Testing user profile...")
    try:
        response = requests.get(
            f'{BASE_URL}/api/auth/me',
            headers=headers
        )
        if response.status_code == 200:
            print("✅ User profile retrieval successful")
            user_data = response.json().get('user')
            print(f"User: {user_data.get('first_name')} {user_data.get('last_name')}")
        else:
            print(f"❌ User profile failed: {response.status_code}")
    except Exception as e:
        print(f"❌ User profile error: {e}")
    
    # Test creating a todo
    print("\n5. Testing todo creation...")
    todo_data = {
        'title': 'Test TODO from API',
        'description': 'This is a test TODO created via API',
        'priority': 'high'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/api/todos',
            json=todo_data,
            headers=headers
        )
        if response.status_code == 201:
            print("✅ TODO creation successful")
            todo = response.json().get('todo')
            print(f"Created TODO: {todo.get('title')}")
            return todo.get('id')
        else:
            print(f"❌ TODO creation failed: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ TODO creation error: {e}")
    
    # Test getting todos
    print("\n6. Testing todo retrieval...")
    try:
        response = requests.get(
            f'{BASE_URL}/api/todos',
            headers=headers
        )
        if response.status_code == 200:
            print("✅ TODO retrieval successful")
            todos_data = response.json()
            todos = todos_data.get('todos', [])
            print(f"Found {len(todos)} TODOs")
            for todo in todos[:3]:  # Show first 3 todos
                print(f"  - {todo.get('title')} (Priority: {todo.get('priority')})")
        else:
            print(f"❌ TODO retrieval failed: {response.status_code}")
    except Exception as e:
        print(f"❌ TODO retrieval error: {e}")
    
    return None

def main():
    """Run all tests"""
    token = test_api()
    test_authenticated_endpoints(token)
    print("\n🎉 API testing complete!")

if __name__ == '__main__':
    main()
