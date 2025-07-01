import os
import subprocess
import sys

def install_deps():
    # Create target directory
    os.makedirs("./python", exist_ok=True)
    
    # Install with --no-deps and --platform to ensure compatibility
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--target", "./python",
        "--platform", "manylinux2014_x86_64",  # Ensures Vercel compatibility
        "--only-binary=:all:",
        "--no-deps",
        "-r", "requirements.txt"
    ], check=True)
    
    # Clean up
    for root, dirs, _ in os.walk("./python"):
        if "tests" in dirs:
            test_dir = os.path.join(root, "tests")
            print(f"Removing {test_dir}")
            subprocess.run(["rm", "-rf", test_dir])
        if "__pycache__" in dirs:
            cache_dir = os.path.join(root, "__pycache__")
            print(f"Removing {cache_dir}")
            subprocess.run(["rm", "-rf", cache_dir])

if __name__ == "__main__":
    install_deps()
    print("Installation completed successfully!")