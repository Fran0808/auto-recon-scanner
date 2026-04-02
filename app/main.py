import sys
import subprocess
import os
import time
import concurrent.futures
import analyzer # type: ignore
import html_generator

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

def run_nmap(target: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, "nmap.sh")
    
    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output_file = os.path.join(RESULTS_DIR, "nmap.txt")
    else:
        print(f"{RED}[-] nmap failed:{RESET}")
        print(result.stderr)

def run_whois(target: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, "whois.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        clean_output = filter_whois(result.stdout)

        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "whois.txt")

        with open(output_file, "w") as f:
            f.write(clean_output)
    else:
        print(f"{RED}[-] whois failed:{RESET}")
        print(result.stderr)

def run_whatweb(target: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, "whatweb.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "whatweb.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)
    else:
        print(f"{RED}[-] whatweb failed:{RESET}")
        print(result.stderr)

def run_findomain(target: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, "findomain.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "findomain.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)
    else:
        print(f"{RED}[-] findomain failed:{RESET}")
        print(result.stderr)

def run_ffuf(target: str) -> None:
    script_path = os.path.join(SCRIPTS_DIR, "ffuf.sh")

    result = subprocess.run(
        ["bash", script_path, target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        output_file = os.path.join(RESULTS_DIR, "ffuf.json")
    else:
        print(f"{RED}[-] ffuf failed:{RESET}")
        print(result.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target>")
        sys.exit(1)

    raw_target = sys.argv[1]
    target = raw_target.replace("https://", "").replace("http://", "").strip("/")
    
    print(f"{CYAN}Target: {target}{RESET}")

    try:
        print(f"\n{CYAN}[*] Starting scanner...{RESET}")
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            tasks = [
                executor.submit(run_whois, target), # type: ignore
                executor.submit(run_whatweb, target), # type: ignore
                executor.submit(run_findomain, target), # type: ignore
                executor.submit(run_ffuf, target), # type: ignore
                executor.submit(run_nmap, target)
            ]
            
            completed = 0
            total = len(tasks)
            print(f"{GREEN}[*] Progress: [{completed}/{total}] tools finished...{RESET}", end='\r')
            
            for future in concurrent.futures.as_completed(tasks):
                completed += 1
                print(f"{GREEN}[*] Progress: [{completed}/{total}] tools finished...{RESET}", end='\r')
                
            print()

        print(f"\n{CYAN}[*] Starting Data Analysis and Compiling Report...{RESET}")
        report_data = analyzer.generate_report(RESULTS_DIR, target)
        
        report_path = os.path.join(RESULTS_DIR, "final_report.json")
        analyzer.save_report_json(report_data, report_path)
        
        html_path = os.path.join(RESULTS_DIR, "final_report.html")
        html_generator.generate_html_report(report_data, html_path, target)
        
        end_time = time.time()
        elapsed = (end_time - start_time)/60

        print(f"\n{GREEN}=========================================={RESET}")
        print(f"{GREEN}    SCAN COMPLETE FOR: {target}           {RESET}")
        print(f"{GREEN}    TIME ELAPSED: {elapsed:.2f} minutes    {RESET}")
        print(f"{GREEN}=========================================={RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{RED}Scan has been cancelled by user{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
