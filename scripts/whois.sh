#!/bin/bash
# Whois lookup wrapper

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

# We let Python handle the filtering and file saving for Whois
whois "$TARGET"
