import os
import getpass
import datetime
import sys
import plistlib
import tkinter as tk
from tkinter import filedialog, messagebox
from socket import gethostname
from pathlib import Path

# --debug フラグが指定されているか確認
debug_mode = '--debug' in sys.argv

# Get computername
hostname = gethostname()

# Get login account
username = getpass.getuser()


def get_app_dir():
    """
    アプリケーションの実行可能ファイルが存在するディレクトリ、
    またはスクリプトが配置されているディレクトリを取得します。

    - Nuitka onefile モードでは sys.argv[0] が .exe のパスを指す
    - __compiled__.containing_dir は Nuitka standalone モードで推奨される
    - PyInstaller は _MEIPASS を使用する
    """
    app_dir = ""
    if sys.platform == "win32":
        # Nuitka onefile モード
        if "__compiled__" in globals():
            app_dir = __compiled__.containing_dir

    elif sys.platform == "darwin":
        if "__compiled__" in globals() or hasattr(sys, '_MEIPASS'):
            # Path tweak for macOS (.app) : binary is under <Name>.app/Contents/MacOS/
            # nuitka > "__compiled__" in globals()
            # pyinstaller > hasattr(sys, '_MEIPASS')
            base_dir = os.path.dirname(sys.executable)
            app_dir = os.path.abspath(os.path.join(base_dir, "../../../"))

    else:
        # 対話モード, Win/pyinstaller, Linux, etc.
        app_dir = os.path.dirname(sys.executable)

    return app_dir

# Load all .mobileconfig files in the 'mobileconfig' folder and from user selection
class MobileconfigManager:
    def __init__(self, root):
        self.mobileconfig_files = []
        self.file_vars = []
        self.checkbox_frames = []
        self.root = root  # Store reference to root window

    def check_mobileconfig_folder(self):
        """Check for mobileconfig folder existence at startup"""

        # ここで一貫してアプリのルートディレクトリを取得
        current_dir = get_app_dir()
        mobileconfig_dir = os.path.join(current_dir, "mobileconfig")

        # デバッグログの出力（debug_mode のときだけ）
        if debug_mode:
            with open("debug.log", "a", encoding="utf-8") as log:
                print(f"[DEBUG] check_mobileconfig_folder", file=log)
                print(f"[DEBUG] current_dir: {current_dir}", file=log)
                print(f"[DEBUG] mobileconfig_dir: {mobileconfig_dir}", file=log)

        # フォルダ存在チェック
        if not os.path.exists(mobileconfig_dir):
            self.root.lift()
            self.root.focus_force()
            messagebox.showwarning(
                "Warning",
                "The 'mobileconfig' folder was not found.\n"
                "Please use the 'Add Files' button to manually select files.",
                parent=self.root
            )
            return False
        return True

    def get_mobileconfig_files(self):
        """mobileconfig フォルダから設定ファイルを読み込む"""
        current_dir = get_app_dir()  # ← これに統一！
        mobileconfig_dir = os.path.join(current_dir, "mobileconfig")

        if os.path.exists(mobileconfig_dir):
            folder_files = [
                os.path.join(mobileconfig_dir, f)
                for f in os.listdir(mobileconfig_dir)
                if f.endswith(".mobileconfig")
            ]

            for file in folder_files:
                if file not in self.mobileconfig_files:
                    self.mobileconfig_files.append(file)

        return self.mobileconfig_files

    def browse_mobileconfig(self):
        # Open file dialog to select .mobileconfig files
        filepaths = filedialog.askopenfilenames(
            title="Select .mobileconfig files",
            filetypes=[("mobileconfig files", "*.mobileconfig"), ("All files", "*.*")],
            parent=self.root  # Set parent window for dialog
        )

        # Add selected files to the list if they're not already there
        for filepath in filepaths:
            if filepath not in self.mobileconfig_files:
                self.mobileconfig_files.append(filepath)

        # Update the UI to show the new files
        self.update_file_list()

    def update_file_list(self):
        # Clear existing checkboxes
        for frame in self.checkbox_frames:
            frame.destroy()

        self.checkbox_frames = []
        self.file_vars = []

        # Create new checkboxes
        for i, path in enumerate(self.mobileconfig_files):
            frame = tk.Frame(file_list_frame)
            frame.pack(fill=tk.X, padx=5, anchor="w")
            self.checkbox_frames.append(frame)

            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame, text=os.path.basename(path), variable=var, anchor="w")
            chk.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.file_vars.append(var)

            # Add remove button
            remove_btn = tk.Button(frame, text="×", font=("Arial", 10), width=2,
                                    command=lambda idx=i: self.remove_file(idx))
            remove_btn.pack(side=tk.RIGHT)

        # Update scroll region
        file_list_canvas.configure(scrollregion=file_list_canvas.bbox("all"))

    def remove_file(self, index):
        if 0 <= index < len(self.mobileconfig_files):
            del self.mobileconfig_files[index]
            self.update_file_list()

