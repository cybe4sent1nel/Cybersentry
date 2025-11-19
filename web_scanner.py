#!/usr/bin/env python3
"""
Comprehensive Web Application Vulnerability Scanner
Educational Purpose - Use only on authorized targets
"""

import requests
import socket
import ssl
import subprocess
import json
import time
from urllib.parse import urlparse
import argparse

class WebVulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.results = {
            'reconnaissance': {},
            'port_scan': {},
            'web_analysis': {},
            'vulnerabilities': {},
            'ssl_analysis': {}
        }
    
    def print_banner(self):
        print("=" * 60)
        print("     Professional Web Vulnerability Scanner")
        print("=" * 60)
        print(f"Target: {self.target}")
        print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def get_domain_info(self):
        """Basic domain and DNS information gathering"""
        print("[+] Gathering domain information...")
        
        try:
            # Get IP address
            ip = socket.gethostbyname(self.target.replace('https://', '').replace('http://', '').split('/')[0])
            print(f"    IP Address: {ip}")
            
            # Check if target is up
            try:
                response = requests.head(f"https://{self.target}", timeout=10, verify=False)
                print(f"    HTTPS Status: {response.status_code}")
                https_up = True
            except:
                https_up = False
            
            try:
                response = requests.head(f"http://{self.target}", timeout=10)
                print(f"    HTTP Status: {response.status_code}")
                http_up = True
            except:
                http_up = False
                
            self.results['reconnaissance'] = {
                'ip': ip,
                'https_up': https_up,
                'http_up': http_up
            }
            
        except Exception as e:
            print(f"    Error in domain info: {e}")
    
    def port_scan(self):
        """Basic port scanning"""
        print("[+] Scanning common ports...")
        
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 8080, 8443]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target.replace('https://', '').replace('http://', '').split('/')[0], port))
                if result == 0:
                    open_ports.append(port)
                    print(f"    Port {port}/tcp open")
                sock.close()
            except:
                pass
        
        self.results['port_scan']['open_ports'] = open_ports
        print(f"    Found {len(open_ports)} open ports")
    
    def web_technology_detection(self):
        """Detect web technologies"""
        print("[+] Analyzing web technologies...")
        
        try:
            response = requests.get(f"https://{self.target}", timeout=10, verify=False)
            
            # Extract headers
            headers = dict(response.headers)
            print("    Server Header:", headers.get('Server', 'Not found'))
            print("    X-Powered-By:", headers.get('X-Powered-By', 'Not found'))
            
            # Check for common technologies
            content = response.text.lower()
            technologies = []
            
            if 'wordpress' in content:
                technologies.append('WordPress')
            if 'drupal' in content:
                technologies.append('Drupal')
            if 'joomla' in content:
                technologies.append('Joomla')
            if 'nginx' in headers.get('Server', '').lower():
                technologies.append('Nginx')
            if 'apache' in headers.get('Server', '').lower():
                technologies.append('Apache')
            if 'iis' in headers.get('Server', '').lower():
                technologies.append('IIS')
            
            print("    Detected Technologies:", ', '.join(technologies) if technologies else 'None detected')
            
            self.results['web_analysis'] = {
                'headers': headers,
                'technologies': technologies,
                'status_code': response.status_code,
                'content_length': len(response.content)
            }
            
        except Exception as e:
            print(f"    Error in web analysis: {e}")
    
    def ssl_analysis(self):
        """SSL/TLS analysis"""
        print("[+] Analyzing SSL/TLS configuration...")
        
        try:
            hostname = self.target.replace('https://', '').replace('http://', '').split('/')[0]
            
            # Create SSL context
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    print(f"    SSL Version: {ssock.version()}")
                    print(f"    Cipher: {ssock.cipher()[0]}")
                    
                    if cert:
                        print(f"    Issuer: {cert.get('issuer', [{}])[0].get('CN', 'Unknown')}")
                        print(f"    Subject: {cert.get('subject', [{}])[0].get('CN', 'Unknown')}")
                        
                        # Check expiration
                        from datetime import datetime
                        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (not_after - datetime.now()).days
                        print(f"    Days until expiry: {days_until_expiry}")
                        
                        self.results['ssl_analysis'] = {
                            'ssl_version': ssock.version(),
                            'cipher': ssock.cipher()[0],
                            'issuer': cert.get('issuer', [{}])[0].get('CN', 'Unknown'),
                            'subject': cert.get('subject', [{}])[0].get('CN', 'Unknown'),
                            'days_until_expiry': days_until_expiry
                        }
                    
        except Exception as e:
            print(f"    SSL analysis error: {e}")
    
    def vulnerability_checks(self):
        """Basic vulnerability checks"""
        print("[+] Running vulnerability checks...")
        
        checks = []
        
        try:
            # Test for common vulnerabilities
            url = f"https://{self.target}"
            
            # Check for directory traversal
            traversal_test = requests.get(f"{url}/../../../etc/passwd", timeout=10, verify=False)
            if "root:x:0:0" in traversal_test.text:
                checks.append("CRITICAL: Directory Traversal vulnerability detected")
            
            # Check for SQL Injection in error messages
            sqli_test = requests.get(f"{url}/?id=1'", timeout=10, verify=False)
            if "syntax error" in sqli_test.text.lower() or "mysql" in sqli_test.text.lower():
                checks.append("WARNING: Possible SQL Injection vulnerability")
            
            # Check for XSS
            xss_test = requests.get(f"{url}/?q=<script>alert('xss')</script>", timeout=10, verify=False)
            if "<script>alert('xss')</script>" in xss_test.text:
                checks.append("WARNING: Reflected XSS vulnerability detected")
            
            # Check for open admin panels
            admin_paths = ['/admin', '/wp-admin', '/administrator', '/login', '/phpmyadmin']
            for path in admin_paths:
                try:
                    response = requests.get(f"{url}{path}", timeout=5, verify=False)
                    if response.status_code == 200:
                        checks.append(f"INFO: Open admin panel found at {path}")
                except:
                    pass
            
            # Check for sensitive files
            sensitive_files = ['/robots.txt', '/sitemap.xml', '/.env', '/backup.zip']
            for file in sensitive_files:
                try:
                    response = requests.get(f"{url}{file}", timeout=5, verify=False)
                    if response.status_code == 200:
                        if file in ['/.env', '/backup.zip']:
                            checks.append(f"CRITICAL: Sensitive file exposed: {file}")
                        else:
                            checks.append(f"INFO: Configuration file found: {file}")
                except:
                    pass
            
            print(f"    Found {len(checks)} potential issues")
            for check in checks:
                print(f"    {check}")
                
            self.results['vulnerabilities'] = checks
            
        except Exception as e:
            print(f"    Error in vulnerability checks: {e}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        print("\n" + "=" * 60)
        print("           VULNERABILITY ASSESSMENT REPORT")
        print("=" * 60)
        
        print("\n[RECONNAISSANCE]")
        recon = self.results['reconnaissance']
        print(f"Target IP: {recon.get('ip', 'Unknown')}")
        print(f"HTTPS Available: {'Yes' if recon.get('https_up') else 'No'}")
        print(f"HTTP Available: {'Yes' if recon.get('http_up') else 'No'}")
        
        print("\n[PORT SCAN]")
        ports = self.results['port_scan'].get('open_ports', [])
        print(f"Open Ports: {', '.join(map(str, ports)) if ports else 'None found'}")
        
        print("\n[WEB ANALYSIS]")
        web = self.results['web_analysis']
        print(f"Status Code: {web.get('status_code', 'Unknown')}")
        print(f"Content Length: {web.get('content_length', 'Unknown')}")
        print(f"Server Header: {web.get('headers', {}).get('Server', 'Not found')}")
        print(f"Technologies: {', '.join(web.get('technologies', [])) if web.get('technologies') else 'None detected'}")
        
        print("\n[SSL ANALYSIS]")
        ssl_info = self.results['ssl_analysis']
        print(f"SSL Version: {ssl_info.get('ssl_version', 'Unknown')}")
        print(f"Cipher: {ssl_info.get('cipher', 'Unknown')}")
        print(f"Certificate Issuer: {ssl_info.get('issuer', 'Unknown')}")
        print(f"Days until expiry: {ssl_info.get('days_until_expiry', 'Unknown')}")
        
        print("\n[VULNERABILITIES]")
        vulns = self.results['vulnerabilities']
        if vulns:
            for vuln in vulns:
                severity = vuln.split(':')[0]
                description = vuln.split(':')[1].strip()
                print(f"{severity}: {description}")
        else:
            print("No vulnerabilities detected")
        
        print("\n" + "=" * 60)
        print("Scan completed. Review findings and verify manually.")
        print("=" * 60)
        
        # Save detailed report
        with open('vulnerability_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        print("\nDetailed report saved to: vulnerability_report.json")

def main():
    parser = argparse.ArgumentParser(description='Web Vulnerability Scanner')
    parser.add_argument('target', help='Target domain (e.g., example.com)')
    args = parser.parse_args()
    
    scanner = WebVulnerabilityScanner(args.target)
    scanner.print_banner()
    
    # Run scans
    scanner.get_domain_info()
    scanner.port_scan()
    scanner.web_technology_detection()
    scanner.ssl_analysis()
    scanner.vulnerability_checks()
    
    # Generate report
    scanner.generate_report()

if __name__ == "__main__":
    main()
