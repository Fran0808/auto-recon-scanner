import sys
import subprocess
import os

RESULTS_DIR = "results"

def run_nmap(target):
    print("Running nmap scan...")

    result = subprocess.run(
        ["nmap", "-sV", target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)

        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "nmap.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"Results saved to {output_file}")
    else:
        print("nmap failed:")
        print(result.stderr)

def run_whois(target):
    print("Running whois lookup...")

    result = subprocess.run(
        ["whois", target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)

        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_file = os.path.join(RESULTS_DIR, "whois.txt")

        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"Results saved to {output_file}")
    else:
        print("whois failed:")
        print(result.stderr)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"Target: {target}")

    try:
        run_whois(target)
        run_nmap(target)
    except KeyboardInterrupt:
        print("\nScan has been cancelled by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