def save_exit():
    new_value1 = entry_field1.get().strip()

    if not new_value1:
        messagebox.showwarning("Alert", "Please enter your account", parent=root)
        return

    new_value1 = new_value1.split('@')[0]

    try:
        current_dir = get_app_dir()  # ← ここを統一！

        saved_count = 0
        for var, file in zip(manager.file_vars, manager.mobileconfig_files):
            if var.get():
                with open(file, "rb") as f:
                    data = plistlib.load(f)

                data["PayloadContent"][0]["EAPClientConfiguration"]["UserName"] = new_value1
                dt_now = datetime.datetime.now()
                data["PayloadIdentifier"] = hostname + "_" + dt_now.strftime('%Y%m%d-%H%M%S.%f')

                newname = Path(file).stem + "-" + new_value1 + ".mobileconfig"
                save_path = os.path.join(current_dir, newname)

                with open(save_path, "wb") as f:
                    plistlib.dump(data, f)

                saved_count += 1

        if saved_count > 0:
            messagebox.showinfo("Success", f"Saved {saved_count} file(s)", parent=root)
            root.destroy()
        else:
            messagebox.showwarning("Warning", "No files selected", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred while saving: {e}", parent=root)


# Set up UI
root = tk.Tk()
root.title("Custom Profile Generator")
root.geometry("500x400")

# Common font setting
def configure_root(root):
    default_font = ("Arial", 12)
    root.option_add("*Font", default_font)
    root.option_add("*Button.Font", default_font)
    root.option_add("*Entry.Font", default_font)
    scaling_factor = root.tk.call('tk', 'scaling')
    if scaling_factor != 1.0:
        root.tk.call('tk', 'scaling', 1.0)

configure_root(root)

# Center the window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

# Create a manager for mobileconfig files and pass root window reference
manager = MobileconfigManager(root)

# Check if mobileconfig folder exists at startup
# Wait for window to be visible before showing dialog
root.update()
manager.check_mobileconfig_folder()

# Header frame
header_frame = tk.Frame(root)
header_frame.pack(fill=tk.X, padx=10, pady=10)

label0 = tk.Label(header_frame, text="Mobileconfig File List\n(Select files to modify)", wraplength=400, justify="left")
label0.pack(side=tk.LEFT)

# Add browse button
browse_button = tk.Button(header_frame, text="Add Files", command=manager.browse_mobileconfig)
browse_button.pack(side=tk.RIGHT, padx=10)

# Create a frame with scrollbar for file list
file_list_outer_frame = tk.Frame(root, borderwidth=1, relief="sunken", height=200)
file_list_outer_frame.pack(fill=tk.X, padx=10, pady=10)
file_list_outer_frame.pack_propagate(False)

# Add scrollbar
file_list_scrollbar = tk.Scrollbar(file_list_outer_frame)
file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add canvas for scrolling
file_list_canvas = tk.Canvas(file_list_outer_frame, yscrollcommand=file_list_scrollbar.set)
file_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
file_list_scrollbar.config(command=file_list_canvas.yview)

# Frame inside canvas for checkboxes
file_list_frame = tk.Frame(file_list_canvas)
file_list_canvas.create_window((0, 0), window=file_list_frame, anchor="nw")

def on_frame_configure(event):
    file_list_canvas.configure(scrollregion=file_list_canvas.bbox("all"))

file_list_frame.bind("<Configure>", on_frame_configure)

# Load initial files and populate list
manager.get_mobileconfig_files()
manager.update_file_list()

# Input fields frame
input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Account input field
entry_label1 = tk.Label(input_frame, text="Your account")
entry_label1.grid(row=0, column=0, padx=40, pady=5, sticky="w")

entry_field1 = tk.Entry(input_frame, width=35)
entry_field1.grid(row=0, column=1, padx=0, pady=5)

## Password input field
#entry_label2 = tk.Label(input_frame, text="Your password")
#entry_label2.grid(row=1, column=0, padx=40, pady=5, sticky="w")
#
#entry_field2 = tk.Entry(input_frame, width=35, show="*")
#entry_field2.grid(row=1, column=1, padx=0, pady=5)

# Save button
save_exit_button = tk.Button(root, text="Save & Exit", command=save_exit, padx=15, pady=5)
save_exit_button.pack(pady=10)
save_exit_button.bind("<Return>", lambda event: save_exit())

root.mainloop()
