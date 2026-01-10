# Advanced Attendance

Advanced Attendance Management for Frappe/ERPNext

## Features

- Allows multiple attendance records for the same employee on the same day and project when:
  - **Overlap** checkbox is enabled (`custom_overlap`)
  - **Additional Attendance** checkbox is enabled (`custom_additional_attendance`)

## Installation

```bash
bench get-app https://github.com/eng-khalidselim/advanced_attendance
bench --site your-site.local install-app advanced_attendance
```

## Usage

1. Go to Attendance doctype
2. Check either "Overlap" or "Additional Attendance" checkbox
3. You can now create multiple attendance records for the same employee on the same day

## License

MIT
