#!/usr/bin/env python3
"""
Claude App Launcher - Professional GUI tool for running Claude-generated Python applications
Modern card-based interface with professional UX design
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import sys
from pathlib import Path
import re
import threading
import json


class AppCard(ttk.Frame):
    """A beautiful card widget for displaying an app"""
    
    def __init__(self, parent, app_name, app_info, launcher):
        super().__init__(parent, style='Card.TFrame')
        self.app_name = app_name
        self.app_info = app_info
        self.launcher = launcher
        
        # Card padding
        self.configure(padding=20)
        
        # App title
        title_label = ttk.Label(
            self, 
            text=app_name,
            font=("Segoe UI", 14, "bold"),
            foreground="#2c3e50"
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # App details
        details = []
        details.append(f"Entry: {app_info['entry_point']}")
        
        if app_info['has_requirements']:
            details.append("Dependencies: requirements.txt")
        elif app_info['dependencies']:
            details.append(f"Dependencies: {', '.join(app_info['dependencies'][:3])}")
            if len(app_info['dependencies']) > 3:
                details.append(f"  (+{len(app_info['dependencies']) - 3} more)")
        else:
            details.append("Dependencies: None")
        
        details_text = "\n".join(details)
        details_label = ttk.Label(
            self,
            text=details_text,
            font=("Segoe UI", 9),
            foreground="#7f8c8d",
            justify=tk.LEFT
        )
        details_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Button frame
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        # Run button
        run_btn = ttk.Button(
            btn_frame,
            text="Run Now",
            command=self.run_app,
            style='Accent.TButton'
        )
        run_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create launcher button
        launcher_btn = ttk.Button(
            btn_frame,
            text="Create Script",
            command=self.create_launcher
        )
        launcher_btn.pack(side=tk.LEFT)
    
    def run_app(self):
        """Run this app"""
        self.launcher.run_app(self.app_name, self.app_info)
    
    def create_launcher(self):
        """Create launcher script for this app"""
        self.launcher.create_launcher(self.app_name, self.app_info)


class ModernLauncher:
    """Modern, professional Claude App Launcher"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Claude® App Launcher \t\t\t\t\t\t\t\t © Mark Eckdahl 2025")
        self.root.geometry("1000x700")
        
        # Setup paths
        self.base_path = Path(__file__).parent
        self.config_file = self.base_path / ".launcher_config.json"
        
        # Load saved projects path or use default
        self.projects_path = self.load_projects_path()
        self.projects_path.mkdir(exist_ok=True)
        
        self.apps = {}
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.setup_ui()
        
        # Load apps
        self.scan_projects()
    
    def setup_styles(self):
        """Setup modern color scheme and styles"""
        style = ttk.Style()
        
        # Colors
        self.colors = {
            'primary': '#3498db',      # Blue
            'success': '#2ecc71',      # Green
            'warning': '#f39c12',      # Orange
            'danger': '#e74c3c',       # Red
            'dark': '#2c3e50',         # Dark blue-gray
            'light': '#ecf0f1',        # Light gray
            'white': '#ffffff',
            'text': '#2c3e50',
            'text_light': '#7f8c8d'
        }
        
        # Card style
        style.configure('Card.TFrame', 
                       background='#ffffff',
                       relief='raised',
                       borderwidth=1)
        
        # Accent button
        style.configure('Accent.TButton',
                       font=('Segoe UI', 10, 'bold'))
        
        # Header style
        style.configure('Header.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['dark'])
        
        # Subheader style
        style.configure('Subheader.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.colors['text_light'])
    
    def setup_ui(self):
        """Create the modern UI"""
        # Main container with background color
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, padx=30, pady=(30, 10))
        
        # Title and subtitle
        title_label = ttk.Label(
            header_frame,
            text="Claude® App Launcher",
            style='Header.TLabel'
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Manage and run your Python applications with ease",
            style='Subheader.TLabel'
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Toolbar
        toolbar_frame = ttk.Frame(main_container)
        toolbar_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        
        # Refresh button
        refresh_btn = ttk.Button(
            toolbar_frame,
            text="Refresh Apps",
            command=self.scan_projects,
            style='Accent.TButton'
        )
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Open folder button
        folder_btn = ttk.Button(
            toolbar_frame,
            text="Open Projects Folder",
            command=self.open_projects_folder
        )
        folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Change folder button
        change_folder_btn = ttk.Button(
            toolbar_frame,
            text="Change Projects Folder",
            command=self.change_projects_folder
        )
        change_folder_btn.pack(side=tk.LEFT)
        
        # App count label
        self.app_count_label = ttk.Label(
            toolbar_frame,
            text="",
            font=("Segoe UI", 10),
            foreground=self.colors['text_light']
        )
        self.app_count_label.pack(side=tk.RIGHT)
        
        # Scrollable canvas for app cards
        canvas_frame = ttk.Frame(main_container)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Canvas and scrollbar
        self.canvas = tk.Canvas(
            canvas_frame,
            bg='#f5f7fa',
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            foreground=self.colors['text_light'],
            padding=(30, 10)
        )
        status_label.pack(anchor="w")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def scan_projects(self):
        """Scan for Python apps and display them"""
        self.apps = {}
        
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.projects_path.exists():
            self.show_empty_state("Projects folder not found")
            return
        
        # Find all subdirectories
        for folder in sorted(self.projects_path.iterdir()):
            if folder.is_dir() and not folder.name.startswith('.'):
                app_info = self.analyze_app(folder)
                if app_info:
                    self.apps[folder.name] = app_info
        
        if not self.apps:
            self.show_empty_state("No apps found in projects folder")
            return
        
        # Create cards for each app
        row = 0
        col = 0
        max_cols = 2
        
        for app_name, app_info in self.apps.items():
            card = AppCard(self.scrollable_frame, app_name, app_info, self)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(max_cols):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Update app count
        count = len(self.apps)
        self.app_count_label.config(
            text=f"{count} app{'s' if count != 1 else ''} found"
        )
        self.status_var.set("Ready")
    
    def show_empty_state(self, message):
        """Show empty state message"""
        empty_frame = ttk.Frame(self.scrollable_frame)
        empty_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        empty_label = ttk.Label(
            empty_frame,
            text=message,
            font=("Segoe UI", 12),
            foreground=self.colors['text_light']
        )
        empty_label.pack()
        
        help_text = ttk.Label(
            empty_frame,
            text="\nAdd Python apps to the 'projects' folder\nEach app should be in its own subfolder",
            font=("Segoe UI", 10),
            foreground=self.colors['text_light'],
            justify=tk.CENTER
        )
        help_text.pack(pady=10)
        
        self.app_count_label.config(text="0 apps found")
    
    def analyze_app(self, folder):
        """Analyze a folder to determine if it's a valid Python app"""
        python_files = list(folder.glob("*.py"))
        
        if not python_files:
            return None
        
        # Try to find main entry point
        entry_point = None
        for name in ["main.py", "app.py", "run.py", "__main__.py"]:
            if (folder / name).exists():
                entry_point = name
                break
        
        if not entry_point:
            entry_point = python_files[0].name
        
        # Detect imports/dependencies
        imports = set()
        entry_file = folder / entry_point
        
        try:
            content = entry_file.read_text(encoding='utf-8')
            import_pattern = r'^(?:from|import)\s+([a-zA-Z0-9_]+)'
            for match in re.finditer(import_pattern, content, re.MULTILINE):
                module = match.group(1)
                if module not in ['os', 'sys', 'json', 're', 'pathlib', 'subprocess', 
                                 'datetime', 'time', 'math', 'random', 'collections',
                                 'itertools', 'functools', 'typing', 'tkinter']:
                    imports.add(module)
        except Exception:
            pass
        
        return {
            'folder': folder,
            'entry_point': entry_point,
            'python_files': [f.name for f in python_files],
            'dependencies': sorted(imports),
            'has_requirements': (folder / "requirements.txt").exists()
        }
    
    def run_app(self, app_name, app_info):
        """Run an app"""
        app_folder = app_info['folder']
        entry_point = app_info['entry_point']
        
        self.status_var.set(f"Running {app_name}...")
        
        def run_thread():
            try:
                # Check if UV is available
                uv_check = subprocess.run(
                    ["uv", "--version"],
                    capture_output=True,
                    text=True
                )
                
                if uv_check.returncode != 0:
                    self.root.after(0, lambda: messagebox.showerror(
                        "UV Not Found",
                        "UV is not installed. Install it with:\n\npip install uv"
                    ))
                    return
                
                # Setup UV environment if needed
                venv_path = app_folder / ".venv"
                
                if not venv_path.exists():
                    self.root.after(0, lambda: self.status_var.set("Creating environment..."))
                    subprocess.run(
                        ["uv", "venv"],
                        cwd=app_folder,
                        check=True,
                        capture_output=True
                    )
                
                # Install dependencies if requirements.txt exists
                if app_info['has_requirements']:
                    self.root.after(0, lambda: self.status_var.set("Installing dependencies..."))
                    subprocess.run(
                        ["uv", "pip", "install", "-r", "requirements.txt"],
                        cwd=app_folder,
                        check=True,
                        capture_output=True
                    )
                elif app_info['dependencies']:
                    self.root.after(0, lambda: self.status_var.set("Installing dependencies..."))
                    subprocess.run(
                        ["uv", "pip", "install"] + list(app_info['dependencies']),
                        cwd=app_folder,
                        check=True,
                        capture_output=True
                    )
                
                # Run the app
                self.root.after(0, lambda: self.status_var.set(f"Executing {entry_point}..."))
                
                if sys.platform == 'win32':
                    python_exe = venv_path / "Scripts" / "python.exe"
                else:
                    python_exe = venv_path / "bin" / "python"
                
                result = subprocess.run(
                    [str(python_exe), entry_point],
                    cwd=app_folder,
                    capture_output=True,
                    text=True
                )
                
                # Show output
                output = f"=== Output ===\n{result.stdout}\n"
                if result.stderr:
                    output += f"\n=== Errors ===\n{result.stderr}"
                
                self.root.after(0, lambda: self.show_output(app_name, output, result.returncode))
                
            except subprocess.CalledProcessError as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Execution Error",
                    f"Failed to run app:\n{str(e)}"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Unexpected error:\n{str(e)}"
                ))
            finally:
                self.root.after(0, lambda: self.status_var.set("Ready"))
        
        thread = threading.Thread(target=run_thread, daemon=True)
        thread.start()
    
    def show_output(self, app_name, output, return_code):
        """Display app output in a modern dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Output - {app_name}")
        dialog.geometry("800x600")
        
        # Header
        header_frame = ttk.Frame(dialog)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        status_text = "Completed Successfully" if return_code == 0 else f"Exited with code {return_code}"
        status_color = self.colors['success'] if return_code == 0 else self.colors['danger']
        
        status_label = ttk.Label(
            header_frame,
            text=status_text,
            font=("Segoe UI", 12, "bold"),
            foreground=status_color
        )
        status_label.pack()
        
        # Output text
        text_widget = scrolledtext.ScrolledText(
            dialog,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg='#f8f9fa',
            fg=self.colors['dark']
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        text_widget.insert(1.0, output)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = ttk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            style='Accent.TButton'
        )
        close_btn.pack(pady=(0, 20))
    
    def create_launcher(self, app_name, app_info):
        """Create launcher scripts for an app"""
        app_folder = app_info['folder']
        entry_point = app_info['entry_point']
        
        # Shell script
        sh_script = f"""#!/bin/bash
