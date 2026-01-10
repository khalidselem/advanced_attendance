"""
Custom Attendance Class Override

This module overrides the standard Attendance doctype to allow multiple 
attendance records for the same employee on the same day when:
- custom_overlap checkbox is checked, OR
- custom_additional_attendance checkbox is checked
"""

import frappe
from frappe import _

# Try to import from hrms first, fall back to erpnext
try:
    from hrms.hr.doctype.attendance.attendance import Attendance
except ImportError:
    try:
        from erpnext.hr.doctype.attendance.attendance import Attendance
    except ImportError:
        from frappe.model.document import Document as Attendance


class CustomAttendance(Attendance):
    """
    Custom Attendance class that allows duplicate attendance records
    when overlap or additional attendance flags are enabled.
    """

    def validate(self):
        """Override validate to conditionally skip duplicate check."""
        # Check if we should skip duplicate validation
        skip_duplicate_check = self.should_skip_duplicate_check()
        
        if skip_duplicate_check:
            # Temporarily disable duplicate check by running parent validate
            # but intercepting the duplicate validation
            self.validate_attendance_date()
            self.set_roster_and_shift()
            self.validate_employee()
            self.validate_working_hours()
            # Skip validate_duplicate_record
        else:
            # Run the standard validation including duplicate check
            super().validate()
    
    def should_skip_duplicate_check(self):
        """
        Check if we should skip the duplicate attendance check.
        
        Returns True if either:
        - custom_overlap is checked
        - custom_additional_attendance is checked
        """
        # Check for custom_overlap field
        overlap = getattr(self, 'custom_overlap', 0)
        
        # Check for custom_additional_attendance field
        additional_attendance = getattr(self, 'custom_additional_attendance', 0)
        
        return bool(overlap or additional_attendance)
    
    def validate_attendance_date(self):
        """Validate that attendance date is not in the future."""
        from frappe.utils import getdate, nowdate
        
        if getdate(self.attendance_date) > getdate(nowdate()):
            frappe.throw(_("Attendance can not be marked for future dates"))
    
    def set_roster_and_shift(self):
        """Set roster and shift details if not already set."""
        # This is handled by parent class, call it if available
        if hasattr(super(), 'set_roster_and_shift'):
            super().set_roster_and_shift()
    
    def validate_employee(self):
        """Validate that the employee is valid and active."""
        if hasattr(super(), 'validate_employee'):
            super().validate_employee()
    
    def validate_working_hours(self):
        """Validate working hours."""
        if hasattr(super(), 'validate_working_hours'):
            super().validate_working_hours()


def allow_duplicate_attendance(doc, method=None):
    """
    Event hook to check and allow duplicate attendance.
    This can be used as an alternative to class override.
    """
    if doc.get('custom_overlap') or doc.get('custom_additional_attendance'):
        # Mark that duplicate check should be skipped
        doc.flags.skip_duplicate_check = True
