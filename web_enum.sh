#!/bin/bash
# Try web application enumeration since HTTP/HTTPS are available
echo "=== WEB APPLICATION ENUMERATION ==="

# Try to access HTTP service
echo "1. Testing HTTP service access..."
curl -I -m 10 http://10.201.70.249

echo -e "\n2. Testing HTTPS service access..."
curl -I -k -m 10 https://10.201.70.249

echo -e "\n3. Testing HTTP on port 8080..."
curl -I -m 10 http://10.201.70.249:8080

echo -e "\n4. Testing HTTPS on port 8443..."
curl -I -k -m 10 https://10.201.70.249:8443

echo -e "\n=== WEB ENUMERATION COMPLETE ==="
