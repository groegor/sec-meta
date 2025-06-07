import subprocess
import sys

def build_package():
    """Build the package"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "build", "twine"])
    subprocess.check_call([sys.executable, "-m", "build"])
    
if __name__ == "__main__":
    build_package()