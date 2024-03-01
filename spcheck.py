#!/usr/bin/env python3

"""
Problem: Validate a Minecraft Sound Resource pack
Target Users: Me
Target System: GNU/Linux
Interface: Command-line
Functional Requirements: Print out a list of potential errors.
invalid file names, broken links, orphaned files, non-ogg files
Notes:

Command-line arguments:

    --help      (-h)    Show usage
    --version   (-v)    Show version number
"""

__version__ = '2.18'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import json
import os
import re
import sys

from pathlib import Path


# ------------------------------------------------------
# Function definitions
# ------------------------------------------------------


def handle_command_line():
    """
    Handle arguments supplied by the user
    """

    parser = argparse.ArgumentParser(
        prog="Sound Pack Checker",
        description=("generates lists of invalid connections "
                     "between json and sound files."))

    parser.add_argument(
            "-v",
            "--version",
            action="version", 
            version="%(prog)s version " + __version__)

    parser.add_argument(
        "remainder",
        action="store",
        nargs=argparse.REMAINDER,
        help=("Path to the sounds.json file you want to check.  "
              "The file name itself is not required."))

    args = parser.parse_args()

    args.path = get_real_path(args.remainder)

    return args


def get_real_path(args_path: list[str]) -> Path:

    # if path has been specified, use it, otherwise assume cwd
    path: Path = Path(args_path[0] if (len(args_path) > 0) else "")

    # Does the path refer only to a folder?  Assume sounds.json
    if path.is_dir():
        path = path / "sounds.json"

    # Has the user specified the wrong file extension?
    if path.suffix != ".json":
        raise ValueError(f"specified file: {path} is not a JSON file")

    # Does path folder exist on the file system?
    if not path.exists():
        raise FileNotFoundError(f"Specified path not found. "
                                f"{path} is not a valid filesystem path.")

    return Path(path).resolve()


def get_event_dictionary(path: Path) -> dict[str, list[Path]]:

    with open(path, "r") as read_file:
        json_data: dict = dict(json.load(read_file))

    events: dict[str, list] = {}

    for event in json_data.items():

        sound_paths: list[Path] = []
        for sound in event[1]['sounds']:
            sound_paths.append(get_sound_path(path, sound))

        events[event[0]] = sound_paths

    return events


def get_sound_path(path: Path, sound: str) -> Path:

    sound_path: str = ""

    if isinstance(sound, str):
        sound_path = sound

    elif isinstance(sound, dict):
        sound_path = sound['name']

    else:
        sys.exit(f"\nI have no idea how to process this: {sound}\n")

    namespace: str = "minecraft"

    if ":" in sound_path:
        parts = sound_path.split(":")
        namespace = Path(parts[0])
        sound_path = Path(parts[1])

    new_path: str = str(sound_path) + ".ogg"
    temp = path.parent.parent / namespace / "sounds" / new_path
    return temp


def get_invalid_file_names(events: dict[str, list[Path]]) -> list[Path]:

    bad_names: list[Path] = []
    pattern = re.compile("^[a-z0-9/._-]+$")

    for value in events.values():

        for sound in value:

            # Check for "invalid" characters
            if not pattern.match(str(sound)):
                bad_names.append(sound)

    return bad_names


def get_broken_links(
        events: dict[str, list[Path]],
        vanilla_events: dict[str, list[Path]]) -> list[Path]:

    vanilla_sounds: list[Path] = []
    broken_links: list[Path] = []
    for event, sounds in events.items():

        if event in vanilla_events.keys():
            vanilla_sounds = vanilla_events[event]

        bad_paths = list(p for p in sounds if not p.exists())

        for pth in bad_paths:

            if pth.is_symlink():
                broken_links.append(pth)
                continue

            if vanilla_sounds:
                if pth.name not in list(v.name for v in vanilla_sounds):
                    broken_links.append(pth)

    return broken_links


def get_orphaned_files(
           events: dict[str, list[Path]], 
           ogg_files: list[Path]) -> list[Path]:

    orphaned_files: list[Path] = []

    sounds: list[Path] = []
    for sound in events.values():
        sounds.extend(sound)

    links: list[Path] = list(
        set([lnk.resolve() for lnk in ogg_files if lnk.is_symlink()]))

    orphans: list[Path] = [
        o for o in ogg_files if o not in sounds and o not in links]

    if len(orphans) > 0:
        orphaned_files.extend(orphans)

    return orphaned_files


def get_alien_files(path: Path) -> list[Path]:
    """
    Generates a list of files under the specified path 
    that are not .ogg files
    :param path: The path from which to begin the search
    :return: A list of paths to files that shouldn't be 
    in this folder structure
    """
    all = path.glob('**/*')
    alien_files: list[Path] = [
        f for f in all if f.is_file() and f.suffix not in (".ogg", ".json")]

    return sorted(alien_files)


def print_warnings(message: str, files: list[Path], assets_folder: Path):

    if len(files) == 0:
        return

    red = "\033[31m"
    default = "\033[0m"

    print(f"{red}\n{message}{default}")
    temp = [print(f" .../{f.relative_to(assets_folder)}") for f in files]


def print_summary(events):

    green = "\033[32m"
    default = "\033[0m"

    # Sound count / summary
    bar = "-" * 56
    print(f"{green}\n{bar}\nSound count:\n")
    count: int = 0

    for key in events:
        paths = [
            pth for pth in events[key] if not pth.is_symlink() and pth.exists()
        ]
        links = list(set([
            lnk.resolve() for lnk in events[key]
            if lnk.is_symlink() and lnk.resolve().exists()
        ]))
        paths.extend(links)

        c = len(paths)

        if c > 0:
            print(f"{key} -> {c}")
            count += c

    print(f"\nTotal sounds: {count}\n{bar}{default}")


# Main -------------------------------------------------
def main():
    """
    Main program loop
    This function generates lists of invalid connections 
    between json and sound files
    """
    yellow = "\033[33m"
    white = "\033[97m"
    bold = "\033[1m"
    default = "\033[0m"

    # Platform independent clearing of screen
    os.system('cls||clear')

    args = handle_command_line()

    print(f"{bold}{white}Scanning file:\n{default}{yellow}{args.path}")

    # All sound event records in sounds.json
    events: dict[str, list] = get_event_dictionary(args.path)

    # The "trunk" of our tree
    assets_folder: Path = args.path.parent.parent

    # All ogg files in folder structure
    ogg_files: list[Path] = list(assets_folder.rglob("*.ogg"))

    # All sound event records in the vanilla game
    script_home_path: Path = Path(__file__).absolute().resolve().parent
    vanilla_events = get_event_dictionary(
        script_home_path / Path("vanilla-sounds.json"))

    # Collect all the bad files/records
    invalid_file_names: list = get_invalid_file_names(events)
    broken_links: list[Path] = get_broken_links(events, vanilla_events)
    orphaned_files: list[Path] = get_orphaned_files(events, ogg_files)
    alien_files: list[Path] = get_alien_files(assets_folder)

    # Print all the warnings to the user
    print_warnings(
        "The following file names violate"
        "Mojang's naming constraints:",
        invalid_file_names,
        assets_folder)

    print_warnings(
        "The following paths exist in JSON, "
        "but do not correspond to actual file system files:",
        broken_links,
        assets_folder)

    print_warnings(
        "The following .ogg files exist, "
        "but no JSON record refers to them: ",
        orphaned_files,
        assets_folder)

    print_warnings(
        "The following files are not .ogg files, "
        "but are in the sound folders anyway:",
        alien_files,
        assets_folder)

    print_summary(events)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
