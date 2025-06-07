import subprocess
import sys
import os

def build_package():
    """Build the package"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "build", "twine"])
    
    # Change to the directory containing pyproject.toml
    os.chdir("secmeta_pkg")
    subprocess.check_call([sys.executable, "-m", "build"])
    
if __name__ == "__main__":
    build_package()