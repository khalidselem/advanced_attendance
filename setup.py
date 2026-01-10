from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in advanced_attendance/__init__.py
from advanced_attendance import __version__ as version

setup(
    name="advanced_attendance",
    version=version,
    description="Advanced Attendance Management - Allows multiple attendance records for same employee on same day when overlap or additional attendance is enabled",
    author="eng.khalidselim",
    author_email="khalidselim05@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    package_data={
        "": ["*.json", "*.js", "*.css", "*.html", "*.md", "*.txt", "*.py"],
    },
)
