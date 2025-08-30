from enum import Enum
from typing import List, Set, Optional
from functools import wraps

class UserRole(Enum):
    PATIENT = "Patient"
    DOCTOR = "Doctor"
    ADMIN = "Admin"

class Permission(Enum):
    # Appointment permissions
    VIEW_APPOINTMENTS = "view_appointments"
    CREATE_APPOINTMENT = "create_appointment"
    CANCEL_APPOINTMENT = "cancel_appointment"
    RESCHEDULE_APPOINTMENT = "reschedule_appointment"
    
    # Medical record permissions
    VIEW_MEDICAL_RECORDS = "view_medical_records"
    CREATE_MEDICAL_RECORD = "create_medical_record"
    UPDATE_MEDICAL_RECORD = "update_medical_record"
    
    # Patient permissions
    VIEW_PATIENTS = "view_patients"
    CREATE_PATIENT = "create_patient"
    UPDATE_PATIENT = "update_patient"
    DELETE_PATIENT = "delete_patient"
    
    # Doctor permissions
    VIEW_DOCTORS = "view_doctors"
    CREATE_DOCTOR = "create_doctor"
    UPDATE_DOCTOR = "update_doctor"
    DELETE_DOCTOR = "delete_doctor"

# Define role-based permissions
ROLE_PERMISSIONS = {
    UserRole.PATIENT: {
        Permission.VIEW_APPOINTMENTS,
        Permission.CREATE_APPOINTMENT,
        Permission.CANCEL_APPOINTMENT,
        Permission.RESCHEDULE_APPOINTMENT,
        Permission.VIEW_MEDICAL_RECORDS,  # Can only view their own records
    },
    UserRole.DOCTOR: {
        Permission.VIEW_APPOINTMENTS,
        Permission.VIEW_MEDICAL_RECORDS,
        Permission.CREATE_MEDICAL_RECORD,
        Permission.UPDATE_MEDICAL_RECORD,
        Permission.VIEW_PATIENTS,
    },
    UserRole.ADMIN: {
        permission for permission in Permission  # All permissions
    }
}

class User:
    def __init__(self, user_id: str, username: str, role: UserRole, reference_id: Optional[str] = None):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.reference_id = reference_id  # patient_id or doctor_id depending on role
        self._permissions = ROLE_PERMISSIONS[role]
    
    def has_permission(self, permission: Permission) -> bool:
        return permission in self._permissions
    
    def can_access_record(self, record_id: str) -> bool:
        """Check if user can access a specific record"""
        if self.role == UserRole.STAFF_ADMIN:
            return True
        elif self.role == UserRole.DOCTOR:
            # TODO: Check if doctor is assigned to this record
            return True
        elif self.role == UserRole.PATIENT:
            # TODO: Check if record belongs to the patient
            return True
        return False

class AuthenticationManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthenticationManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.current_user: Optional[User] = None
    
    def set_current_user(self, username: str, role: UserRole, reference_id: Optional[str] = None):
        """Set the current authenticated user"""
        # Generate a user ID based on role
        if role == UserRole.ADMIN:
            user_id = f"ADM_{username}"
        elif role == UserRole.DOCTOR:
            user_id = f"DOC_{username}"
        elif role == UserRole.PATIENT:
            user_id = f"PAT_{username}"
            
        self.current_user = User(user_id, username, role, reference_id)
        
    def logout(self):
        """Log out the current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get the currently authenticated user"""
        return self.current_user

def require_permission(permission: Permission):
    """Decorator to check if user has required permission"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_manager = AuthenticationManager()
            user = auth_manager.get_current_user()
            
            if not user:
                raise PermissionError("User not authenticated")
            
            if not user.has_permission(permission):
                raise PermissionError(f"User does not have permission: {permission.value}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_self_or_admin(resource_id_param: str = "patient_id"):
    """Decorator to check if user is accessing their own data or is an admin"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_manager = AuthenticationManager()
            user = auth_manager.get_current_user()
            
            if not user:
                raise PermissionError("User not authenticated")
            
            resource_id = kwargs.get(resource_id_param)
            if user.role != UserRole.ADMIN and user.reference_id != resource_id:
                raise PermissionError("Cannot access other user's data")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
