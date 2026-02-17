import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import sys
import ctypes
if sys.platform.startswith("win"):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
import platform
import subprocess
import webbrowser
from datetime import datetime

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False
    print("CustomTkinter not available, using standard Tkinter")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() - 20
        
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None

class WatermarkText(scrolledtext.ScrolledText):
    def __init__(self, *args, **kwargs):
        scrolledtext.ScrolledText.__init__(self, *args, **kwargs)
        self.configure(bg='#2b2b2b', fg='white', insertbackground='white')
        self.tag_configure("watermark", foreground="gray", justify="center", font=("Arial", 24, "bold"))
        
    def update_watermark(self):
        self.delete("1.0", "end")
        
        content = self.get("1.0", "end-1c")
        
        if not content.strip():
            self.insert("1.0", "\n\n\nLΣⱮØπPy", "watermark")
        else:
            self.insert("end", "\n\nLΣⱮØπPy", "watermark")
            
        self.tag_lower("watermark")

class WindowsSecurityManager:
    def __init__(self):
        self.check_admin()
        
        if CTK_AVAILABLE:
            ctk.set_appearance_mode("Dark")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
        
        self.root.title("Windows Security Manager v3.0 - LΣⱮØπPy")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)
        
        self.security_tasks = {
            "windows_defender": {
                "name": "Windows Defender",
                "description": "Real-time antivirus and threat protection",
                "enabled": False
            },
            "windows_firewall": {
                "name": "Windows Firewall", 
                "description": "Network firewall for unauthorized access prevention",
                "enabled": False
            },
            "remote_desktop": {
                "name": "Remote Desktop (RDP)",
                "description": "Remote desktop connection control",
                "enabled": False
            },
            "user_account_control": {
                "name": "User Account Control (UAC)",
                "description": "System change notifications and control",
                "enabled": False
            },
            "windows_update": {
                "name": "Windows Update",
                "description": "Automatic security updates and patches",
                "enabled": False
            },
            "smart_screen": {
                "name": "Windows SmartScreen",
                "description": "Block malicious websites and downloads",
                "enabled": False
            },
            "core_isolation": {
                "name": "Core Isolation",
                "description": "Protect system memory from attacks",
                "enabled": False
            },
            "bitlocker": {
                "name": "BitLocker Encryption", 
                "description": "Full disk encryption for data protection",
                "enabled": False
            }
        }
        
        self.backup_available = False
        self.system_status = "grey"
        
        self.current_settings = {}
        
        self.log_text = None
        
        self.setup_gui()
        self.root.after(100, self.detect_current_status)
        
    def check_admin(self):
        """Ensure app runs as admin"""
        try:
            if ctypes.windll.shell32.IsUserAnAdmin() == 0:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()
        except:
            pass

    def run_powershell_command(self, command):
        """Run PowerShell command safely without showing window"""
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            result = subprocess.run([
                "powershell", "-WindowStyle", "Hidden", "-Command", command
            ], capture_output=True, text=True, timeout=60,
               creationflags=subprocess.CREATE_NO_WINDOW,
               startupinfo=startupinfo)
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)

    def detect_current_status(self):
        """Detect current status of all security features"""
        # Check if log_text is ready
        if not self.log_text:
            self.log_message("⚠️ Initializing security status detection...")
        
        self.log_message("🔍 Detecting current security status...")
        
        # Check Windows Defender status
        success, output = self.run_powershell_command(
            "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled"
        )
        if success and "True" in output:
            self.security_tasks["windows_defender"]["enabled"] = True
            self.log_status_message("Windows Defender", True)
        else:
            self.security_tasks["windows_defender"]["enabled"] = False
            self.log_status_message("Windows Defender", False)
        
        # Check Firewall status
        success, output = self.run_powershell_command(
            "Get-NetFirewallProfile | Where-Object {$_.Enabled -eq $True} | Select-Object -First 1"
        )
        if success and output.strip():
            self.security_tasks["windows_firewall"]["enabled"] = True
            self.log_status_message("Windows Firewall", True)
        else:
            self.security_tasks["windows_firewall"]["enabled"] = False
            self.log_status_message("Windows Firewall", False)
        
        # Check RDP status
        success, output = self.run_powershell_command(
            "reg query \"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections"
        )
        if success and "0x0" in output:
            self.security_tasks["remote_desktop"]["enabled"] = True
            self.log_status_message("Remote Desktop", True)
        else:
            self.security_tasks["remote_desktop"]["enabled"] = False
            self.log_status_message("Remote Desktop", False)
        
        # Check UAC status
        success, output = self.run_powershell_command(
            "reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA"
        )
        if success and "0x1" in output:
            self.security_tasks["user_account_control"]["enabled"] = True
            self.log_status_message("User Account Control", True)
        else:
            self.security_tasks["user_account_control"]["enabled"] = False
            self.log_status_message("User Account Control", False)
        
        # Check Windows Update status
        success, output = self.run_powershell_command(
            "Get-Service -Name wuauserv | Select-Object Status"
        )
        if success and "Running" in output:
            self.security_tasks["windows_update"]["enabled"] = True
            self.log_status_message("Windows Update", True)
        else:
            self.security_tasks["windows_update"]["enabled"] = False
            self.log_status_message("Windows Update", False)
        
        # Check SmartScreen status
        success, output = self.run_powershell_command(
            "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AppHost' -Name 'EnableWebContentEvaluation' -ErrorAction SilentlyContinue"
        )
        if success and "1" in output:
            self.security_tasks["smart_screen"]["enabled"] = True
            self.log_status_message("Windows SmartScreen", True)
        else:
            self.security_tasks["smart_screen"]["enabled"] = False
            self.log_status_message("Windows SmartScreen", False)
        
        # Check Core Isolation status
        success, output = self.run_powershell_command(
            "Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' -Name 'Enabled' -ErrorAction SilentlyContinue"
        )
        if success and "1" in output:
            self.security_tasks["core_isolation"]["enabled"] = True
            self.log_status_message("Core Isolation", True)
        else:
            self.security_tasks["core_isolation"]["enabled"] = False
            self.log_status_message("Core Isolation", False)
        
        # Check BitLocker status
        success, output = self.run_powershell_command(
            "Manage-BDE -Status C: -ErrorAction SilentlyContinue | Where-Object {$_.ProtectionStatus -eq 'On'}"
        )
        if success and output.strip():
            self.security_tasks["bitlocker"]["enabled"] = True
            self.log_status_message("BitLocker Encryption", True)
        else:
            self.security_tasks["bitlocker"]["enabled"] = False
            self.log_status_message("BitLocker Encryption", False)
        
        self.log_message("✅ Security status detection completed")
        self.update_display_settings()

    def log_status_message(self, message, status):
        """Log message with colored status (ENABLED/DISABLED)"""
        # Safe logging - check if log_text exists
        if not hasattr(self, 'log_text') or self.log_text is None:
            print(f"LOG: {message}: {'ENABLED' if status else 'DISABLED'}")
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        try:
            self.log_text.config(state="normal")
            self.log_text.insert("end", f"[{timestamp}] {message}: ")
            
            # SPECIAL CASE: For Remote Desktop, reverse the colors
            if "Remote Desktop" in message:
                if status:  # Enabled - DANGEROUS
                    self.log_text.insert("end", "ENABLED ⚠️", "red")
                else:  # Disabled - SAFE
                    self.log_text.insert("end", "DISABLED ✅", "green")
            else:
                # Normal behavior for other settings
                if status:
                    self.log_text.insert("end", "ENABLED", "green")
                else:
                    self.log_text.insert("end", "DISABLED", "red")
            
            self.log_text.insert("end", "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
            
            # Update watermark position
            if hasattr(self.log_text, 'update_watermark'):
                self.log_text.update_watermark()
            self.root.update()
        except Exception as e:
            print(f"Error logging message: {e}")

    def log_message(self, message, tag=None):
        """Add message to log with optional color tag"""
        # Safe logging - check if log_text exists
        if not hasattr(self, 'log_text') or self.log_text is None:
            print(f"LOG: {message}")
            return
            
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            # Insert the message
            self.log_text.config(state="normal")
            if tag:
                self.log_text.insert("end", log_entry, tag)
            else:
                self.log_text.insert("end", log_entry)
            self.log_text.see("end")
            self.log_text.config(state="disabled")
            
            # Update watermark position
            self.log_text.update_watermark()
            
            self.root.update()
        except Exception as e:
            print(f"Error logging message: {e}")

    def setup_gui(self):
        """Setup user interface"""
        if CTK_AVAILABLE:
            self.setup_gui_ctk()
        else:
            self.setup_gui_standard()
    
    def setup_gui_ctk(self):
        """Setup GUI using CustomTkinter"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="#240FE2")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ctk.CTkLabel(header_frame, 
                                  text="Windows Security Manager - LΣⱮØπPy",
                                  text_color="white",
                                  font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame for top buttons (centered)
        top_button_frame = ctk.CTkFrame(main_frame, height=50, fg_color="transparent")
        top_button_frame.pack(fill="x", pady=(0, 10))
        top_button_frame.pack_propagate(False)
        
        # Inner frame for centering buttons
        inner_top_frame = ctk.CTkFrame(top_button_frame, fg_color="transparent")
        inner_top_frame.pack(expand=True)
        
        # Check Status Button
        self.status_btn = ctk.CTkButton(inner_top_frame, text="Check All Status", 
                                       command=self.check_all_status,
                                       width=120, height=35, 
                                       corner_radius=8,
                                       fg_color="#240FE2", hover_color="#1A0BB9")
        self.status_btn.pack(side="left", padx=10)
        ToolTip(self.status_btn, "Check current status of all security features")
        
        # Enable All Button
        self.enable_all_btn = ctk.CTkButton(inner_top_frame, text="Enable All", 
                                           command=self.enable_all_security,
                                           width=120, height=35, 
                                           corner_radius=8,
                                           fg_color="green", hover_color="#006400")
        self.enable_all_btn.pack(side="left", padx=10)
        ToolTip(self.enable_all_btn, "Enable all security features")
        
        # Disable All Button
        self.disable_all_btn = ctk.CTkButton(inner_top_frame, text="Disable All", 
                                            command=self.disable_all_security,
                                            width=120, height=35, 
                                            corner_radius=8,
                                            fg_color="red", hover_color="#8B0000")
        self.disable_all_btn.pack(side="left", padx=10)
        ToolTip(self.disable_all_btn, "Disable all security features")
        
        # Create Backup Button
        self.backup_btn = ctk.CTkButton(inner_top_frame, text="Create Backup", 
                                       command=self.create_backup,
                                       width=120, height=35, 
                                       corner_radius=8,
                                       fg_color="orange", hover_color="#CC5500")
        self.backup_btn.pack(side="left", padx=10)
        ToolTip(self.backup_btn, "Create backup of current security settings")
        
        # Frame for security settings (2 columns)
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=(0, 10))
        
        # Left settings frame
        left_frame = ctk.CTkFrame(settings_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Right settings frame
        right_frame = ctk.CTkFrame(settings_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Security settings configuration
        security_settings = [
            ("Windows Defender", "windows_defender", "Essential real-time antivirus protection that continuously\nmonitors for malware, viruses, and security threats to keep your system safe."),
            ("Windows Firewall", "windows_firewall", "Network security system that monitors and controls all traffic\nbased on security rules to prevent unauthorized access to your computer."),
            ("Remote Desktop", "remote_desktop", "Allows remote connections to your computer from other devices.\nDisabling enhances security by closing potential entry points for attackers."),
            ("User Account Control", "user_account_control", "Security feature that prompts for permission when programs try\nchanges, preventing unauthorized system modifications and malware installation."),
            ("Windows Update", "windows_update", "Automatically downloads and installs critical security patches\nto protect against newly discovered vulnerabilities and security threats."),
            ("Windows SmartScreen", "smart_screen", "Filters malicious websites and downloads by checking against\na threat database, blocking phishing attempts and malware attacks."),
            ("Core Isolation", "core_isolation", "Advanced security feature that isolates core system processes\nin a secure environment to protect against memory-based attacks."),
            ("BitLocker Encryption", "bitlocker", "Full disk encryption technology that secures your entire hard drive,\nprotecting data if your device is lost, stolen, or accessed unauthorized.")
        ]
        
        # Split into two columns
        left_settings = security_settings[:4]
        right_settings = security_settings[4:]
        
        self.left_vars = {}
        for text, key, tooltip in left_settings:
            self.create_security_setting_row(left_frame, text, key, self.left_vars, tooltip)
        
        self.right_vars = {}
        for text, key, tooltip in right_settings:
            self.create_security_setting_row(right_frame, text, key, self.right_vars, tooltip)
        
        # Output log
        log_label = ctk.CTkLabel(main_frame, text="   Security Activity Log:", anchor="w")
        log_label.pack(fill="x", pady=(10, 5))
        
        # Create custom text widget with dark background and watermark
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.log_text = WatermarkText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
        
        # Configure text tags for colored output
        self.log_text.tag_config("red", foreground="red")
        self.log_text.tag_config("green", foreground="green")
        self.log_text.tag_config("yellow", foreground="orange")
        self.log_text.tag_config("blue", foreground="blue")
        
        # Frame for bottom action buttons (centered)
        bottom_button_frame = ctk.CTkFrame(main_frame, height=50, fg_color="transparent")
        bottom_button_frame.pack(fill="x")
        bottom_button_frame.pack_propagate(False)
        
        # Inner frame for centering buttons
        inner_bottom_frame = ctk.CTkFrame(bottom_button_frame, fg_color="transparent")
        inner_bottom_frame.pack(expand=True)
        
        # Apply Selected Button (Green)
        self.apply_btn = ctk.CTkButton(inner_bottom_frame, text="Apply Selected", 
                                      command=self.apply_selected_settings,
                                      width=120, height=35,
                                      fg_color="green", hover_color="#006400")
        self.apply_btn.pack(side="left", padx=10, pady=10)
        ToolTip(self.apply_btn, "Apply all selected security settings changes")
        
        # Quick Actions Button (Blue)
        self.quick_btn = ctk.CTkButton(inner_bottom_frame, text="Quick Actions", 
                                      command=self.show_quick_actions,
                                      width=120, height=35,
                                      fg_color="#240FE2", hover_color="#1A0BB9")
        self.quick_btn.pack(side="left", padx=10, pady=10)
        ToolTip(self.quick_btn, "Show quick security actions menu")
        
        # Website Button (Purple)
        self.website_btn = ctk.CTkButton(inner_bottom_frame, text="LΣⱮØπPy", 
                                        command=self.open_website,
                                        width=100, height=35,
                                        fg_color="purple", hover_color="#4B0082")
        self.website_btn.pack(side="left", padx=10, pady=10)
        ToolTip(self.website_btn, "Visit our website")
        
        # Donate Button (Purple)
        self.donate_btn = ctk.CTkButton(inner_bottom_frame, text="Donate Page", 
                                       command=self.open_donate,
                                       width=100, height=35,
                                       fg_color="purple", hover_color="#4B0082")
        self.donate_btn.pack(side="left", padx=10, pady=10)
        ToolTip(self.donate_btn, "Support our project")

    def create_security_setting_row(self, parent, text, key, var_dict, tooltip_text):
        """Create security setting row with colored boxes"""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=3)
        
        # Setting label with tooltip
        label = ctk.CTkLabel(frame, text=text, width=180, anchor="w")
        label.pack(side="left", padx=5)
        ToolTip(label, tooltip_text)
        
        var = tk.BooleanVar()
        var_dict[key] = var
        
        # Enable box (Green when selected)
        enable_frame = ctk.CTkFrame(frame, width=80, height=28, corner_radius=5)
        enable_frame.pack(side="left", padx=2)
        enable_frame.pack_propagate(False)
        
        enable_btn = ctk.CTkRadioButton(enable_frame, text="Enable", variable=var, 
                                      value=True, command=lambda: self.on_setting_change(key),
                                      width=70, height=24, corner_radius=4)
        enable_btn.pack(expand=True)
        ToolTip(enable_btn, f"Enable {text}")
        
        # Disable box (Red when selected)
        disable_frame = ctk.CTkFrame(frame, width=80, height=28, corner_radius=5)
        disable_frame.pack(side="left", padx=2)
        disable_frame.pack_propagate(False)
        
        disable_btn = ctk.CTkRadioButton(disable_frame, text="Disable", variable=var, 
                                       value=False, command=lambda: self.on_setting_change(key),
                                       width=70, height=24, corner_radius=4)
        disable_btn.pack(expand=True)
        ToolTip(disable_btn, f"Disable {text}")
        
        # Action buttons frame - FIXED: Pastikan width cukup untuk kedua-dua button
        action_frame = ctk.CTkFrame(frame, width=140, height=28, corner_radius=5, fg_color="transparent")
        action_frame.pack(side="right", padx=5)
        action_frame.pack_propagate(False)
        
        # Check button - FIXED: Pastikan button ini wujud dan berfungsi
        check_btn = ctk.CTkButton(action_frame, text="Check", 
                                 command=lambda: self.check_single_status(key),
                                 width=60, height=24,
                                 fg_color="#240FE2", hover_color="#1A0BB9",
                                 font=("Arial", 10))
        check_btn.pack(side="left", padx=2)
        ToolTip(check_btn, f"Check current status of {text}")
        
        # Apply button - FIXED: Pastikan button ini wujud dan berfungsi
        apply_btn = ctk.CTkButton(action_frame, text="Apply", 
                                 command=lambda: self.apply_single_setting(key),
                                 width=60, height=24,
                                 fg_color="green", hover_color="#006400",
                                 font=("Arial", 10))
        apply_btn.pack(side="left", padx=2)
        ToolTip(apply_btn, f"Apply {text} setting")
        
        # Store references for color updates
        if not hasattr(self, 'setting_widgets'):
            self.setting_widgets = {}
        self.setting_widgets[key] = {
            'enable_frame': enable_frame,
            'disable_frame': disable_frame,
            'enable_btn': enable_btn,
            'disable_btn': disable_btn,
            'label': label,
            'frame': frame,
            'var': var,
            'check_btn': check_btn,
            'apply_btn': apply_btn
        }

    def update_setting_colors(self):
        """Update colors based on current selection"""
        all_vars = {**self.left_vars, **self.right_vars}
        
        for key, var in all_vars.items():
            widgets = self.setting_widgets.get(key)
            if widgets:
                # SPECIAL CASE: Remote Desktop - Disabled is GOOD (Green), Enabled is BAD (Red)
                if key == "remote_desktop":
                    if var.get():  # Enabled - DANGEROUS (Red)
                        widgets['enable_frame'].configure(fg_color="red")
                        widgets['disable_frame'].configure(fg_color="#2b2b2b")
                        widgets['enable_btn'].configure(fg_color="darkred", hover_color="red")
                        widgets['disable_btn'].configure(fg_color="#2b2b2b", hover_color="#3b3b3b")
                    else:  # Disabled - SAFE (Green)
                        widgets['enable_frame'].configure(fg_color="#2b2b2b")
                        widgets['disable_frame'].configure(fg_color="green")
                        widgets['enable_btn'].configure(fg_color="#2b2b2b", hover_color="#3b3b3b")
                        widgets['disable_btn'].configure(fg_color="darkgreen", hover_color="green")
                else:
                    # Normal behavior for other settings
                    if var.get():  # Enabled
                        widgets['enable_frame'].configure(fg_color="green")
                        widgets['disable_frame'].configure(fg_color="#2b2b2b")
                        widgets['enable_btn'].configure(fg_color="darkgreen", hover_color="green")
                        widgets['disable_btn'].configure(fg_color="#2b2b2b", hover_color="#3b3b3b")
                    else:  # Disabled
                        widgets['enable_frame'].configure(fg_color="#2b2b2b")
                        widgets['disable_frame'].configure(fg_color="red")
                        widgets['enable_btn'].configure(fg_color="#2b2b2b", hover_color="#3b3b3b")
                        widgets['disable_btn'].configure(fg_color="darkred", hover_color="red")

    def update_display_settings(self):
        """Update display based on current security settings"""
        all_vars = {**self.left_vars, **self.right_vars}
        for key, var in all_vars.items():
            if key in self.security_tasks:
                var.set(self.security_tasks[key]["enabled"])
        
        # Update colors after setting values
        self.update_setting_colors()

    def on_setting_change(self, key):
        """Handle setting changes"""
        value = self.left_vars.get(key, self.right_vars.get(key)).get()
        status = "ENABLED" if value else "DISABLED"
        task_name = self.security_tasks[key]["name"]
        
        self.log_message(f"⚙️ Setting {task_name} changed to: {status}")
        self.update_setting_colors()

    def check_all_status(self):
        """Check status of all security features"""
        self.log_message("🔍 Checking status of all security features...")
        self.detect_current_status()

    def check_single_status(self, key):
        """Check status of single security feature"""
        task_name = self.security_tasks[key]["name"]
        current_status = self.security_tasks[key]["enabled"]
        
        # Run specific check command for each feature
        check_commands = {
            "windows_defender": "Get-MpComputerStatus | Select-Object RealTimeProtectionEnabled",
            "windows_firewall": "Get-NetFirewallProfile | Where-Object {$_.Enabled -eq $True} | Select-Object -First 1",
            "remote_desktop": "reg query \"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections",
            "user_account_control": "reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA",
            "windows_update": "Get-Service -Name wuauserv | Select-Object Status",
            "smart_screen": "Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AppHost' -Name 'EnableWebContentEvaluation' -ErrorAction SilentlyContinue",
            "core_isolation": "Get-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' -Name 'Enabled' -ErrorAction SilentlyContinue",
            "bitlocker": "Manage-BDE -Status C: -ErrorAction SilentlyContinue | Where-Object {$_.ProtectionStatus -eq 'On'}"
        }
        
        if key in check_commands:
            success, output = self.run_powershell_command(check_commands[key])
            if success:
                if any(x in output for x in ["True", "0x0", "Running", "1", "On"]):
                    detected_status = True
                    status_text = "ENABLED"
                else:
                    detected_status = False
                    status_text = "DISABLED"
                
                self.security_tasks[key]["enabled"] = detected_status
                self.update_display_settings()
                self.log_message(f"📊 {task_name}: {status_text} (Current Status)")
            else:
                self.log_message(f"❌ Failed to check {task_name} status")

    def apply_selected_settings(self):
        """Apply all selected security settings"""
        self.log_message("🚀 Applying selected security settings...")
        
        # Update security tasks based on user selection
        all_vars = {**self.left_vars, **self.right_vars}
        for key, var in all_vars.items():
            self.security_tasks[key]["enabled"] = var.get()
            
        # Apply settings using PowerShell
        self.apply_settings_with_powershell()
        self.log_message("✅ All security settings applied successfully")
        self.update_setting_colors()

    def apply_single_setting(self, key):
        """Apply single security setting"""
        task_name = self.security_tasks[key]["name"]
        enable = self.left_vars.get(key, self.right_vars.get(key)).get()
        
        self.log_message(f"🔄 Applying {task_name}...")
        
        if enable:
            self.enable_single_task(key)
        else:
            self.disable_single_task(key)

    def enable_single_task(self, key):
        """Enable single security task"""
        task_name = self.security_tasks[key]["name"]
        
        enable_commands = {
            "windows_defender": "Set-MpPreference -DisableRealtimeMonitoring $false; Start-Service -Name WinDefend",
            "windows_firewall": "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True",
            "remote_desktop": "reg add \"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 0 /f; netsh advfirewall firewall set rule group=\"remote desktop\" new enable=Yes",
            "user_account_control": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA /t REG_DWORD /d 1 /f; reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 5 /f",
            "windows_update": "Set-Service -Name wuauserv -StartupType Automatic; Start-Service -Name wuauserv; Set-Service -Name BITS -StartupType Automatic; Start-Service -Name BITS",
            "smart_screen": "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AppHost' -Name 'EnableWebContentEvaluation' -Value 1; Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System' -Name 'EnableSmartScreen' -Value 1 -ErrorAction SilentlyContinue",
            "core_isolation": "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' -Name 'Enabled' -Value 1 -ErrorAction SilentlyContinue",
            "bitlocker": "Manage-BDE -On C: -RecoveryPassword -UsedSpaceOnly -ErrorAction SilentlyContinue"
        }
        
        if key in enable_commands:
            success, output = self.run_powershell_command(enable_commands[key])
            if success:
                self.security_tasks[key]["enabled"] = True
                self.update_display_settings()
                self.log_message(f"✅ {task_name} enabled successfully")
            else:
                self.log_message(f"⚠️ {task_name} enable may need manual configuration: {output}")

    def disable_single_task(self, key):
        """Disable single security task"""
        task_name = self.security_tasks[key]["name"]
        
        disable_commands = {
            "windows_defender": "Set-MpPreference -DisableRealtimeMonitoring $true; Stop-Service -Name WinDefend -Force",
            "windows_firewall": "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False",
            "remote_desktop": "reg add \"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 1 /f; netsh advfirewall firewall set rule group=\"remote desktop\" new enable=No",
            "user_account_control": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA /t REG_DWORD /d 0 /f; reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 0 /f",
            "windows_update": "Set-Service -Name wuauserv -StartupType Disabled; Stop-Service -Name wuauserv -Force; Set-Service -Name BITS -StartupType Disabled; Stop-Service -Name BITS -Force",
            "smart_screen": "Set-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\AppHost' -Name 'EnableWebContentEvaluation' -Value 0; Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System' -Name 'EnableSmartScreen' -Value 0 -ErrorAction SilentlyContinue",
            "core_isolation": "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity' -Name 'Enabled' -Value 0 -ErrorAction SilentlyContinue",
            "bitlocker": "Manage-BDE -Off C: -ErrorAction SilentlyContinue"
        }
        
        if key in disable_commands:
            success, output = self.run_powershell_command(disable_commands[key])
            if success:
                self.security_tasks[key]["enabled"] = False
                self.update_display_settings()
                self.log_message(f"✅ {task_name} disabled successfully")
            else:
                self.log_message(f"⚠️ {task_name} disable may need manual configuration: {output}")

    def apply_settings_with_powershell(self):
        """Apply security settings using actual PowerShell commands"""
        for key, task_data in self.security_tasks.items():
            enable = task_data["enabled"]
            
            if enable:
                self.enable_single_task(key)
            else:
                self.disable_single_task(key)

    def enable_all_security(self):
        """Enable all security features"""
        self.log_message("🔄 Enabling all security features...")
        
        all_vars = {**self.left_vars, **self.right_vars}
        for key, var in all_vars.items():
            var.set(True)
            self.security_tasks[key]["enabled"] = True
            
        self.apply_settings_with_powershell()
        self.log_message("✅ All security features enabled")
        self.update_setting_colors()

    def disable_all_security(self):
        """Disable all security features"""
        if not messagebox.askyesno("Warning", "This will disable all security features. Are you sure?"):
            return
            
        self.log_message("🔄 Disabling all security features...")
        
        all_vars = {**self.left_vars, **self.right_vars}
        for key, var in all_vars.items():
            var.set(False)
            self.security_tasks[key]["enabled"] = False
            
        self.apply_settings_with_powershell()
        self.log_message("✅ All security features disabled")
        self.update_setting_colors()

    def create_backup(self):
        """Create backup of current security settings"""
        try:
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "windows_version": platform.system() + " " + platform.release(),
                "security_settings": self.security_tasks.copy()
            }
            
            with open("security_backup.json", "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)
            
            self.log_message("✅ Security backup created successfully: security_backup.json")
            
        except Exception as e:
            self.log_message(f"❌ Error creating backup: {str(e)}")

    def show_quick_actions(self):
        """Show quick security actions menu"""
        quick_menu = tk.Menu(self.root, tearoff=0)
        quick_menu.add_command(label="Open Windows Security", command=self.open_windows_security)
        quick_menu.add_command(label="Check Firewall Status", command=self.check_firewall_status)
        quick_menu.add_command(label="Update Defender Definitions", command=self.update_definitions)
        quick_menu.add_command(label="Create Restore Point", command=self.create_restore_point)
        
        # Show menu at button position
        try:
            quick_menu.tk_popup(self.quick_btn.winfo_rootx(), 
                              self.quick_btn.winfo_rooty() + self.quick_btn.winfo_height())
        finally:
            quick_menu.grab_release()

    def open_windows_security(self):
        """Open Windows Security app"""
        self.log_message("🌐 Opening Windows Security...")
        os.system("start windowsdefender:")

    def check_firewall_status(self):
        """Check detailed firewall status"""
        self.log_message("🔍 Checking detailed firewall status...")
        success, output = self.run_powershell_command(
            "Get-NetFirewallProfile | Format-Table Name, Enabled -AutoSize"
        )
        if success:
            self.log_message(f"📊 Firewall Status:\n{output}")

    def update_definitions(self):
        """Update Windows Defender definitions"""
        self.log_message("🔄 Updating Windows Defender definitions...")
        success, output = self.run_powershell_command("Update-MpSignature")
        if success:
            self.log_message("✅ Definitions updated successfully")
        else:
            self.log_message("❌ Failed to update definitions")

    def create_restore_point(self):
        """Create system restore point"""
        self.log_message("🔄 Creating system restore point...")
        success, output = self.run_powershell_command(
            "Checkpoint-Computer -Description \"Security Manager Restore Point\" -RestorePointType MODIFY_SETTINGS"
        )
        if success:
            self.log_message("✅ System restore point created successfully")
        else:
            self.log_message("❌ Failed to create restore point")

    def open_website(self):
        """Open website"""
        self.log_message("🌐 Opening website...")
        webbrowser.open("https://lemonpyhub.github.io/")

    def open_donate(self):
        """Open donate page"""
        self.log_message("💝 Opening donate page...")
        webbrowser.open("https://lemonpyhub.github.io/donate/")

    def setup_gui_standard(self):
        """Setup GUI using standard Tkinter (fallback)"""
        pass

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WindowsSecurityManager()
    app.run()