import subprocess

def self_update():
    print("updating ziion-cli...")
    print("\nCurrent version:")
    subprocess.run(["ziion", "--version"],
            stderr=subprocess.STDOUT)
    print("\n")
    subprocess.run(["sudo", "pip3.10", "install", "ziion", "-U"],
            stderr=subprocess.STDOUT)
    print("\nNew version:")
    subprocess.run(["ziion", "--version"],
            stderr=subprocess.STDOUT)