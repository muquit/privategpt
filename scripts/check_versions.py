#!/usr/bin/env python3

########################################################################
# List installed python module versions. Python dependency managemen is
# fragile! It makes life painful often.
# muquit@muquit.com Oct-27-2024 
########################################################################

from datetime import datetime
from importlib.metadata import version

HEADER = """# Contains exact versions that are known to work together
# Test environment: Python 3.12
#
# If you want to try the latest versions (may introduce compatibility
# issues):
#   1. pip install -r requirements.txt --upgrade
#   2. If it works: Please create an issue with your versions (run:
#     ./scripts/check_versions.py)
#   3. If it breaks: Fall back to pinned versions, do the follwing:
#      deactive
#      rm -rf pvenv
#      python3 -m venv pvenv
#      source pvenv/bin/activate
#      pip install -r requirements_pinned.txt
#
# Generated with: ./scripts/check_versions.py"""

def get_package_name(requirement):
    # strip version specifiers and whitespace
    return requirement.strip().split('==')[0].split('>=')[0].split('<=')[0].strip()

def main():
    # Read existing requirements.txt
    with open('requirements.txt', 'r') as f:
        packages = [get_package_name(line) for line in f if line.strip() and not line.startswith('#')]

    print(HEADER)
    
    # print current versions
    for package in packages:
        try:
            pkg_version = version(package)
            print(f"{package}=={pkg_version}")
        except Exception as e:
            print(f"Warning: {package} is not installed", file=sys.stderr)
            continue

    # Print the date
    today = datetime.today().strftime("%b-%d-%Y")
    print(f"#\n# Last verified: {today}")
    
#    print("\nTo update requirements.txt:", file=sys.stderr)
#    print("1. Review requirements_new.txt", file=sys.stderr)
#    print("2. If everything looks good, run: mv requirements_new.txt requirements.txt", file=sys.stderr)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("Usage: ./check_versions.py > requirements_new.txt")
        sys.exit(0)
    main()
