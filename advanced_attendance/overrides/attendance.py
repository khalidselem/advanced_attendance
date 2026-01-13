"""
Custom Attendance Class Override

This module overrides the standard Attendance doctype to allow multiple 
attendance records for the same employee on the same day when:
- custom_overlap checkbox is checked, OR
- custom_additional_attendance checkbox is checked

Business Rules:
1. FIRST attendance for employee+date: Allowed WITHOUT selecting overlap options
2. SECOND+ attendance: MUST select exactly ONE of: Overlap OR Additional Attendance
3. Validation does NOT block workflow state transitions
"""

import frappe
from frappe import _
from frappe.utils import cint

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
    
    Enforces business rules:
    - First record: No overlap option required
    - Second+ records: Must select exactly one overlap option
    - Workflow transitions are never blocked
    """

    def validate(self):
        """Override validate to conditionally skip duplicate check and enforce business rules."""
        # Always run our custom overlap/additional attendance validation first
        # This runs BEFORE any duplicate check to provide clear messaging
        self.validate_overlap_additional_attendance()
        
        # Check if we should skip duplicate validation (for second+ records)
        skip_duplicate_check = self.should_skip_duplicate_check()
        
        if skip_duplicate_check:
            # Run individual validation methods without duplicate check
            self.validate_attendance_date()
            self.set_roster_and_shift()
            self.validate_employee()
            self.validate_working_hours()
            # Skip validate_duplicate_record from parent
        else:
            # Run the standard validation including duplicate check
            super().validate()
    
    def validate_overlap_additional_attendance(self):
        """
        Enforce business rules for overlap/additional attendance fields.
        
        Rules:
        - First attendance for employee+date: No option required
        - Second+ attendance: Must select exactly ONE of Overlap OR Additional Attendance
        - Workflow state changes bypass this validation
        
        Works for: UI / API / Data Import
        Compatible with: ERPNext v14 and v15
        """
        # Skip validation if this is purely a workflow state change
        if self.is_workflow_transition_only():
            return
        
        # Skip if essential fields are not set (incomplete document)
        if not self.employee or not self.attendance_date:
            return
        
        # Build filters to count existing attendance records
        filters = {
            'employee': self.employee,
            'attendance_date': self.attendance_date,
            'docstatus': ['!=', 2]  # Exclude cancelled records
        }
        
        # Exclude current document when editing
        if self.name and not self.is_new():
            filters['name'] = ['!=', self.name]
        
        # Count existing non-cancelled attendance records
        existing_count = frappe.db.count('Attendance', filters=filters)
        
        if existing_count == 0:
            # First record for this employee+date - no validation needed
            # Allow saving without selecting overlap options
            return
        
        # Second or more record - must select exactly ONE option
        overlap = cint(getattr(self, 'custom_overlap', 0))
        additional = cint(getattr(self, 'custom_additional_attendance', 0))
        
        # Check for mutual exclusivity (both selected is invalid)
        if overlap and additional:
            frappe.throw(
                _('Please select <b>ONLY ONE</b> option: either "Overlap" OR "Additional Attendance", not both.'),
                title=_('Invalid Selection')
            )
        
        # Check that at least one is selected for second+ record
        if not overlap and not additional:
            frappe.throw(
                _('An attendance record already exists for this employee on <b>{0}</b>.<br><br>'
                  'To create another attendance record, please select <b>one</b> of the following options:<br>'
                  '• <b>Overlap</b> - for overlapping time periods on the same day<br>'
                  '• <b>Additional Attendance</b> - for an additional record on the same day'
                ).format(frappe.format(self.attendance_date, {'fieldtype': 'Date'})),
                title=_('Attendance Already Exists')
            )
    
    def is_workflow_transition_only(self):
        """
        Check if this save is purely a workflow state transition.
        
        When a workflow transitions state (e.g., Draft → Pending Approval → Approved),
        we should NOT block the save with our validation. This ensures workflow
        approvers can approve/reject without needing to modify overlap fields.
        
        Returns:
            bool: True if only workflow_state changed, False otherwise
        """
        # New documents are never workflow-only transitions
        if self.is_new():
            return False
        
        # Check if document has a workflow applied
        if not self.meta.get_workflow():
            return False
        
        try:
            # Get the previous document state from database
            previous_doc = frappe.get_doc('Attendance', self.name)
            
            # Fields that are relevant to our validation
            # If ANY of these changed, it's not a workflow-only transition
            validation_relevant_fields = [
                'employee',
                'attendance_date', 
                'custom_overlap',
                'custom_additional_attendance'
            ]
            
            for field in validation_relevant_fields:
                current_value = getattr(self, field, None)
                previous_value = getattr(previous_doc, field, None)
                
                # Normalize None and empty values
                if current_value in (None, '', 0):
                    current_value = None
                if previous_value in (None, '', 0):
                    previous_value = None
                    
                if current_value != previous_value:
                    # A validation-relevant field changed - run validation
                    return False
            
            # Only workflow_state (or other non-relevant fields) changed
            return True
            
        except frappe.DoesNotExistError:
            # Document doesn't exist in DB yet (edge case)
            return False
    
    def should_skip_duplicate_check(self):
        """
        Check if we should skip the duplicate attendance check.
        
        Returns True if either:
        - custom_overlap is checked
        - custom_additional_attendance is checked
        
        This bypasses ERPNext's built-in "Attendance for employee {0} on {1} already exists"
        validation when creating legitimate multiple attendance records.
        """
        overlap = cint(getattr(self, 'custom_overlap', 0))
        additional_attendance = cint(getattr(self, 'custom_additional_attendance', 0))
        
        return bool(overlap or additional_attendance)
    
    def validate_attendance_date(self):
        """Validate that attendance date is not in the future."""
        from frappe.utils import getdate, nowdate
        
        if getdate(self.attendance_date) > getdate(nowdate()):
            frappe.throw(_("Attendance can not be marked for future dates"))
    
    def set_roster_and_shift(self):
        """Set roster and shift details if not already set."""
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
        doc.flags.skip_duplicate_check = True
