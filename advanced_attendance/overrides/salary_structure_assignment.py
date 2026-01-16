"""
Salary Structure Assignment Override

This module provides doc_events hook for automatic base calculation
using configurable settings without modifying ERPNext core.

Formula: base = gross_pay / gross_divider
With min/max limits applied (SSA values take priority over Settings defaults)
"""

import frappe
from frappe import _
from frappe.utils import flt


def calculate_base_from_settings(doc, method=None):
    """
    Calculate base from gross_pay using Settings configuration.
    
    Called on validate event for Salary Structure Assignment.
    
    Logic:
    1. Check if feature is enabled in Settings
    2. Get gross_pay from document
    3. Calculate: base = gross_pay / gross_divider
    4. Apply min/max limits (SSA fields take priority over Settings defaults)
    
    Works for: UI / API / Data Import
    Compatible with: ERPNext v14 and v15
    
    Args:
        doc: Salary Structure Assignment document
        method: Event method name (unused, required for hook signature)
    """
    # Get settings (use cached single doc)
    try:
        settings = frappe.get_cached_doc("Salary Base Calculation Settings")
    except (frappe.DoesNotExistError, ImportError):
        # Settings not configured yet or DocType module misconfigured - skip calculation
        return
    
    # Check if feature is enabled
    if not settings.get("enable_auto_base"):
        return
    
    # Get gross_pay from document (custom field)
    gross_pay = flt(doc.get("custom_gross_pay"))
    
    # Skip if no gross_pay provided
    if not gross_pay:
        return
    
    # Get divider from settings (default to 1.3 to avoid division by zero)
    gross_divider = flt(settings.get("gross_divider")) or 1.3
    
    # Validate divider is not zero
    if gross_divider == 0:
        frappe.throw(_("Gross Divider cannot be zero in Salary Base Calculation Settings"))
    
    # Calculate base: gross_pay / gross_divider
    calculated_base = flt(gross_pay / gross_divider, 2)
    
    # Get min/max limits with priority:
    # 1. Values from Salary Structure Assignment (if provided)
    # 2. Default values from Settings
    min_base = get_limit_value(
        doc.get("custom_minimum_base_amount"),
        settings.get("default_min_base")
    )
    
    max_base = get_limit_value(
        doc.get("custom_maximum_base_amount"),
        settings.get("default_max_base")
    )
    
    # Apply limits
    final_base = apply_limits(calculated_base, min_base, max_base)
    
    # Set the base amount
    doc.base = final_base


def get_limit_value(ssa_value, settings_value):
    """
    Get the effective limit value with SSA priority.
    
    Args:
        ssa_value: Value from Salary Structure Assignment (priority)
        settings_value: Default value from Settings (fallback)
    
    Returns:
        float: The effective limit value, or 0 if none set
    """
    # SSA value takes priority if provided
    ssa_val = flt(ssa_value)
    if ssa_val > 0:
        return ssa_val
    
    # Fallback to settings default
    return flt(settings_value)


def apply_limits(calculated_base, min_base, max_base):
    """
    Apply min/max limits to the calculated base.
    
    Args:
        calculated_base: The raw calculated base value
        min_base: Minimum allowed base (0 = no minimum)
        max_base: Maximum allowed base (0 = no maximum)
    
    Returns:
        float: The base value after applying limits
    """
    final_base = calculated_base
    
    # Apply minimum limit
    if min_base > 0 and final_base < min_base:
        final_base = min_base
    
    # Apply maximum limit
    if max_base > 0 and final_base > max_base:
        final_base = max_base
    
    return final_base