# Launcher for {app_name}

cd "$(dirname "$0")"

if ! command -v uv &> /dev/null; then
    echo "UV is not installed. Install it with: pip install uv"
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Creating environment..."
    uv venv
fi
"""
        
        if app_info['has_requirements']:
            sh_script += """
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    uv pip install -r requirements.txt
fi
"""
        elif app_info['dependencies']:
            deps = ' '.join(app_info['dependencies'])
            sh_script += f"""
echo "Installing dependencies..."
uv pip install {deps}
"""
        
        sh_script += f"""
echo "Running {entry_point}..."
.venv/bin/python {entry_point}
"""
        
        # Batch script
        bat_script = f"""@echo off
REM Launcher for {app_name}

cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo UV is not installed. Install it with: pip install uv
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating environment...
    uv venv
)
"""
        
        if app_info['has_requirements']:
            bat_script += """
if exist "requirements.txt" (
    echo Installing dependencies...
    uv pip install -r requirements.txt
)
"""
        elif app_info['dependencies']:
            deps = ' '.join(app_info['dependencies'])
            bat_script += f"""
echo Installing dependencies...
uv pip install {deps}
"""
        
        bat_script += f"""
echo Running {entry_point}...
.venv\\Scripts\\python.exe {entry_point}

pause
"""
        
        try:
            sh_path = app_folder / "run.sh"
            bat_path = app_folder / "run.bat"
            
            sh_path.write_text(sh_script, encoding='utf-8')
            bat_path.write_text(bat_script, encoding='utf-8')
            
            if sys.platform != 'win32':
                import stat
                sh_path.chmod(sh_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            
            messagebox.showinfo(
                "Success",
                f"Launcher scripts created! (\*.bat or \*.sh)\n\n"
                f"To Distribute, copy entire folder and send to the user. -May need Python installed on their machine.\n\n"
                f"Mac/Linux: run.sh\nWindows: run.bat\n\nLocation: {app_folder}"
            )
            
            self.status_var.set("Launcher scripts created")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create scripts:\n{str(e)}")
    
    def load_projects_path(self):
        """Load the saved projects path from config file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    projects_path = Path(config.get('projects_path', self.base_path / "projects"))
                    if projects_path.exists():
                        return projects_path
        except Exception:
            pass
        
        # Default to projects folder in same directory as launcher
        return self.base_path / "projects"
    
    def save_projects_path(self, path):
        """Save the projects path to config file"""
        try:
            config = {'projects_path': str(path)}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save configuration:\n{str(e)}")
    
    def change_projects_folder(self):
        """Allow user to select a different projects folder"""
        new_path = filedialog.askdirectory(
            title="Select Projects Folder",
            initialdir=self.projects_path,
            mustexist=True
        )
        
        if new_path:
            new_path = Path(new_path)
            self.projects_path = new_path
            self.save_projects_path(new_path)
            self.status_var.set(f"Projects folder changed to: {new_path}")
            self.scan_projects()
            
            messagebox.showinfo(
                "Folder Changed",
                f"Projects folder is now:\n{new_path}\n\nThe launcher will remember this location."
            )
    
    def open_projects_folder(self):
        """Open the projects folder"""
        import platform
        system = platform.system()
        
        try:
            if system == "Windows":
                subprocess.run(["explorer", str(self.projects_path)])
            elif system == "Darwin":
                subprocess.run(["open", str(self.projects_path)])
            else:
                subprocess.run(["xdg-open", str(self.projects_path)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
