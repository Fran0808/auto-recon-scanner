#!/bin/bash
# WhatWeb fingerprinting script

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target>"
    exit 1
fi

whatweb -a 3 "$TARGET"

if [ $? -eq 0 ]; then
    exit 0
else
    echo "Error: WhatWeb scan failed."
    exit 1
fi
