app_name = "advanced_attendance"
app_title = "Advanced Attendance"
app_publisher = "eng.khalidselim"
app_description = "Advanced Attendance Management - Allows multiple attendance records for same employee on same day when overlap or additional attendance is enabled"
app_email = "khalidselim05@gmail.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext", "hrms"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/advanced_attendance/css/advanced_attendance.css"
# app_include_js = "/assets/advanced_attendance/js/advanced_attendance.js"

# include js, css files in header of web template
# web_include_css = "/assets/advanced_attendance/css/advanced_attendance.css"
# web_include_js = "/assets/advanced_attendance/js/advanced_attendance.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "advanced_attendance/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Attendance": "public/js/attendance.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "advanced_attendance/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "advanced_attendance.utils.jinja_methods",
# 	"filters": "advanced_attendance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "advanced_attendance.install.before_install"
after_install = "advanced_attendance.install.after_install"
after_migrate = "advanced_attendance.install.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "advanced_attendance.uninstall.before_uninstall"
# after_uninstall = "advanced_attendance.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "advanced_attendance.utils.before_app_install"
# after_app_install = "advanced_attendance.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "advanced_attendance.utils.before_app_uninstall"
# after_app_uninstall = "advanced_attendance.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "advanced_attendance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Attendance": "advanced_attendance.overrides.attendance.CustomAttendance"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Salary Structure Assignment": {
        "validate": "advanced_attendance.overrides.salary_structure_assignment.calculate_base_from_settings"
    }
}

# Fixtures for custom fields
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["dt", "in", ["Salary Structure Assignment"]]
        ]
    }
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"advanced_attendance.tasks.all"
# 	],
# 	"daily": [
# 		"advanced_attendance.tasks.daily"
# 	],
# 	"hourly": [
# 		"advanced_attendance.tasks.hourly"
# 	],
# 	"weekly": [
# 		"advanced_attendance.tasks.weekly"
# 	],
# 	"monthly": [
# 		"advanced_attendance.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "advanced_attendance.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "advanced_attendance.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "advanced_attendance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["advanced_attendance.utils.before_request"]
# after_request = ["advanced_attendance.utils.after_request"]

# Job Events
# ----------
# before_job = ["advanced_attendance.utils.before_job"]
# after_job = ["advanced_attendance.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"advanced_attendance.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
