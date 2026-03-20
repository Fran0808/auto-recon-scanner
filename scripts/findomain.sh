#!/bin/bash
# Findomain subdomain enumeration script

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

findomain -t "$TARGET" -q

if [ $? -eq 0 ]; then
    exit 0
else
    echo "Error: Findomain enumeration failed."
    exit 1
fi
