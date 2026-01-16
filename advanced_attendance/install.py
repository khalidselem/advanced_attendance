# Copyright (c) 2026, eng.khalidselim and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def after_install():
    """Run after app installation to ensure all DocTypes are synced"""
    sync_salary_base_calculation_settings()

def after_migrate():
    """Run after bench migrate to ensure DocTypes are in sync"""
    sync_salary_base_calculation_settings()

def sync_salary_base_calculation_settings():
    """
    Ensure Salary Base Calculation Settings DocType exists in the database.
    This handles cases where the DocType was created but not properly synced.
    """
    doctype_name = "Salary Base Calculation Settings"
    
    # Check if DocType exists
    if not frappe.db.exists("DocType", doctype_name):
        # Force sync the DocType from JSON
        try:
            from frappe.modules.import_file import import_file_by_path
            import os
            
            # Get the path to the DocType JSON
            app_path = frappe.get_app_path("advanced_attendance")
            json_path = os.path.join(
                app_path,
                "advanced_attendance",
                "doctype",
                "salary_base_calculation_settings",
                "salary_base_calculation_settings.json"
            )
            
            if os.path.exists(json_path):
                import_file_by_path(json_path, force=True)
                frappe.db.commit()
                print(f"✓ DocType '{doctype_name}' synced successfully")
            else:
                print(f"✗ DocType JSON not found at: {json_path}")
        except Exception as e:
            print(f"✗ Error syncing DocType: {e}")
    else:
        # DocType exists, check if module is correct
        current_module = frappe.db.get_value("DocType", doctype_name, "module")
        if current_module != "Advanced Attendance":
            frappe.db.set_value("DocType", doctype_name, "module", "Advanced Attendance")
            frappe.db.commit()
            print(f"✓ Updated module for '{doctype_name}' to 'Advanced Attendance'")
