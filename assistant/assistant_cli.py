#!/usr/bin/env python3
import sys
import argparse
from cli_config import CLI_DESCRIPTION, CLI_ARGUMENTS

def create_parser():
    parser = argparse.ArgumentParser(description=CLI_DESCRIPTION)
    for arg in CLI_ARGUMENTS:
        flags = arg.pop("flags")
        parser.add_argument(*flags, **arg)
    return parser

if __name__ == "__main__":
    parser = create_parser()
    
    if len(sys.argv) == 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
        parser.print_help()
        sys.exit(0)
    
    # Parse arguments only if we're not showing help
    args = parser.parse_args()
    
    # Import and run the main application
    from aclim import doit
    doit(args)
