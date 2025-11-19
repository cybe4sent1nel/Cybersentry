#!/bin/bash
# Basic network reconnaissance script
echo "Starting network reconnaissance on 10.201.70.249"
echo "==============================================="

# Check if the host is up
echo "1. Checking if host is alive..."
ping -c 3 10.201.70.249

echo -e "\n2. Basic port scan..."
# Install nmap if not available
if ! command -v nmap &> /dev/null; then
    echo "Installing nmap..."
    sudo apt update && sudo apt install -y nmap
fi

# Quick scan for open ports
nmap -T4 -F 10.201.70.249

echo -e "\n3. Service version detection on common ports..."
# Scan common ports with version detection
nmap -sV -p 21,22,23,25,53,80,110,143,443,993,995,3306,3389,5900,8080 10.201.70.249

echo -e "\n4. OS detection..."
# OS fingerprinting
nmap -O 10.201.70.249

echo -e "\n5. Vulnerability scanning with nmap scripts..."
# Basic vulnerability scan
nmap --script vuln 10.201.70.249

echo "Reconnaissance complete!"
