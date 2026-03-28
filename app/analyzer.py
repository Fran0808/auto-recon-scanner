import os
import json

def parse_nmap(filepath):
    open_ports = []
    
    if not os.path.exists(filepath):
        print(f"Warning: File not found -> {filepath}")
        return open_ports

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if "/tcp" in line and "open" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0]
                    service = parts[2]
                    open_ports.append({"port": port, "service": service})
                    
    return open_ports

def parse_whatweb(filepath):
    technologies = set()
    
    if not os.path.exists(filepath):
        print(f"Warning: File not found -> {filepath}")
        return list(technologies)

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(", ")
            for part in parts:
                technologies.add(part.strip())
                
    return sorted(list(technologies))

def parse_ffuf(filepath, target=""):
    directories = []
    
    if not os.path.exists(filepath):
        print(f"Warning: File not found -> {filepath}")
        return directories

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for res in data.get("results", []):
                directories.append({
                    "url": res.get("url"),
                    "status": str(res.get("status"))
                })
    except Exception as e:
        print(f"Warning: Failed to parse FFUF JSON -> {e}")
                    
    return directories

def parse_findomain(filepath):
    subdomains = []
    
    if not os.path.exists(filepath):
        print(f"Warning: File not found -> {filepath}")
        return subdomains

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                subdomains.append(line)
                
    return subdomains

def generate_report(results_dir, target=""):
    """
    Combines all parsers to build a master report dictionary.
    """
    nmap_file = os.path.join(results_dir, "nmap.txt")
    whatweb_file = os.path.join(results_dir, "whatweb.txt")
    ffuf_file = os.path.join(results_dir, "ffuf.json")
    findomain_file = os.path.join(results_dir, "findomain.txt")

    report = {
        "open_ports": parse_nmap(nmap_file),
        "web_technologies": parse_whatweb(whatweb_file),
        "directories": parse_ffuf(ffuf_file, target),
        "subdomains": parse_findomain(findomain_file)
    }
    return report

def save_report_json(report_data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)
    print(f"\n[+] Final OSINT Report saved to: {filepath}")

if __name__ == "__main__":
    nmap_file = os.path.join("results", "nmap.txt")
    whatweb_file = os.path.join("results", "whatweb.txt")
    ffuf_file = os.path.join("results", "ffuf.json")
    findomain_file = os.path.join("results", "findomain.txt")
    
    print("\n--- Testing Nmap Parser ---")
    ports = parse_nmap(nmap_file)
    for p in ports:
        print(f"Port: {p['port']} | Service: {p['service']}")
    print(f"Total open ports found: {len(ports)}")

    print("\n--- Testing WhatWeb Parser ---")
    techs = parse_whatweb(whatweb_file)
    for t in techs:
        print(f" detected: {t}")
    print(f"Total technologies found: {len(techs)}")

    print("\n--- Testing FFUF Parser ---")
    dirs = parse_ffuf(ffuf_file, target="testdomain.com")
    for d in dirs:
        print(f"Found URL: {d['url']} | Status: {d['status']}")
    print(f"Total REAL directories found: {len(dirs)}")

    print("\n--- Testing Findomain Parser ---")
    subs = parse_findomain(findomain_file)
    for s in subs:
        print(f"Subdomain: {s}")
    print(f"Total subdomains found: {len(subs)}")
