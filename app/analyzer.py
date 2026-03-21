import os

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

def parse_gobuster(filepath):
    directories = []
    
    if not os.path.exists(filepath):
        print(f"Warning: File not found -> {filepath}")
        return directories

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
           
            if "(Status:" in line and "429" not in line:
                parts = line.split()
                if len(parts) >= 3:
                    path = parts[0]
                    status = parts[2].replace(")", "")
                    directories.append({"path": path, "status": status})
                    
    return directories

if __name__ == "__main__":
    nmap_file = os.path.join("results", "nmap.txt")
    whatweb_file = os.path.join("results", "whatweb.txt")
    gobuster_file = os.path.join("results", "gobuster.txt")
    
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

    print("\n--- Testing Gobuster Parser ---")
    dirs = parse_gobuster(gobuster_file)
    for d in dirs:
        print(f"Found path: /{d['path']} | Status: {d['status']}")
    print(f"Total REAL directories found: {len(dirs)}")
