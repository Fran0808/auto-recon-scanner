#!/bin/bash

TARGET=$1

echo "Scanning $TARGET..."
nmap -sV $TARGET -oN results/nmap.txt

echo "Scan completed"