# Auto Recon Scanner

## Description
Auto Recon Scanner is an automated OSINT and reconnaissance orchestration tool. It chains together several industry-standard pentesting utilities (Nmap, WhatWeb, Gobuster, Findomain) to perform comprehensive attack surface mapping, subsequently aggregating and cleaning the raw outputs into a single, structured JSON report.

## Features
- Port and Service Enumeration (Nmap)
- Hidden Directory Discovery (Gobuster)
- Subdomain Enumeration (Findomain)
- Web Technology Fingerprinting (WhatWeb)
- Automated JSON Report Generation for easy integration with other tools

## Installation and Usage

There are two main ways to run Auto Recon Scanner: using Docker (Recommended) or natively on your operating system (Best suited for Kali Linux).

### Method 1: Docker Compose (Recommended)
This method is cross-platform and ensures all dependencies (such as Wordlists and specific versions of tools) are met without altering your host system.

1. Build the Docker image:
```bash
docker-compose build
```

2. Run the scanner against your target:
```bash
docker-compose run --rm scanner <target-domain>
```

### Method 2: Native Execution
If you prefer to run the scripts directly on your host machine, you must ensure all dependencies are installed and available in your system's PATH.

1. Install system requirements (Debian/Kali based):
```bash
sudo apt-get update
sudo apt-get install python3 nmap whatweb gobuster dirb wget unzip
```

2. Install Findomain manually and place it in your PATH:
```bash
wget https://github.com/Findomain/Findomain/releases/download/10.0.1/findomain-linux.zip
unzip findomain-linux.zip
sudo mv findomain /usr/local/bin/findomain
sudo chmod +x /usr/local/bin/findomain
```

3. Run the Python orchestrator:
```bash
python3 app/main.py <target-domain>
```

## Output Structure
Upon completion of the scan, the tool will populate the `results/` directory with the raw text outputs of each individual tool.

Additionally, the Python analyzer will compile the most critical findings into a structured file located at:
`results/final_report.json`

This JSON file contains arrays mapping open ports, subdomains, full URLs to hidden directories, and detected server technologies.
