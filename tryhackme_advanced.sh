#!/bin/bash
# Try different approaches for the TryHackMe machine
echo "=== TRYHACKME MACHINE ANALYSIS ==="
echo "Target: 10.201.70.249"
echo ""

# 1. Try a very slow scan to avoid detection
echo "1. Trying very slow scan (T0 timing)..."
nmap -T0 -Pn -p 80,443,22,21,23,25,53,110,143,993,995,3306,3389,5900,8080 10.201.70.249

# 2. Try fragmented packets
echo -e "\n2. Trying fragmented packet scan..."
nmap -f -Pn -p 80,443 10.201.70.249

# 3. Try decoy scan
echo -e "\n3. Trying decoy scan..."
nmap -D RND:5 -Pn -p 80,443 10.201.70.249

# 4. Try with different source ports
echo -e "\n4. Trying different source ports..."
nmap -g 53 -Pn -p 80,443 10.201.70.249

echo -e "\n=== ADVANCED SCANS COMPLETE ==="
