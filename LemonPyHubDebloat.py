import tkinter as tk
import customtkinter as ctk
import pywinstyles
import subprocess
import webbrowser
import ctypes
import sys
from tkinter import messagebox

# ==========================================
# ADMIN PRIVILEGE CHECK & AUTO-ELEVATE
# ==========================================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show_tip(self):
        if self.tip_window or not self.text: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes("-topmost", True)
        label = tk.Label(tw, text=self.text, justify="left", background="#2b2b2b", 
                         foreground="#ffffff", relief="solid", borderwidth=1, 
                         font=("Segoe UI", 9), padx=8, pady=4)
        label.pack()

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw: tw.destroy()

def add_tooltip(widget, text):
    tooltip = ToolTip(widget, text)
    widget.bind("<Enter>", lambda e: tooltip.show_tip())
    widget.bind("<Leave>", lambda e: tooltip.hide_tip())

class LemonPyHubDebloat(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LemonPyHub: Windows Debloater & Privacy")
        self.geometry("930x650")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.bloatware_info = {
            "Microsoft.ZuneVideo": "Movies & TV: Default player for local video files.",
            "Microsoft.ZuneMusic": "Media Player: Used for MP3s and local music playback.",
            "Microsoft.XboxApp": "Xbox Companion: Necessary for Xbox social and game syncing.",
            "Microsoft.WindowsCommunicationsApps": "Mail and Calendar: Default email/calendar apps.",
            "Microsoft.People": "Contacts: Manages contact list across Microsoft apps.",
            "Microsoft.BingNews": "News: Integrated news feed in the Start menu.",
            "Microsoft.BingWeather": "Weather: Provides weather forecasts and widgets.",
            "Microsoft.SkypeApp": "Skype: Default video calling and messaging.",
            "Microsoft.GetHelp": "Get Help: Support tool for Windows troubleshooting.",
            "Microsoft.YourPhone": "Phone Link: Syncs mobile notifications to PC.",
            "Microsoft.MixedReality.Portal": "Mixed Reality: Software for VR/AR support.",
            "Microsoft.MicrosoftSolitaireCollection": "Solitaire: Default card game collection.",
            "Microsoft.WindowsFeedbackHub": "Feedback Hub: Send feedback to Microsoft.",
            "Microsoft.Wallet": "Wallet: Payment management for Store services.",
            "Microsoft.GamingApp": "Xbox App: Modern gaming interface for Win 10/11."
        }
        self.bloatware_data = list(self.bloatware_info.keys())
        self.checkbox_vars = {}
        self.debloat_widgets = {}
        self.restore_widgets = {}

        self.setup_sidebar()
        self.setup_main_frames()
        self.setup_status_bar()
        
        try:
            pywinstyles.apply_style(self, "mica")
        except:
            pass 

        self.refresh_app_status(silent=True)
        self.show_page("debloater")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="LemonPyHub", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=30)

        self.btn_nav_debloat = self.create_nav_btn("Debloater", "debloater")
        self.btn_nav_privacy = self.create_nav_btn("Privacy Settings", "privacy")
        self.btn_nav_restore = self.create_nav_btn("Restore Center", "restore")
        
        bottom_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        bottom_container.pack(side="bottom", fill="x", pady=20, padx=20)

        self.btn_refresh = ctk.CTkButton(bottom_container, text="↻ Refresh Status", fg_color="gray25", 
                                         command=self.refresh_app_status)
        self.btn_refresh.pack(fill="x", pady=(0, 15))

        self.btn_home = ctk.CTkButton(bottom_container, text="LΣⱮØπPyHub", fg_color="#2980b9", 
                                      command=lambda: webbrowser.open("https://lemonpyhub.github.io"))
        self.btn_home.pack(fill="x", pady=5)

        self.btn_donate = ctk.CTkButton(bottom_container, text="Coffee", fg_color="#27ae60", 
                                        command=lambda: webbrowser.open("https://lemonpyhub.github.io/donate/"))
        self.btn_donate.pack(fill="x", pady=5)

    def setup_status_bar(self):
        is_admin_active = is_admin()
        status_color = "#27ae60" if is_admin_active else "#e74c3c"
        status_text = "MODE: ADMINISTRATOR (FULL ACCESS)" if is_admin_active else "MODE: USER (LIMITED ACCESS)"
        
        self.status_bar = ctk.CTkFrame(self, height=28, corner_radius=0, fg_color="#1a1a1a")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.status_bar, text=status_text, font=("Segoe UI", 11, "bold"), text_color=status_color)
        self.status_label.pack(side="left", padx=20)

    def create_nav_btn(self, text, page):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, fg_color="transparent", anchor="w",
                            command=lambda: self.show_page(page))
        btn.pack(fill="x", padx=20, pady=5)
        return btn

    def setup_main_frames(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        
        # Page 1: Debloater
        debloat_desc = (
            "Windows comes pre-installed with background apps that consume CPU, RAM, and disk space. "
            "By removing these 'bloatware' packages, you can improve system boot times, free up resources for gaming or work, "
            "and create a cleaner, distraction-free Start menu environment."
        )
        self.debloater_frame = self.create_app_list_page("Windows Debloater", debloat_desc, "Remove Selected", "#e74c3c", self.execute_debloat, "debloat")
        
        # Page 2: Privacy
        self.privacy_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        ctk.CTkLabel(self.privacy_frame, text="Privacy Dashboard", font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=10)
        
        info_card = ctk.CTkFrame(self.privacy_frame, corner_radius=12, fg_color=("#ebebeb", "#2b2b2b"))
        info_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(info_card, text="What is Windows Telemetry?", font=("Segoe UI", 16, "bold"), text_color="#3498db").pack(anchor="w", padx=20, pady=(15, 5))
        
        p_desc = ctk.CTkLabel(info_card, text=(
            "Windows Telemetry is an automated data collection system that monitors how you use your PC. "
            "It sends usage patterns, app data, and error reports to Microsoft servers.\n\n"
            "• Disabling this enhances your personal privacy.\n"
            "• Reduces unnecessary background network traffic.\n"
            "• Stops the creation of advertising profiles based on your behavior."
        ), justify="left", wraplength=650)
        p_desc.pack(anchor="w", padx=20, pady=(0, 15))

        # Privacy Action Card with Status
        action_card = ctk.CTkFrame(self.privacy_frame, corner_radius=12)
        action_card.pack(fill="x", pady=10)
        
        status_container = ctk.CTkFrame(action_card, fg_color="transparent")
        status_container.pack(side="left", padx=20, pady=20)
        
        ctk.CTkLabel(status_container, text="Privacy Actions", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        
        # REALTIME STATUS LABEL
        self.privacy_status_lbl = ctk.CTkLabel(status_container, text="Status: Checking...", font=("Segoe UI", 12))
        self.privacy_status_lbl.pack(anchor="w")

        btn_grp = ctk.CTkFrame(action_card, fg_color="transparent")
        btn_grp.pack(side="right", padx=20)
        ctk.CTkButton(btn_grp, text="Apply Privacy Fix", fg_color="#e74c3c", command=self.execute_privacy).pack(side="left", padx=5)
        ctk.CTkButton(btn_grp, text="Undo (Default)", fg_color="gray25", command=self.undo_privacy).pack(side="left", padx=5)

        # Page 3: Restore
        restore_desc = (
            "If you find that you need a specific app that was previously removed, you can reinstall it here. "
            "Restoring apps will register them back to your system using the original Windows Store manifest, "
            "returning your PC's functionality to its default state."
        )
        self.restore_frame = self.create_app_list_page("Restore Center", restore_desc, "Restore Selected", "#03a511", self.execute_reinstall, "restore")

    def create_app_list_page(self, title, desc, btn_text, btn_color, command, type_page):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(frame, text=desc, text_color="gray", wraplength=700, justify="left").pack(anchor="w", pady=(0, 20))
        
        scroll = ctk.CTkScrollableFrame(frame, label_text="System Packages")
        scroll.pack(fill="both", expand=True, pady=10)

        for app_id in self.bloatware_data:
            if app_id not in self.checkbox_vars:
                self.checkbox_vars[app_id] = ctk.BooleanVar(value=False)
            
            cb = ctk.CTkCheckBox(scroll, text=app_id.replace("Microsoft.", ""), variable=self.checkbox_vars[app_id])
            cb.pack(pady=8, padx=10, anchor="w")
            add_tooltip(cb, self.bloatware_info.get(app_id, "No data available."))
            
            if type_page == "debloat":
                self.debloat_widgets[app_id] = cb
            else:
                self.restore_widgets[app_id] = cb

        ctk.CTkButton(frame, text=btn_text, fg_color=btn_color, command=command).pack(pady=20, side="right")
        return frame

    def check_privacy_status(self):
        """Checks if Telemetry is currently disabled in Registry."""
        try:
            cmd = 'Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry"'
            result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, creationflags=0x08000000)
            
            if "AllowTelemetry : 0" in result.stdout:
                self.privacy_status_lbl.configure(text="Status: TELEMETRY DISABLED (PROTECTED)", text_color="#27ae60")
            else:
                self.privacy_status_lbl.configure(text="Status: TELEMETRY ENABLED (DEFAULT)", text_color="#e67e22")
        except:
            self.privacy_status_lbl.configure(text="Status: UNKNOWN", text_color="gray")

    def refresh_app_status(self, silent=False):
        self.btn_refresh.configure(text="⌛ Scanning...", state="disabled", fg_color="#d35400")
        self.update_idletasks() 
        
        # Check Privacy Status too during refresh
        self.check_privacy_status()

        try:
            result = subprocess.run(["powershell", "-Command", "Get-AppxPackage | Select-Object -ExpandProperty Name"], 
                                    capture_output=True, text=True, creationflags=0x08000000)
            installed_apps = result.stdout
        except:
            installed_apps = ""

        for app_id in self.bloatware_data:
            is_installed = app_id in installed_apps
            clean_name = app_id.replace("Microsoft.", "")
            if app_id in self.debloat_widgets:
                if is_installed:
                    self.debloat_widgets[app_id].configure(text=f"{clean_name} [INSTALLED]", state="normal", text_color="#ffffff")
                else:
                    self.debloat_widgets[app_id].configure(text=f"{clean_name} [REMOVED]", state="disabled", text_color="gray")
                    self.checkbox_vars[app_id].set(False)
            if app_id in self.restore_widgets:
                if not is_installed:
                    self.restore_widgets[app_id].configure(text=f"{clean_name} [AVAILABLE]", state="normal", text_color="#2ecc71")
                else:
                    self.restore_widgets[app_id].configure(text=f"{clean_name} [INSTALLED]", state="disabled", text_color="gray")
                    self.checkbox_vars[app_id].set(False)

        self.btn_refresh.configure(text="↻ Refresh Status", state="normal", fg_color="gray25")
        if not silent:
            messagebox.showinfo("Scanner", "System scan complete!")

    def show_page(self, page_name):
        pages = {"debloater": self.debloater_frame, "privacy": self.privacy_frame, "restore": self.restore_frame}
        btns = {"debloater": self.btn_nav_debloat, "privacy": self.btn_nav_privacy, "restore": self.btn_nav_restore}
        for p in pages.values(): p.grid_forget()
        for b in btns.values(): b.configure(fg_color="transparent")
        pages[page_name].grid(row=0, column=0, sticky="nsew")
        btns[page_name].configure(fg_color=("gray75", "gray25"))
        
        # Refresh status when entering privacy page
        if page_name == "privacy":
            self.check_privacy_status()

    def execute_debloat(self):
        selected = [app for app, var in self.checkbox_vars.items() if var.get()]
        if not selected: return
        if messagebox.askyesno("Confirm", f"Uninstall {len(selected)} apps?"):
            for app in selected:
                subprocess.run(["powershell", "-Command", f"Get-AppxPackage *{app}* | Remove-AppxPackage"], 
                               capture_output=True, creationflags=0x08000000)
            messagebox.showinfo("Success", "Apps removed.")
            self.refresh_app_status(silent=True)

    def execute_reinstall(self):
        selected = [app for app, var in self.checkbox_vars.items() if var.get()]
        if not selected: return
        if messagebox.askyesno("Confirm", f"Restore {len(selected)} apps?"):
            for app in selected:
                ps_cmd = f"Get-AppxPackage -allusers *{app}* | foreach {{Add-AppxPackage -register \"$($_.InstallLocation)\\appxmanifest.xml\" -DisableDevelopmentMode}}"
                subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, creationflags=0x08000000)
            messagebox.showinfo("Success", "Apps restored.")
            self.refresh_app_status(silent=True)

    def execute_privacy(self):
        if messagebox.askyesno("Privacy Fix", "Disable Telemetry?"):
            try:
                subprocess.run(["powershell", "-Command", "Stop-Service -Name DiagTrack; Set-Service -Name DiagTrack -StartupType Disabled"], 
                               capture_output=True, creationflags=0x08000000)
                reg_cmd = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 0'
                subprocess.run(["powershell", "-Command", reg_cmd], capture_output=True, creationflags=0x08000000)
                messagebox.showinfo("Privacy", "Telemetry disabled.")
                self.check_privacy_status() # Update realtime status
            except:
                messagebox.showerror("Error", "Access Denied.")

    def undo_privacy(self):
        if messagebox.askyesno("Undo Privacy", "Restore defaults?"):
            try:
                subprocess.run(["powershell", "-Command", "Set-Service -Name DiagTrack -StartupType Automatic; Start-Service -Name DiagTrack"], 
                               capture_output=True, creationflags=0x08000000)
                reg_cmd = 'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 1'
                subprocess.run(["powershell", "-Command", reg_cmd], capture_output=True, creationflags=0x08000000)
                messagebox.showinfo("Privacy", "Restored to default.")
                self.check_privacy_status() # Update realtime status
            except:
                messagebox.showerror("Error", "Failed to restore.")

if __name__ == "__main__":
    app = LemonPyHubDebloat()
    app.mainloop()