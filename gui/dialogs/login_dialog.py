import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from ...config import DB_CONFIG
from ...auth.rbac import AuthenticationManager, UserRole

class LoginDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = False
        # Database connection
        self.db = mysql.connector.connect(**DB_CONFIG)
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Login")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        window_width = 300
        window_height = 200
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        self.create_widgets()
        
        # Configure style
        style = ttk.Style()
        style.configure("LoginHeader.TLabel", font=("Helvetica", 16, "bold"))
        
        self.dialog.wait_window()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Label(
            main_frame,
            text="Serenity Health HMS",
            style="LoginHeader.TLabel"
        )
        header.pack(pady=(0, 20))
        
        # Username
        username_frame = ttk.Frame(main_frame)
        username_frame.pack(fill="x", pady=5)
        
        ttk.Label(username_frame, text="Username:").pack(side="left")
        self.username_var = tk.StringVar()
        ttk.Entry(username_frame, textvariable=self.username_var).pack(side="right", expand=True)
        
        # Password
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill="x", pady=5)
        
        ttk.Label(password_frame, text="Password:").pack(side="left")
        self.password_var = tk.StringVar()
        ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*"
        ).pack(side="right", expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="Login",
            command=self.on_login
        ).pack(side="right", padx=5)
        
        ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.on_cancel
        ).pack(side="right")
        
        # Role selection (for demo purposes)
        role_frame = ttk.Frame(main_frame)
        role_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Label(role_frame, text="Login as:").pack(side="left")
        self.role_var = tk.StringVar(value="Patient")
        
        ttk.Radiobutton(
            role_frame,
            text="Patient",
            variable=self.role_var,
            value="Patient"
        ).pack(side="left")
        
        ttk.Radiobutton(
            role_frame,
            text="Doctor",
            variable=self.role_var,
            value="Doctor"
        ).pack(side="left")
        
        ttk.Radiobutton(
            role_frame,
            text="Admin",
            variable=self.role_var,
            value="Admin"
        ).pack(side="left")
    
    def on_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        try:
            cursor = self.db.cursor()
            cursor.execute(
                "SELECT role FROM rbac_auth WHERE username = %s AND password = %s",
                (username, password)
            )
            result = cursor.fetchone()
            
            if result:
                role = result[0]
                auth_manager = AuthenticationManager()
                user_role = UserRole(role)
                auth_manager.set_current_user(username, user_role)
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username or password"
                )
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"Could not authenticate: {err}"
            )
    
    def on_cancel(self):
        self.result = False
        if hasattr(self, 'db') and self.db.is_connected():
            self.db.close()
        self.dialog.destroy()
        
    def __del__(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.db.close()
