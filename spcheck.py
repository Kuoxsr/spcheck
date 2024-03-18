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

__version__ = '3.1.1'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import json
import os
import re
import sys
import zipfile

from tempfile import TemporaryDirectory
from objects.sound_event_handler import SoundEventHandler
from objects.custom_path import CPath


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
        "-n",
        "--no-clear",
        action='store_true',
        help="Don't clear the screen before displaying report.")

    parser.add_argument(
        "remainder",
        action="store",
        nargs=argparse.REMAINDER,
        help=("Path to the sounds.json file you want to check. "
              "The file name itself is not required. "
              "You can also specify a .zip file, and this "
              "application will check the contents in a"
              "temporary directory."))

    args = parser.parse_args()

    args.path = get_real_path(args.remainder)

    return args


def get_real_path(args_path: list[str]) -> CPath:

    # if path has been specified, use it, otherwise assume cwd
    path: CPath = CPath(args_path[0] if (len(args_path) > 0) else "")

    # Does the path refer only to a folder?  Assume sounds.json
    if path.is_dir():
        path = path / "sounds.json"

    # Does the path exist on the file system?
    if not path.exists():
        raise FileNotFoundError(f"Specified path not found. "
                                f"{path} is not a valid filesystem path.")

    # Has the user specified the wrong file extension?
    if path.suffix not in [".json", ".zip"]:
        raise ValueError(
            f"specified file: {path} is not a supported file\n"
            f"Supported formats are currently .json and .zip")

    return CPath(path).resolve()


def get_all_files(assets_folder: CPath):

    files: list[CPath] = (
        list(CPath(f) for f in assets_folder.rglob("*") if f.is_file()))

    return files


def get_irrelevant_files(all_files: list[CPath]) -> list[CPath]:
    """
    Given the list of all files in the target path,
    generate a list of all files that are not relevant
    to the sound pack.
    :param all_files: The list of files to search
    :return: A list of paths to files that shouldn't be
    in this folder structure
    """

    irrelevant_files: list[CPath] = [
        f for f in all_files if f.suffix != ".ogg" and f.suffix != ".json"]

    return sorted(irrelevant_files)  # noqa


def get_orphaned_files(events: SoundEventHandler,
                       ogg_files: list[CPath]) -> list[CPath]:
    """
    Given a list of sound events and a list of ogg files,
    generate a list of files that don't have a matching record
    in the JSON file.
    :param events: A dictionary of sound events
    :param ogg_files: A list of ogg paths
    :return: A list of files that don't have matching JSON
    """
    sounds: list[CPath] = events.get_sound_files()

    links: list[CPath] = list(
        set([k.target_path for k in ogg_files if k.is_symbolic_link]))

    orphans: list[CPath] = [
        o for o in ogg_files if o not in sounds and o not in links]

    orphaned_files: list[CPath] = orphans if len(orphans) > 0 else []

    return sorted(orphaned_files)  # noqa


def get_broken_links(
        events: SoundEventHandler,
        vanilla_events: SoundEventHandler,
        ogg_files: list[CPath]) -> list[CPath]:
    """
    Given a list of JSON sound references and a list of the ogg files in
    the folder structure, generate a list of the JSON references that
    have no corresponding ogg file.
    :param events: A dictionary of sound events
    :param vanilla_events: A list of vanilla sound events
    :param ogg_files: A list of ogg paths
    :return: A list of JSON references that have no matching files
    """

    # Normal files
    file_paths = [p for p in ogg_files if p.is_symbolic_link is False]

    # Symlinks that can be resolved
    file_paths.extend([
        p for p in ogg_files if
        p.is_symbolic_link is True and p.target_path is not None])

    # JSON records that point to vanilla sounds
    file_paths.extend(events.get_sound_files_in(vanilla_events))

    # Based on the 3 categories, above, the following are bad
    events_sounds = events.get_sound_files()
    broken_links = [p for p in events_sounds if p not in file_paths]

    return sorted(broken_links)  # noqa


def get_invalid_file_names(ogg_files: list[CPath]) -> list[CPath]:
    """
    Given a list of paths, generate a list of paths that
    violate Mojang's naming rules.
    :param: ogg_files: A list of paths
    :return: A list of the paths that fail Mojang's naming test
    """

    pattern = re.compile("^[a-z0-9/._-]+$")
    bad_names = [n for n in ogg_files if not pattern.match(str(n))]
    return sorted(bad_names)  # noqa


def print_warnings(message: str, files: list[CPath], assets_folder: CPath):

    if len(files) == 0:
        return

    red = "\033[31m"
    default = "\033[0m"

    print(f"{red}\n{message}{default}")
    [print(f" .../{f.relative_to(assets_folder)}") for f in files]


def print_summary(events: SoundEventHandler, ogg_files: list[CPath]):

    green = "\033[32m"
    default = "\033[0m"

    # Sound count / summary
    bar = "-" * 56
    print(f"{green}\n{bar}\nSound count:\n")
    count: int = 0

    for key in events.get_event_names():

        paths = set(ogg_files).intersection(events.get_sound_files(key))

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

    try:
        args = handle_command_line()
    except FileNotFoundError as e:
        sys.exit(str(e))

    # Platform independent clearing of screen
    if not args.no_clear:
        os.system('cls||clear')

    print(f"{bold}{white}Scanning file:\n{default}{yellow}{args.path}")

    # Handle .zip files
    if args.path.suffix == ".zip":

        # Create temp directory
        zip_dir = TemporaryDirectory(dir="/tmp")

        # Extract contents of zip to temp dir
        file = zipfile.ZipFile(args.path)
        file.extractall(path=zip_dir.name)

        # Set args.path to the location of sounds.json within the temp dir
        sounds_json_paths = list(CPath(zip_dir.name).glob("**/sounds.json"))

        # If it can find sounds.json, retrieve that path for the rest
        # of the processing.
        if len(sounds_json_paths) == 1:
            args.path = sounds_json_paths[0]

    # The "trunk" of our tree
    assets_folder: CPath = args.path.parent.parent

    # All sound event records in sounds.json
    with open(args.path, "r") as file:
        events = SoundEventHandler(assets_folder, json.load(file))

    # All files in the entire folder structure
    all_files: list[CPath] = get_all_files(assets_folder)

    # All sound event records in the vanilla game
    script_home_path: CPath = CPath(__file__).absolute().resolve().parent

    with open(script_home_path / CPath("vanilla-sounds.json"), "r") as file:
        vanilla_events = SoundEventHandler(assets_folder, json.load(file))

    # Collect all the files that don't belong in the pack
    irrelevant_files: list[CPath] = get_irrelevant_files(all_files)

    # Remove the irrelevant files from our list
    ogg_files = [
        f for f in all_files if f.suffix == ".ogg" and f not in irrelevant_files]

    # Collect all the ogg files that have no JSON reference
    orphaned_files: list[CPath] = get_orphaned_files(events, ogg_files)

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in orphaned_files]

    # Collect all the JSON references that have no corresponding ogg file
    broken_links: list[CPath] = (
        get_broken_links(events, vanilla_events, ogg_files))

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in broken_links]

    invalid_file_names: list = get_invalid_file_names(ogg_files)

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in invalid_file_names]

    # Print all the warnings to the user
    print_warnings(
        "The following files are not .ogg files, "
        "but are in the sound folders anyway:",
        irrelevant_files,
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
        "The following file names violate "
        "Mojang's naming constraints:",
        invalid_file_names,
        assets_folder)

    print_summary(events, ogg_files)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
