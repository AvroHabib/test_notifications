#!/usr/bin/env python
"""
Simple test script to verify the Django FCM Notification Backend API
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("🚀 Testing Django FCM Notification Backend API")
    print("=" * 50)
    
    # Test server health
    try:
        response = requests.get(f"{BASE_URL}/docs/")
        if response.status_code == 200:
            print("✅ Server is running and API documentation is accessible")
        else:
            print(f"❌ Server responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000")
        return
    
    # Test user registration
    print("\n📝 Testing user registration...")
    registration_data = {
        "phone_number": "+1987654321",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=registration_data)
        if response.status_code == 201:
            print("✅ User registration successful")
            user_data = response.json()
            print(f"   Created user: {user_data.get('phone_number')}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test user login
    print("\n🔐 Testing user login...")
    login_data = {
        "phone_number": "+1987654321",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if response.status_code == 200:
            print("✅ User login successful")
            tokens = response.json()
            access_token = tokens.get('access')
            print(f"   Got access token: {access_token[:50]}...")
            
            # Test authenticated endpoint
            headers = {"Authorization": f"Bearer {access_token}"}
            profile_response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
            if profile_response.status_code == 200:
                print("✅ Authenticated API call successful")
                profile = profile_response.json()
                print(f"   User profile: {profile.get('phone_number')}")
            else:
                print(f"❌ Profile request failed: {profile_response.status_code}")
                
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    print("\n🎉 API testing completed!")
    print("\n📚 Visit http://127.0.0.1:8000/api/docs/ for full API documentation")

if __name__ == "__main__":
    test_api()
