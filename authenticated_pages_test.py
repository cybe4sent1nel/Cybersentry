import requests
import json
import time

# Test for pages that might require authentication but are accessible
def test_authenticated_pages():
    print("=== Testing Pages That Should Require Authentication ===")
    
    # Test various authenticated paths
    authenticated_paths = [
        "/index.html",  # Main app page
        "/app",         # App directory
        "/user",        # User directory
        "/profile",     # Profile page
        "/settings",    # Settings page
        "/api",         # API endpoints
        "/admin/api",   # Admin API
        "/user/data",   # User data
        "/admin/panel", # Admin panel
        "/staff/portal", # Staff portal
        "/internal/api", # Internal API
        "/secure",      # Secure area
        "/private",     # Private area
    ]
    
    base_url = "https://uplinkai.in"
    
    for path in authenticated_paths:
        try:
            full_url = f"{base_url}{path}"
            response = requests.get(full_url, allow_redirects=False)
            
            if response.status_code == 200:
                print(f"✅ {path}: ACCESSIBLE (200)")
                content = response.text
                # Check for Firebase auth requirements
                if 'auth' in content.lower() or 'signin' in content.lower():
                    print(f"   ℹ️  Contains auth references")
                else:
                    print(f"   ⚠️  No authentication requirement detected!")
                    
            elif response.status_code == 302:
                print(f"🔄 {path}: REDIRECT ({response.status_code})")
                if 'location' in response.headers:
                    print(f"   Redirects to: {response.headers['location']}")
            else:
                print(f"❌ {path}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {path}: Error - {e}")

# Test for direct access to the main application
def test_main_app_access():
    print("\n=== Testing Main Application Access ===")
    
    # Try to access the main app without authentication
    main_app_urls = [
        "https://uplinkai.in/index.html",
        "https://uplinkai.in/app.html", 
        "https://uplinkai.in/dashboard.html",
        "https://uplinkai.in/user.html",
        "https://uplinkai.in/profile.html"
    ]
    
    for url in main_app_urls:
        try:
            response = requests.get(url, allow_redirects=False)
            print(f"{url}: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                # Look for Firebase auth checks
                auth_patterns = [
                    'auth.currentUser',
                    'firebase.auth',
                    'onAuthStateChanged',
                    'signInWithEmailAndPassword'
                ]
                
                has_auth_check = any(pattern in content for pattern in auth_patterns)
                if not has_auth_check:
                    print(f"   ⚠️  No Firebase auth check found!")
                else:
                    print(f"   ℹ️  Contains Firebase auth code")
                    
        except Exception as e:
            print(f"Error testing {url}: {e}")

if __name__ == "__main__":
    test_authenticated_pages()
    test_main_app_access()
