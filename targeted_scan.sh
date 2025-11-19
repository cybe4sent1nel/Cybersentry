#!/bin/bash
# More targeted port scanning
echo "Trying specific common ports..."
nmap -Pn -p 22,80,443,8080,3000,5000,8000,9000,10000 10.201.70.249

echo -e "\nTrying UDP scan..."
nmap -Pn -sU -p 53,161,123 10.201.70.249

echo -e "\nTrying with different timing..."
nmap -Pn -T2 -p 1-1000 10.201.70.249
