#!/bin/bash
# Advanced enumeration techniques for firewalled targets
echo "=== ADVANCED ENUMERATION TECHNIQUES ==="

# 1. Try different scan types
echo "1. Trying SYN scan (stealth)..."
nmap -sS -Pn -p 80,443,22,21 10.201.70.249

# 2. Try ACK scan to detect firewall rules
echo -e "\n2. ACK scan to analyze firewall behavior..."
nmap -sA -Pn -p 80,443,22 10.201.70.249

# 3. Try NULL scan
echo -e "\n3. NULL scan for firewall analysis..."
nmap -sN -Pn -p 80,443,22 10.201.70.249

# 4. Try XMAS scan
echo -e "\n4. XMAS scan for firewall analysis..."
nmap -sX -Pn -p 80,443,22 10.201.70.249

# 5. Try slow timing to avoid detection
echo -e "\n5. Slow timing scan (T1)..."
nmap -T1 -Pn -p 80,443,22 10.201.70.249

echo -e "\n=== ADVANCED ENUMERATION COMPLETE ==="
