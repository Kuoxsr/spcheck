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

__version__ = '2.0'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import json
import os
from pathlib import Path
from collections import Counter

# Constants
RED = "\033[31m"
WHITE = "\033[0m"

# ------------------------------------------------------
# Function definitions
# ------------------------------------------------------


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


def get_links(json_data: dict, path: Path):
    file_paths = []

    # Loop through json paths
    for value in json_data.values():

        for sound in value['sounds']:
            sound_path = ""

            if isinstance(sound, str):
                sound_path = sound

            elif isinstance(sound, dict):
                sound_path = sound['name']

            else:
                print(f"I have no idea how to process this: {sound}\n")

            # Append the fully qualified path to the array
            full_path = path.parent / Path("sounds") / Path(sound_path).with_suffix(".ogg")
            file_paths.append(full_path)

    return file_paths


def print_file_counts(args, ogg_files):
    w = '\033[0m'   # white (normal)
    g = '\033[32m'  # green

    # All the folders that contain ogg files
    ogg_folders: list[Path] = list(f.relative_to(args.path.parent).parent for f in ogg_files)

    # Remove my custom folder names - I fear this is hopelessly proprietary
    adjusted_folders = []
    for x in ogg_folders:
        if len(x.parts) < 3:
            adjusted_folders.append(x.parts)
        else:
            adjusted_folders.append(x.parts[0:3] + x.parts[-1:])

    # This is fascinating, but could be misleading, due to category overlap
    #    print("\n\n-------------------------------------------------------")
    #    print("Json link count:\n")
    #    for k in data:
    #        print(k, "->", len(data[k]['sounds']))

    print(g + "\n-------------------------------------------------------")
    print("ogg file count:\n")

    # File counts
    counter: dict[tuple, int] = {}
    for item in sorted(adjusted_folders):
        if item not in counter:
            counter[item] = 0
        counter[item] += 1

    for key in counter:
        print("/".join(key), "->", counter[key])

    print(f"\nTotal Sounds: {len(ogg_folders)}\n" + w)


def print_orphaned_files(args, file_paths, ogg_files):
    orphaned_files: list[Path] = [o for o in ogg_files if o not in file_paths]
    if len(orphaned_files) > 0:
        print(RED + "\nThe following .ogg files exist, but no JSON record refers to them:" + WHITE)
        for orphan in orphaned_files:
            print(f".../{orphan.relative_to(args.path.parent.parent)}")


def print_broken_links(args, file_paths):
    bad_paths = list(p for p in file_paths if not p.exists())
    if len(bad_paths) > 0:
        print(RED + "\nThe following paths exist in JSON, but do not correspond to actual file system files:" + WHITE)
        for bad in bad_paths:
            print(f".../{bad.relative_to(args.path.parent.parent)}")


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates lists of invalid connections between json and sound files
    """

    args = handle_command_line()
    print(f"Scanning file: {args.path}")

    with open(args.path, "r") as read_file:
        data: dict = dict(json.load(read_file))

    # Minecraft Sound events
#    sounds: list = list(data.keys())

    # All file links in json
    file_paths: list[Path] = list(get_links(data, args.path))

    # All ogg files in folder structure
    ogg_files: list[Path] = list(args.path.parent.rglob("*.ogg"))

    print_broken_links(args, file_paths)

    print_orphaned_files(args, file_paths, ogg_files)

    # Show file counts
    print_file_counts(args, ogg_files)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
