import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"Target: {target}")

    result = subprocess.run(
        ["nmap", "--version"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("nmap is available:")
        print(result.stdout)
    else:
        print("nmap not found or failed:")
        print(result.stderr)

if __name__ == "__main__":
    main()
