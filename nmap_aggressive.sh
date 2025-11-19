#!/bin/bash
# Try nmap with -Pn flag to bypass ping blocking
echo "Attempting nmap scan with -Pn flag (no ping)..."
nmap -Pn -T4 -F 10.201.70.249

echo -e "\nTrying more aggressive scan with service detection..."
nmap -Pn -sV -sC -A 10.201.70.249
