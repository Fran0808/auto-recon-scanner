import sys
import subprocess
import os
import analyzer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

WHOIS_FIELDS = [
    "Domain Name",
    "Creation Date",
    "Registry Expiry Date",
    "Registrar Registration Expiration Date",
    "Updated Date",
    "Registrar:",
    "Domain Status",
    "Name Server",
    "DNSSEC",
    "Registrant Country",
    "Registrant State/Province",
]

def filter_whois(raw_output):
    seen = set()
    filtered = []

    for line in raw_output.splitlines():
        stripped = line.strip()

        if "REDACTED" in stripped:
            continue

        for field in WHOIS_FIELDS:
            if stripped.lower().startswith(field.lower()):
                if field not in seen:
                    seen.add(field)
                    filtered.append(stripped)
                break

    return "\n".join(filtered)

def run_nmap(target):
    print(f"\n{CYAN}[*] Running nmap scan...{RESET}")
    script_path = os.path.join(SCRIPTS_DIR, "nmap.sh")
    
    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
        output_file = os.path.join(RESULTS_DIR, "nmap.txt")
        print(f"{GREEN}[+] Results saved to {output_file}{RESET}")
    else:
        print(f"{RED}[-] nmap failed:{RESET}")
        print(result.stderr)

def run_whois(target):
    print(f"\n{CYAN}[*] Running whois lookup...{RESET}")
    script_path = os.path.join(SCRIPTS_DIR, "whois.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        clean_output = filter_whois(result.stdout)
        print(clean_output)

        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "whois.txt")

        with open(output_file, "w") as f:
            f.write(clean_output)

        print(f"{GREEN}[+] Results saved to {output_file}{RESET}")
    else:
        print(f"{RED}[-] whois failed:{RESET}")
        print(result.stderr)

def run_whatweb(target):
    print(f"\n{CYAN}[*] Running whatweb fingerprinting...{RESET}")
    script_path = os.path.join(SCRIPTS_DIR, "whatweb.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout.strip())
        
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "whatweb.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"{GREEN}[+] Results saved to {output_file}{RESET}")
    else:
        print(f"{RED}[-] whatweb failed:{RESET}")
        print(result.stderr)

def run_findomain(target):
    print(f"\n{CYAN}[*] Running findomain...{RESET}")
    script_path = os.path.join(SCRIPTS_DIR, "findomain.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout.strip())
        
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "findomain.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"{GREEN}[+] Results saved to {output_file}{RESET}")
    else:
        print(f"{RED}[-] findomain failed:{RESET}")
        print(result.stderr)

def run_gobuster(target):
    print(f"\n{CYAN}[*] Running gobuster directory scan...{RESET}")
    script_path = os.path.join(SCRIPTS_DIR, "gobuster.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout.strip())
        output_file = os.path.join(RESULTS_DIR, "gobuster.txt")
        print(f"{GREEN}[+] Results saved to {output_file}{RESET}")
    else:
        print(f"{RED}[-] gobuster failed:{RESET}")
        print(result.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"{CYAN}Target: {target}{RESET}")

    try:
        run_whois(target)
        run_whatweb(target)
        run_findomain(target)
        run_gobuster(target)
        run_nmap(target)

        # Compilation
        print(f"\n{CYAN}[*] Starting Data Analysis and Compiling Report...{RESET}")
        report_data = analyzer.generate_report(RESULTS_DIR)
        
        report_path = os.path.join(RESULTS_DIR, "final_report.json")
        analyzer.save_report_json(report_data, report_path)

        print(f"\n{GREEN}=========================================={RESET}")
        print(f"{GREEN}    SCAN COMPLETE FOR: {target}           {RESET}")
        print(f"{GREEN}=========================================={RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{RED}Scan has been cancelled by user{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
