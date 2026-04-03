"""
Build PushBack as a standalone desktop app.
Creates a single executable that opens in the user's browser.
No install, no terminal, no Python required.

Usage:
    python build.py

Output:
    dist/PushBack (Linux)
    dist/PushBack.exe (Windows)
    dist/PushBack.app (Mac)
"""

import subprocess
import sys
import os

def main():
    # Install PyInstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--quiet"])

    print("Building PushBack desktop app...")
    print("This takes 1-2 minutes...\n")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "PushBack",
        "--add-data", "parser.py:.",
        "--add-data", "analyzer.py:.",
        "--hidden-import", "PyPDF2",
        "--hidden-import", "docx",
        "--hidden-import", "openpyxl",
        "--hidden-import", "pptx",
        "--hidden-import", "anthropic",
        "--noconsole" if sys.platform == "win32" else "--console",
        "app.py",
    ]

    subprocess.run(cmd)

    print("\n✓ Build complete!")
    print(f"  Executable: dist/PushBack{'exe' if sys.platform == 'win32' else ''}")
    print(f"  Share this single file — no install needed.")
    print(f"  User double-clicks → browser opens → drop files → get analysis.")


if __name__ == "__main__":
    main()
