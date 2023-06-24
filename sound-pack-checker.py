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

__version__ = '1.2'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import json
from pathlib import Path
import os

# Constants


# ------------------------------------------------------
# Function definitions
# ------------------------------------------------------

# handle_command_line ----------------------------------
def handle_command_line():
    """
    Handle arguments supplied by the user
    """

    # Platform independent clearing of screen
    os.system('cls||clear')

    parser = argparse.ArgumentParser(
        prog="Sound Pack Checker",
        description="generates lists of invalid connections between json and sound files.")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s version " + __version__)

    parser.add_argument(
        "path",
        action="store",
        nargs=argparse.REMAINDER,
        help="Path to the sounds.json file you want to check.  The file name itself is not required.")

    args = parser.parse_args()

    # path is a LIST at this point, and we want just a string
    if len(args.path) > 0:
        args.path = args.path[0]
    else:
        args.path = ""

    # Has the user specified a path at all?
    if not args.path:
        print("Path to sounds.json is required.")
        exit()

    path = Path(args.path)

    # Does path folder exist on the file system?
    if not path.exists():
        print(f"Specified path not found. {path} is not a valid filesystem path.")
        exit()

    # Has the user specified the wrong file name?
    if path.name != "sounds.json":
        args.path += "sounds.json"

    # Does sounds.json exist, now that we've added it for them (if necessary?)
    if not Path(args.path).exists():
        print("sounds.json not found.")
        exit()

    # Finally, make the argument a Path  (does this work?)
    args.path = Path(args.path)

#    print("args:",args); exit()
    return args


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates lists of invalid connections between json and sound files
    """

    args = handle_command_line()

    with open(args.path, "r") as read_file:
        data = json.load(read_file)

    file_paths = []

    # Loop through json paths
    for value in data.values():

        for sound in value['sounds']:
            sound_path = ""

            if isinstance(sound, str):
                sound_path = sound

            elif isinstance(sound, dict):
                sound_path = sound['name']

            else:
                print(f"I have no idea how to process this: {sound}\n")

            # Append the fully qualified path to the array
            full_path = args.path.parent / Path("sounds") / Path(sound_path).with_suffix(".ogg")
            file_paths.append(full_path)

    # Iterate over our full list of paths
    bad_paths = []
    for p in file_paths:
        if not p.exists():
            bad_paths.append(p)

    print("\nThe following paths exist in JSON, but do not correspond to actual file system files:")
    for bad in bad_paths:
        print(bad)

    # Loop through ogg files in folder structure
    print("\n\nThe following .ogg files exist, but no JSON record refers to them:")
    for i in args.path.parent.rglob("*.ogg"):
        if i not in file_paths:
            print(i)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
