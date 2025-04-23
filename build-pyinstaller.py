"""
make executable
"""
import subprocess
import platform
import sys
import os

def Make_exe():
    result = ""
    
    # resources folder path
    resources_dir = os.path.join(os.getcwd(), "icons")

    # Windows
    if platform.system() == "Windows":
        ico_path = os.path.join(resources_dir, "cpg.ico")
        if not os.path.exists(ico_path):
            print(f"Error: {ico_path} not found.")
            sys.exit(1)
        result = subprocess.run(f"pyinstaller main.py --name cpg-win.exe --onefile --noconsole --noconfirm --icon={ico_path}", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        sys.exit(0)
    
    # macOS
    elif platform.system() == "Darwin":
        icns_path = os.path.join(resources_dir, "cpg.icns")
        if not os.path.exists(icns_path):
            print(f"Error: {icns_path} not found.")
            sys.exit(1)
        result = subprocess.run(f"pyinstaller main.py --name cpg-mac --onefile --noconsole --noconfirm --icon={icns_path}", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        sys.exit(0)

if __name__=="__main__":
    Make_exe()