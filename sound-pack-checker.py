#!/usr/bin/env python3

# noinspection GrazieInspection
"""
Problem: Validate a Minecraft Sound Resource pack
Target Users: Me
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Print out a list of broken links.
Notes:

Command-line arguments:

    --help      (-h)    Show usage
    --version   (-v)    Show version number
"""

__version__ = '0.1'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import math
import os
import random

# Constants


# ------------------------------------------------------
# Function definitions
# ------------------------------------------------------

# handle_command_line ----------------------------------
def handle_command_line():
    """
    Handle arguments supplied by the user
    """

    parser = argparse.ArgumentParser(
        prog="Sound Pack Checker",
        description="Generate two lists: json lines that don't mach files, and files that don't match the json.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __version__)

    parser.add_argument(
        "path",
        action="store",
        nargs=argparse.REMAINDER,
        help="Path to the sounds.json file you want to check.  The file name itself is not required.")

    args = parser.parse_args()

    # TODO: validate path

#    print("args:",args); exit()
    return args


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates lists of invalid connections between json and sound files
    """

    # Loop through json paths
    #     - Add path to first list if no ogg file in that location

    # Loop through ogg files in folder structure
    #     - Add path to second list if not mentioned in json paths

    # Print output in console


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
