#!/bin/bash
# Gobuster directory brute-forcing script

TARGET=$1
WORDLIST="/usr/share/wordlists/dirb/common.txt"
OUTPUT_FILE="results/gobuster.txt"

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

mkdir -p results

if [[ ! "$TARGET" =~ ^http ]]; then
    TARGET="https://$TARGET"
fi

# Run gobuster in dir mode
gobuster dir -u "$TARGET" -w "$WORDLIST" -t 50 -q -o "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    exit 0
else
    echo "Error: Gobuster scan failed. Make sure the target is reachable and the wordlist exists."
    exit 1
fi
