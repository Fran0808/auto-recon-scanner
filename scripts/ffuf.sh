#!/bin/bash
TARGET=$1
OUTPUT_FILE="/scanner/results/ffuf.json"
WORDLIST="/usr/share/wordlists/dirb/common.txt"


ffuf -u "https://$TARGET/FUZZ" -w "$WORDLIST" -ac -s -o "$OUTPUT_FILE" -of json
