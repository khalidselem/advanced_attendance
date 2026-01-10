/**
 * Advanced Attendance - Client-side script for Attendance doctype
 * 
 * This script provides visual feedback and helper functionality
 * for the overlap and additional attendance features.
 */

frappe.ui.form.on('Attendance', {
    refresh: function (frm) {
        // Add visual indicator when overlap or additional attendance is enabled
        advanced_attendance.update_overlap_indicator(frm);

        // Add help text for the custom fields
        if (frm.fields_dict.custom_overlap) {
            frm.fields_dict.custom_overlap.$wrapper.attr('title',
                'Enable to allow creating attendance for overlapping time periods on the same day');
        }

        if (frm.fields_dict.custom_additional_attendance) {
            frm.fields_dict.custom_additional_attendance.$wrapper.attr('title',
                'Enable to create additional attendance record for the same employee on the same day and project');
        }
    },

    custom_overlap: function (frm) {
        advanced_attendance.update_overlap_indicator(frm);
        advanced_attendance.show_overlap_message(frm);
    },

    custom_additional_attendance: function (frm) {
        advanced_attendance.update_overlap_indicator(frm);
        advanced_attendance.show_overlap_message(frm);
    }
});

// Namespace for advanced attendance functions
var advanced_attendance = {
    /**
     * Update the visual indicator based on overlap/additional attendance flags
     */
    update_overlap_indicator: function (frm) {
        // Remove any existing indicator
        frm.page.clear_indicator();

        if (frm.doc.custom_overlap || frm.doc.custom_additional_attendance) {
            // Show indicator that duplicate attendance is allowed
            frm.page.set_indicator(__('Multiple Attendance Allowed'), 'blue');
        }
    },

    /**
     * Show informational message when overlap flags are changed
     */
    show_overlap_message: function (frm) {
        if (frm.doc.custom_overlap || frm.doc.custom_additional_attendance) {
            frappe.show_alert({
                message: __('Multiple attendance records are now allowed for this employee on the same day'),
                indicator: 'blue'
            }, 5);
        }
    },

    /**
     * Helper to check if duplicate attendance exists
     */
    check_duplicate_attendance: function (frm) {
        if (!frm.doc.employee || !frm.doc.attendance_date) {
            return;
        }

        frappe.call({
            method: 'frappe.client.get_count',
            args: {
                doctype: 'Attendance',
                filters: {
                    employee: frm.doc.employee,
                    attendance_date: frm.doc.attendance_date,
                    name: ['!=', frm.doc.name || ''],
                    docstatus: ['!=', 2]
                }
            },
            callback: function (r) {
                if (r.message && r.message > 0) {
                    if (!frm.doc.custom_overlap && !frm.doc.custom_additional_attendance) {
                        frappe.msgprint({
                            title: __('Existing Attendance Found'),
                            message: __('There are {0} existing attendance record(s) for this employee on {1}. Enable "Overlap" or "Additional Attendance" to create another record.',
                                [r.message, frm.doc.attendance_date]),
                            indicator: 'orange'
                        });
                    }
                }
            }
        });
    }
};
