#!/bin/bash
# Install additional tools and continue enumeration
echo "Installing additional reconnaissance tools..."
sudo apt update

# Install tools that might not be available
sudo apt install -y nikto dirb gobuster sqlmap enum4linux smbclient

echo -e "\n=== CONTINUING RECONNAISSANCE ==="

# Try specific port scans
echo -e "\n1. Scanning specific high-value ports..."
nmap -Pn -sV -p 21,22,23,25,53,80,110,143,443,993,995,1433,3306,3389,5432,5900,8080,8443,10000 10.201.70.249

# Try UDP scan on common ports
echo -e "\n2. UDP scan on common ports..."
nmap -Pn -sU -p 53,161,162,631,1900 10.201.70.249

# Try service detection on any open ports found
echo -e "\n3. Service detection with version info..."
nmap -Pn -sV --version-all 10.201.70.249

# Try to identify the service/application
echo -e "\n4. Attempting to identify web services..."
nmap -Pn -p 80,443,8080,8443 --script http-headers,http-title,http-server-header 10.201.70.249

echo -e "\n=== RECONNAISSANCE COMPLETE ==="
