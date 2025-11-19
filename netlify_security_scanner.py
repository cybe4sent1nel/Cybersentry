#!/usr/bin/env python3
import requests
import time
import re
from urllib.parse import urljoin, quote

class NetlifySecurityScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.vulnerabilities = []
        
    def log_vulnerability(self, vuln_type, description, severity, evidence, exploit_url=None):
        vuln = {
            'type': vuln_type,
            'description': description,
            'severity': severity,
            'evidence': evidence,
            'exploit_url': exploit_url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.vulnerabilities.append(vuln)
        print(f"\n🚨 {severity.upper()} VULNERABILITY FOUND!")
        print(f"Type: {vuln_type}")
        print(f"Description: {description}")
        print(f"Evidence: {evidence}")
        if exploit_url:
            print(f"Exploit URL: {exploit_url}")
        print("-" * 60)
        
    def test_netlify_admin_paths(self):
        print("🔍 TESTING NETLIFY ADMIN PATHS")
        print("=" * 60)
        
        # Test Netlify-specific admin paths
        netlify_admin_paths = [
            '/admin/',
            '/netlify-admin/',
            '/admin/index.html',
            '/admin/config.yml',
            '/admin/config.toml',
            '/netlify.toml',
            '/netlify.yml',
            '/_netlify/',
            '/.netlify/',
            '/admin/_redirects',
            '/admin/_headers',
            '/admin/.htaccess',
            '/admin/.env',
            '/admin/settings',
            '/admin/builds',
            '/admin/functions',
            '/admin/forms',
            '/admin/identity',
            '/admin/assets',
            '/admin/media',
            '/admin/collections',
            '/admin/collection',
            '/admin/entries',
            '/admin/users',
            '/admin/roles',
            '/admin/invites'
        ]
        
        for path in netlify_admin_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify Admin Access",
                        f"Accessible Netlify admin path: {path}",
                        "CRITICAL",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Check for admin content
                    admin_content = ['admin', 'dashboard', 'settings', 'build', 'deploy']
                    found_admin = []
                    for content in admin_content:
                        if content in response.text.lower():
                            found_admin.append(content)
                    
                    if found_admin:
                        print(f"   🚨 Admin content found: {found_admin}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def test_netlify_configuration_files(self):
        print("\n⚙️ TESTING NETLIFY CONFIGURATION FILES")
        print("=" * 60)
        
        # Test for Netlify configuration files
        config_files = [
            '/netlify.toml',
            '/netlify.yml',
            '/.netlify.toml',
            '/.netlify.yml',
            '/admin/config.yml',
            '/admin/config.toml',
            '/static/admin/config.yml',
            '/src/admin/config.yml',
            '/public/admin/config.yml',
            '/content/admin/config.yml',
            '/dist/admin/config.yml'
        ]
        
        for file_path in config_files:
            try:
                url = self.target_url + file_path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify Configuration Exposure",
                        f"Exposed Netlify config file: {file_path}",
                        "HIGH",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Extract sensitive information from config
                    content = response.text
                    secrets = []
                    
                    # Look for API keys
                    api_keys = re.findall(r'(api[_-]?key|apikey)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)
                    if api_keys:
                        secrets.extend([f"API Key: {key[1][:10]}..." for key in api_keys])
                    
                    # Look for tokens
                    tokens = re.findall(r'(token|auth[_-]?token)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)
                    if tokens:
                        secrets.extend([f"Token: {token[1][:10]}..." for token in tokens])
                    
                    # Look for secrets
                    secrets_pattern = re.findall(r'(secret|password|pwd)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)
                    if secrets_pattern:
                        secrets.extend([f"Secret: {secret[1][:10]}..." for secret in secrets_pattern])
                    
                    if secrets:
                        print(f"   🚨 Secrets found: {secrets[:3]}")
                        
            except Exception as e:
                print(f"Error testing {file_path}: {e}")
    
    def test_netlify_build_logs(self):
        print("\n📊 TESTING NETLIFY BUILD LOGS")
        print("=" * 60)
        
        # Test for build logs and deployment information
        build_paths = [
            '/admin/builds',
            '/admin/logs',
            '/admin/deploy',
            '/admin/deployments',
            '/admin/build-logs',
            '/admin/build-log',
            '/admin/.cache/logs',
            '/admin/.cache/build',
            '/admin/cache/logs',
            '/admin/cache/build'
        ]
        
        for path in build_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify Build Information Disclosure",
                        f"Accessible build information: {path}",
                        "MEDIUM",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Look for deployment secrets
                    content = response.text
                    deployment_secrets = []
                    
                    # Look for deployment tokens
                    deploy_tokens = re.findall(r'(deploy[_-]?token|deployment[_-]?token)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)
                    if deploy_tokens:
                        deployment_secrets.extend([f"Deploy Token: {token[1][:10]}..." for token in deploy_tokens])
                    
                    # Look for build environment variables
                    env_vars = re.findall(r'(ENV_[A-Z_]+)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content)
                    if env_vars:
                        deployment_secrets.extend([f"Env Var: {var[0]}={var[1][:10]}..." for var in env_vars[:3]])
                    
                    if deployment_secrets:
                        print(f"   🚨 Deployment secrets found: {deployment_secrets}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def test_netlify_identity_and_forms(self):
        print("\n🔐 TESTING NETLIFY IDENTITY AND FORMS")
        print("=" * 60)
        
        # Test for Netlify Identity and Forms access
        identity_paths = [
            '/admin/identity',
            '/admin/users',
            '/admin/invites',
            '/admin/forms',
            '/admin/submissions',
            '/admin/entries',
            '/.netlify/identity',
            '/.netlify/identity.html',
            '/admin/.netlify/identity',
            '/admin/users.csv',
            '/admin/users.json',
            '/admin/forms.csv',
            '/admin/forms.json'
        ]
        
        for path in identity_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify Identity/Data Exposure",
                        f"Accessible identity/data path: {path}",
                        "CRITICAL",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Look for user data
                    content = response.text
                    user_data = []
                    
                    # Look for emails
                    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)
                    if emails:
                        user_data.extend([f"Email: {email}" for email in emails[:3]])
                    
                    # Look for usernames
                    usernames = re.findall(r'(username|user)["\']?\s*[:=]\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)
                    if usernames:
                        user_data.extend([f"Username: {user[1]}" for user in usernames[:3]])
                    
                    if user_data:
                        print(f"   🚨 User data found: {user_data}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def test_netlify_functions_and_edge(self):
        print("\n⚡ TESTING NETLIFY FUNCTIONS AND EDGE")
        print("=" * 60)
        
        # Test for Netlify Functions and Edge handlers
        function_paths = [
            '/.netlify/functions/',
            '/.netlify/functions.json',
            '/admin/functions/',
            '/admin/functions.json',
            '/netlify/functions/',
            '/netlify/functions.json',
            '/api/functions/',
            '/api/edge/',
            '/.netlify/edge-functions/',
            '/admin/edge/'
        ]
        
        for path in function_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify Functions Access",
                        f"Accessible functions path: {path}",
                        "HIGH",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Look for function secrets
                    content = response.text
                    function_secrets = []
                    
                    # Look for function environment variables
                    func_env = re.findall(r'(process\.env\.[A-Z_]+|functions?\.[\w_]+)', content)
                    if func_env:
                        function_secrets.extend([f"Function var: {var}" for var in func_env[:3]])
                    
                    # Look for API endpoints in functions
                    api_endpoints = re.findall(r'(fetch|axios|request)\(["\']([^"\']+)', content)
                    if api_endpoints:
                        function_secrets.extend([f"API Endpoint: {endpoint[1]}" for endpoint in api_endpoints[:3]])
                    
                    if function_secrets:
                        print(f"   🚨 Function secrets found: {function_secrets}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def test_netlify_environment_disclosure(self):
        print("\n🌍 TESTING NETLIFY ENVIRONMENT DISCLOSURE")
        print("=" * 60)
        
        # Test for environment variables and deployment info
        env_disclosure_paths = [
            '/admin/env',
            '/admin/environment',
            '/admin/.env',
            '/admin/deploy.env',
            '/admin/build.env',
            '/.env.production',
            '/.env.staging',
            '/.env.local',
            '/admin/secrets',
            '/admin/keys',
            '/admin/tokens'
        ]
        
        for path in env_disclosure_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Environment Variables Disclosure",
                        f"Accessible environment data: {path}",
                        "CRITICAL",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Extract environment variables
                    content = response.text
                    env_vars = []
                    
                    # Look for various env variable patterns
                    env_patterns = [
                        r'(export\s+[\w_]+=["\']?[^"\'\s]+)',
                        r'([\w_]+=["\']?[^"\'\s]+)',
                        r'(process\.env\.([\w_]+))'
                    ]
                    
                    for pattern in env_patterns:
                        matches = re.findall(pattern, content)
                        for match in matches[:5]:  # Limit to first 5 matches
                            env_vars.append(f"Env: {str(match)[:50]}")
                    
                    if env_vars:
                        print(f"   🚨 Environment variables found: {env_vars[:3]}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def test_netlify_cms_access(self):
        print("\n📝 TESTING NETLIFY CMS ACCESS")
        print("=" * 60)
        
        # Test for Netlify CMS access
        cms_paths = [
            '/admin/',
            '/admin/index.html',
            '/admin/config.yml',
            '/admin/collections/',
            '/admin/collections.json',
            '/admin/media/',
            '/admin/media-library',
            '/admin/editorial-workflow',
            '/admin/workflow',
            '/admin/collections/pages',
            '/admin/collections/posts',
            '/admin/collections/blog',
            '/admin/collections/products'
        ]
        
        for path in cms_paths:
            try:
                url = self.target_url + path
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    self.log_vulnerability(
                        "Netlify CMS Access",
                        f"Accessible CMS path: {path}",
                        "HIGH",
                        f"Status: {response.status_code}, Size: {len(response.text)} bytes",
                        url
                    )
                    
                    # Check for CMS content
                    content = response.text
                    cms_content = []
                    
                    # Look for collection data
                    if 'collection' in content.lower():
                        cms_content.append("Collection data found")
                    
                    # Look for media files
                    if 'media' in content.lower() or 'assets' in content.lower():
                        cms_content.append("Media files accessible")
                    
                    # Look for editorial workflow
                    if 'workflow' in content.lower() or 'editorial' in content.lower():
                        cms_content.append("Editorial workflow data found")
                    
                    if cms_content:
                        print(f"   🚨 CMS content found: {cms_content}")
                        
            except Exception as e:
                print(f"Error testing {path}: {e}")
    
    def run_netlify_security_scan(self):
        print("🚀 NETLIFY SECURITY SCANNING STARTED")
        print("=" * 80)
        print(f"Target: {self.target_url}")
        print("Specializing in Netlify-specific vulnerabilities and owner information")
        print("=" * 80)
        
        self.test_netlify_admin_paths()
        self.test_netlify_configuration_files()
        self.test_netlify_build_logs()
        self.test_netlify_identity_and_forms()
        self.test_netlify_functions_and_edge()
        self.test_netlify_environment_disclosure()
        self.test_netlify_cms_access()
        
        print("\n" + "=" * 80)
        print("🎯 NETLIFY SECURITY SCANNING COMPLETE")
        print("=" * 80)
        
        if self.vulnerabilities:
            print(f"\n🚨 FOUND {len(self.vulnerabilities)} NETLIFY-SPECIFIC VULNERABILITIES!")
            
            # Group by severity
            critical_vulns = [v for v in self.vulnerabilities if v['severity'] == 'CRITICAL']
            high_vulns = [v for v in self.vulnerabilities if v['severity'] == 'HIGH']
            medium_vulns = [v for v in self.vulnerabilities if v['severity'] == 'MEDIUM']
            
            print(f"\n📊 SUMMARY:")
            print(f"🔴 Critical: {len(critical_vulns)}")
            print(f"🟠 High: {len(high_vulns)}")
            print(f"🟡 Medium: {len(medium_vulns)}")
            
            print(f"\n🏆 TOP 5 MOST CRITICAL NETLIFY VULNERABILITIES:")
            for i, vuln in enumerate(sorted(self.vulnerabilities, key=lambda x: x['severity'], reverse=True)[:5], 1):
                print(f"\n{i}. {vuln['type']} ({vuln['severity']})")
                print(f"   Description: {vuln['description']}")
                print(f"   Evidence: {vuln['evidence']}")
                if vuln['exploit_url']:
                    print(f"   Exploit URL: {vuln['exploit_url']}")
        else:
            print("\n✅ No Netlify-specific vulnerabilities found.")
        
        return self.vulnerabilities

if __name__ == "__main__":
    target = "https://uplinkai.in/"
    scanner = NetlifySecurityScanner(target)
    vulnerabilities = scanner.run_netlify_security_scan()
