import requests
import json
import time

# Test for authentication bypass in the main auth page
def test_auth_bypass():
    print("=== Testing Authentication Bypass in Main Auth Page ===")
    
    auth_url = "https://uplinkai.in/auth"
    
    # Test 1: Check if we can access authenticated content without login
    try:
        # First, let's see if there are any cookies or session tokens
        response = requests.get(auth_url, allow_redirects=False)
        print(f"Auth page status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        # Check for any hidden admin paths or direct access
        if response.status_code == 200:
            content = response.text
            print("Looking for hidden admin paths...")
            
            # Search for any hardcoded admin paths or tokens
            admin_patterns = [
                r'admin.*\.html',
                r'dashboard.*\.html', 
                r'panel.*\.html',
                r'control.*\.html',
                r'management.*\.html'
            ]
            
            for pattern in admin_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"Found potential admin paths: {matches}")
        
    except Exception as e:
        print(f"Error testing auth bypass: {e}")

# Test for direct access to authenticated pages
def test_direct_access():
    print("\n=== Testing Direct Access to Admin Pages ===")
    
    admin_pages = [
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
    
    for page in admin_pages:
        try:
            full_url = f"{base_url}{page}"
            response = requests.get(full_url, allow_redirects=False)
            
            if response.status_code == 200:
                print(f"✅ {page}: ACCESSIBLE (200)")
                
                # Check if the page contains authentication requirements
                content = response.text.lower()
                auth_keywords = ['login required', 'authentication', 'sign in', 'auth']
                
                auth_required = any(keyword in content for keyword in auth_keywords)
                if not auth_required:
                    print(f"   ⚠️  No authentication check found!")
                    
            elif response.status_code == 302:
                print(f"🔄 {page}: REDIRECT ({response.status_code})")
                if 'location' in response.headers:
                    print(f"   Redirects to: {response.headers['location']}")
            else:
                print(f"❌ {page}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {page}: Error - {e}")

if __name__ == "__main__":
    test_auth_bypass()
    test_direct_access()
