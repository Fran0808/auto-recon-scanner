#!/bin/bash
# Nmap scan script

TARGET=$1
OUTPUT_FILE="results/nmap.txt"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

mkdir -p results

echo "Starting Nmap scan on $TARGET..."
# -sV: Probe open ports to determine service/version info
# -sC: default scripts (safe vulnerabilities)
# -Pn: Treat all hosts as online -- skip host discovery
nmap -sV -sC -Pn "$TARGET" -oN "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "Nmap scan completed successfully."
else
    echo "Error: Nmap scan failed."
    exit 1
fi