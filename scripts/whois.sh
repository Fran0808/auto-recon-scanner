#!/bin/bash
# Whois lookup wrapper

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

whois "$TARGET"

if [ $? -eq 0 ]; then
    exit 0
else
    echo "Error: Whois lookup failed."
    exit 1
fi
