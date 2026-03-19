import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"Target: {target}")
    print("Running nmap scan...")

    result = subprocess.run(
        ["nmap", "-sV", target],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("nmap failed:")
        print(result.stderr)

if __name__ == "__main__":
    main()
