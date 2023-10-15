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


# ------------------------------------------------------
# Function definitions
# ------------------------------------------------------


def handle_command_line():
    """
    Handle arguments supplied by the user
    """

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


def get_event_dictionary(path: Path) -> dict[str, list[Path]]:

    with open(path, "r") as read_file:
        json_data: dict = dict(json.load(read_file))

    events: dict[str, list] = {}

    for event in json_data.items():
        # print(f"event -> {type(event)} {event}")
        # print(f"dictionary? -> {type(event[1])} {event[1]}")

        sound_paths: list[Path] = []
        for sound in event[1]['sounds']:
            # print(f"sound -> {sound}")

            sound_path: string = ""

            if isinstance(sound, str):
                sound_path = sound

            elif isinstance(sound, dict):
                sound_path = sound['name']

            else:
                print(f"I have no idea how to process this: {sound}\n")

            full_path = path.parent / Path("sounds") / Path(sound_path).with_suffix(".ogg")
            sound_paths.append(full_path)

        events[event[0]] = sound_paths
        # print(f"\nevent: {event[0]} -> sound_paths: {sound_paths}\n")

    return events


def get_orphaned_files(events: dict[str, list[Path]], ogg_files: list[Path]) -> list[Path]:

    orphaned_files: list[Path] = []
    # print(f"\nevents.values() -> {len(events.values())} {events.values()}\n")

    sounds: list[Path] = []
    for sound in events.values():
        sounds.extend(sound)

    # print(f"\nsounds() -> {len(sounds)} {sounds}")
    # print(f"\nogg_files: {len(ogg_files)} {ogg_files}\n")

    links: list[Path] = list(set([lnk.resolve() for lnk in ogg_files if lnk.is_symlink()]))
    # print(f"\nlinks: {len(links)} {links}\n")

    orphans: list[Path] = [o for o in ogg_files if o not in sounds and o not in links]
    if len(orphans) > 0:
        orphaned_files.extend(orphans)

    return orphaned_files


def get_broken_links(events: dict[str, list[Path]]) -> list[Path]:

    broken_links: list[Path] = []
    for event in events.values():

        bad_path = list(p for p in event if not p.exists())
        if len(bad_path) > 0:
            broken_links.extend(bad_path)

    return broken_links


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates lists of invalid connections between json and sound files
    """

    green = "\033[32m"
    red = "\033[31m"
    white = "\033[0m"

    # Platform independent clearing of screen
    os.system('cls||clear')

    args = handle_command_line()
    print(f"Scanning file: {args.path}")

    events: dict[str, list] = get_event_dictionary(args.path)
    # print("\n===============================")
    # print(f"events: {events}")
    # print("===============================")

    # All ogg files in folder structure
    ogg_files: list[Path] = list(args.path.parent.rglob("*.ogg"))
    # print("\nAll ogg files in folder structure:")
    # temp_ogg_files = [print(e) for e in ogg_files]
    # print()

    assets_folder: Path = args.path.parent.parent

    broken_links: list[Path] = get_broken_links(events)
    if len(broken_links) > 0:
        print(red + "\nThe following paths exist in JSON, but do not correspond to actual file system files:" + white)
        temp = [print(f".../{a.relative_to(assets_folder)}") for a in broken_links]

    orphaned_files: list[Path] = get_orphaned_files(events, ogg_files)
    if len(orphaned_files) > 0:
        print(red + "\nThe following .ogg files exist, but no JSON record refers to them:" + white)
        temp = [print(f".../{b.relative_to(assets_folder)}") for b in orphaned_files]

    print(green + "\n-------------------------------------------------------")
    print("Sound count:\n")

    count: int = 0
    for key in events:

        paths: list[Path] = [pth for pth in events[key] if not pth.is_symlink()]
        links: list[Path] = list(set([lnk.resolve() for lnk in events[key] if lnk.is_symlink()]))
        paths.extend(links)

        c = len(paths)
        print(f"{key} -> {c}")
        count += c

    print(f"\nTotal sounds: {count}")
    print("-------------------------------------------------------" + white)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
