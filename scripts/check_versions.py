#!/usr/bin/env python3
from datetime import datetime

########################################################################
# List installed python module versions. Python dependency managemen is
# fragile! It makes life painful often.
# muquit@muquit.com Oct-27-2024 
########################################################################

from importlib.metadata import version

def get_package_name(requirement):
    # strip version specifiers and whitespace
    return requirement.strip().split('==')[0].split('>=')[0].split('<=')[0].strip()

with open('requirements.txt', 'r') as f:
    packages = [get_package_name(line) for line in f if line.strip() and not line.startswith('#')]

for package in packages:
    try:
        pkg_version = version(package)
        print(f"{package}=={pkg_version}")
    except Exception as e:
        print(f"{package} is not installed")

today = datetime.today().strftime("%b-%d-%Y")
print("\n--")
print(f"Updated: {today}")
