import requests
import json
import time

# Test 1: Check if Firebase API endpoints are exposed
def test_firebase_api_exposure():
    print("=== Testing Firebase API Exposure ===")
    
    # Firebase REST API endpoints to test
    firebase_api_base = "https://identitytoolkit.googleapis.com/v1"
    api_key = "AIzaSyA0grBMnQ2VnDKD-Q8QFkA7cirthBYcmFY"
    
    # Test listAccounts endpoint (should be restricted)
    list_accounts_url = f"{firebase_api_base}/accounts:lookup?key={api_key}"
    
    # Test createAuthUri endpoint
    create_auth_uri_url = f"{firebase_api_base}/createAuthUri?key={api_key}"
    
    test_data = {
        "identifier": "admin@uplinkai.in",
        "continueUri": "https://uplinkai.in/auth"
    }
    
    try:
        response = requests.post(create_auth_uri_url, json=test_data, timeout=10)
        print(f"CreateAuthUri response: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing CreateAuthUri: {e}")
    
    # Test verifyPassword endpoint (legacy)
    verify_password_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
    
    test_login_data = {
        "email": "admin@uplinkai.in",
        "password": "admin123",
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(verify_password_url, json=test_login_data, timeout=10)
        print(f"VerifyPassword response: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing VerifyPassword: {e}")

# Test 2: Check for email enumeration
def test_email_enumeration():
    print("\n=== Testing Email Enumeration ===")
    
    test_emails = [
        "admin@uplinkai.in",
        "admin@gmail.com", 
        "test@uplinkai.in",
        "user@uplinkai.in",
        "admin@uplink.com"
    ]
    
    for email in test_emails:
        print(f"Testing email: {email}")
        # This would need to be done through the actual web interface
        # or via automated browser testing

# Test 3: Check for default credentials
def test_default_credentials():
    print("\n=== Testing Default Credentials ===")
    
    default_passwords = [
        "admin",
        "admin123", 
        "password",
        "password123",
        "123456",
        "uplinkai",
        "uplink",
        "admin@uplinkai",
        "admin2024",
        "welcome123"
    ]
    
    for password in default_passwords:
        print(f"Testing password: {password}")
        # This would need to be done through the actual web interface

if __name__ == "__main__":
    test_firebase_api_exposure()
    test_email_enumeration()
    test_default_credentials()
