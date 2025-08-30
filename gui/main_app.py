import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Type
import tkinter.font as tkfont
from hospital_management_system.gui.frames import *
from hospital_management_system.gui.dialogs.login_dialog import LoginDialog
from hospital_management_system.auth.rbac import AuthenticationManager, UserRole, Permission

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Serenity Health Hospital Management System")
        self.geometry("1200x700")
        
        # Configure styles
        self._configure_styles()
        
        # Initialize authentication
        self.auth_manager = AuthenticationManager()
        
        # Show login dialog
        if not self.show_login():
            self.destroy()
            return
            
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create header
        self._create_header()
        
        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frames
        self.frames: Dict[str, ttk.Frame] = {}
        
        # Register frames
        self._register_frames()
        
        # Show default frame based on role
        self.show_default_frame()

    def _configure_styles(self):
        # Configure fonts
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        
        # Configure styles
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Helvetica", 24, "bold"))
        style.configure("Navigation.TButton", font=("Helvetica", 12))
        style.configure("Content.TFrame", background="#ffffff")
        style.configure("Card.TFrame", background="#f0f0f0")

    def _create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Hospital name
        title = ttk.Label(
            header_frame, 
            text="Serenity Health HMS", 
            style="Header.TLabel"
        )
        title.pack(side="left", padx=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side="right", padx=10)
        
        nav_buttons = [
            ("Dashboard", "Dashboard"),
            ("Patients", "PatientList"),
            ("Doctors", "DoctorList"),
            ("Appointments", "AppointmentList"),
            ("Records", "MedicalRecordList")
        ]
        
        for text, frame in nav_buttons:
            btn = ttk.Button(
                nav_frame,
                text=text,
                style="Navigation.TButton",
                command=lambda f=frame: self.show_frame(f)
            )
            btn.pack(side="left", padx=5)

    def _register_frames(self):
        # Import and register all frames
        frame_classes = {
            "Dashboard": DashboardFrame,
            "PatientList": PatientListFrame,
            "PatientDetails": PatientDetailsFrame,
            "DoctorList": DoctorListFrame,
            "DoctorDetails": DoctorDetailsFrame,
            "AppointmentList": AppointmentListFrame,
            "AppointmentDetails": AppointmentDetailsFrame,
            "MedicalRecordList": MedicalRecordListFrame,
            "MedicalRecordDetails": MedicalRecordDetailsFrame
        }
        
        for name, frame_class in frame_classes.items():
            frame = frame_class(self.main_container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_name: str):
        """Raise the frame to the top"""
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            frame.on_show()  # Call on_show when frame is displayed
    
    def show_login(self) -> bool:
        """Show login dialog and return True if login successful"""
        dialog = LoginDialog(self)
        return dialog.result
    
    def show_default_frame(self):
        """Show the default frame based on user role"""
        user = self.auth_manager.get_current_user()
        if user.role == UserRole.PATIENT:
            self.show_frame("AppointmentList")
        elif user.role == UserRole.DOCTOR:
            self.show_frame("MedicalRecordList")
        else:
            self.show_frame("Dashboard")
    
    def _create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Hospital name
        title = ttk.Label(
            header_frame, 
            text="Serenity Health HMS", 
            style="Header.TLabel"
        )
        title.pack(side="left", padx=10)
        
        # Navigation buttons based on role
        nav_frame = ttk.Frame(header_frame)
        nav_frame.pack(side="right", padx=10)
        
        user = self.auth_manager.get_current_user()
        nav_buttons = self._get_nav_buttons_for_role(user.role)
        
        for text, frame in nav_buttons:
            btn = ttk.Button(
                nav_frame,
                text=text,
                style="Navigation.TButton",
                command=lambda f=frame: self.show_frame(f)
            )
            btn.pack(side="left", padx=5)
        
        # Logout button
        ttk.Button(
            nav_frame,
            text="Logout",
            style="Navigation.TButton",
            command=self.logout
        ).pack(side="left", padx=5)
        
        # User info
        user_label = ttk.Label(
            header_frame,
            text=f"Logged in as: {user.username} ({user.role.value})"
        )
        user_label.pack(side="right", padx=10)
    
    def _get_nav_buttons_for_role(self, role: UserRole) -> list:
        """Get navigation buttons based on user role"""
        if role == UserRole.PATIENT:
            return [
                ("My Appointments", "AppointmentList"),
                ("My Records", "MedicalRecordList")
            ]
        elif role == UserRole.DOCTOR:
            return [
                ("Appointments", "AppointmentList"),
                ("Medical Records", "MedicalRecordList"),
                ("Patients", "PatientList")
            ]
        else:  # STAFF_ADMIN
            return [
                ("Dashboard", "Dashboard"),
                ("Patients", "PatientList"),
                ("Doctors", "DoctorList"),
                ("Appointments", "AppointmentList"),
                ("Records", "MedicalRecordList")
            ]
    
    def logout(self):
        """Logout the current user"""
        self.auth_manager.logout()
        self.destroy()
        new_app = MainApplication()
        new_app.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
