#!/usr/bin/env python3
import requests

def verify_auth_page_content():
    print("🔍 VERIFYING AUTH PAGE CONTENT - NO GIMMICKS")
    print("=" * 60)
    
    target = "https://uplinkai.in/auth"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test original auth page
    print("1. Testing original auth page:")
    try:
        response = session.get(target, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Content Length: {len(response.text)} bytes")
        
        # Extract actual page title
        import re
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
        if title_match:
            print(f"   📄 Page Title: '{title_match.group(1).strip()}'")
        else:
            print("   📄 No title found")
            
        # Check for actual admin/dashboard indicators in content
        admin_keywords = ['admin', 'dashboard', 'panel', 'management', 'control']
        found_in_content = []
        
        for keyword in admin_keywords:
            if keyword in response.text.lower():
                # Find the line containing the keyword
                lines = response.text.split('\n')
                for line in lines:
                    if keyword in line.lower():
                        found_in_content.append(f"{keyword}: {line.strip()}")
                        break
        
        if found_in_content:
            print("   🔍 Content Analysis:")
            for item in found_in_content[:3]:  # Show first 3 matches
                print(f"      {item}")
        else:
            print("   ✅ No admin content found in auth page")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test bypass parameters
    print("\n2. Testing bypass parameters with content verification:")
    
    bypass_params = [
        '?admin=true&bypass=1',
        '?debug=true&admin=1',
        '?user=admin&access=granted'
    ]
    
    for param in bypass_params:
        try:
            print(f"\n   Testing: {param}")
            test_url = target + param
            response = session.get(test_url, timeout=10)
            
            print(f"     Status: {response.status_code}")
            print(f"     Length: {len(response.text)}")
            
            # Check if content actually changed
            if len(response.text) != len(requests.get(target).text):
                print("     🚨 Content length changed!")
            else:
                print("     ✅ Content length unchanged")
            
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                print(f"     📄 Title: '{title}'")
                
                # Check if title indicates admin access
                if any(keyword in title.lower() for keyword in ['admin', 'dashboard', 'panel']):
                    print("     🚨 ADMIN TITLE DETECTED!")
                else:
                    print("     ✅ Normal title")
            else:
                print("     📄 No title found")
            
            # Check for specific admin content indicators
            admin_lines = []
            lines = response.text.split('\n')
            for line in lines:
                if any(keyword in line.lower() for keyword in ['admin', 'dashboard', 'welcome']):
                    admin_lines.append(line.strip())
            
            if admin_lines:
                print(f"     🚨 Found {len(admin_lines)} admin-related lines:")
                for line in admin_lines[:2]:  # Show first 2
                    print(f"        {line[:100]}...")
            else:
                print("     ✅ No admin content lines found")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    # Test actual admin pages for comparison
    print("\n3. Testing actual admin pages for comparison:")
    
    admin_pages = ['/admin', '/dashboard']
    
    for page in admin_pages:
        try:
            print(f"\n   Testing: {page}")
            response = session.get(f"https://uplinkai.in{page}", timeout=10)
            
            print(f"     Status: {response.status_code}")
            print(f"     Length: {len(response.text)}")
            
            # Extract title
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                print(f"     📄 Title: '{title}'")
                
                # Check if this is actually an admin page
                if any(keyword in title.lower() for keyword in ['admin', 'dashboard']):
                    print("     ✅ This is a real admin page!")
                else:
                    print("     ❓ Not clearly an admin page")
            
        except Exception as e:
            print(f"     ❌ Error: {e}")

if __name__ == "__main__":
    verify_auth_page_content()
