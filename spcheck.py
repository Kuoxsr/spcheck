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

__version__ = '2.28'
__maintainer__ = "kuoxsr@gmail.com"
__status__ = "Prototype"

# Import modules
import argparse
import json
import os
import re
import sys

from objects.custom_path import Path


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

    # Does the path exist on the file system?
    if not path.exists():
        raise FileNotFoundError(f"Specified path not found. "
                                f"{path} is not a valid filesystem path.")

    # Has the user specified the wrong file extension?
    if path.suffix != ".json":
        raise ValueError(f"specified file: {path} is not a JSON file")

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

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    new_path: str = str(sound_path) + ".ogg"
    temp = path.parent.parent / namespace / "sounds" / new_path
    return temp


def get_all_files(assets_folder: Path):

    files: list[Path] = (
        list(Path(f) for f in assets_folder.rglob("*") if f.is_file()))

    return files


def get_irrelevant_files(all_files: list[Path]) -> list[Path]:
    """
    Given the list of all files in the target path,
    generate a list of all files that are not relevant
    to the sound pack.
    :param all_files: The list of files to search
    :return: A list of paths to files that shouldn't be
    in this folder structure
    """

    irrelevant_files: list[Path] = [
        f for f in all_files if f.suffix not in (".ogg", ".json")]

    return sorted(irrelevant_files)  # noqa


def get_orphaned_files(events: dict[str, list[Path]],
                       ogg_files: list[Path]) -> list[Path]:
    """
    Given a list of sound events and a list of ogg files,
    generate a list of files that don't have a matching record
    in the JSON file.
    :param events: A dictionary of sound events
    :param ogg_files: A list of ogg paths
    :return: A list of files that don't have matching JSON
    """

    orphaned_files: list[Path] = []

    sounds: list[Path] = []
    [sounds.extend(s) for s in events.values()]

    links: list[Path] = list(
        set([lnk.target_path for lnk in ogg_files if lnk.is_symbolic_link]))

    orphans: list[Path] = [
        o for o in ogg_files if o not in sounds and o not in links]

    if len(orphans) > 0:
        orphaned_files.extend(orphans)

    return sorted(orphaned_files)  # noqa


def get_broken_links(
        events: dict[str, list[Path]],
        vanilla_events: dict[str, list[Path]],
        ogg_files: list[Path]) -> list[Path]:
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
    keys = [k for k in vanilla_events.keys() if k in events.keys()]
    for k in keys:
        file_paths.extend(vanilla_events[k])

    # Based on the 3 categories, above, the following are bad
    broken_links: list[Path] = []
    for event, sounds in events.items():
        broken_links.extend([p for p in sounds if p not in file_paths])

    return sorted(broken_links)  # noqa


def get_invalid_file_names(ogg_files: list[Path]) -> list[Path]:
    """
    Given a list of paths, generate a list of paths that
    violate Mojang's naming rules.
    :param: ogg_files: A list of paths
    :return: A list of the paths that fail Mojang's naming test
    """

    pattern = re.compile("^[a-z0-9/._-]+$")
    bad_names = [n for n in ogg_files if not pattern.match(str(n))]
    return sorted(bad_names)  # noqa


def print_warnings(message: str, files: list[Path], assets_folder: Path):

    if len(files) == 0:
        return

    red = "\033[31m"
    default = "\033[0m"

    print(f"{red}\n{message}{default}")
    [print(f" .../{f.relative_to(assets_folder)}") for f in files]


def print_summary(events: dict[str, list[Path]], ogg_files: list[Path]):

    green = "\033[32m"
    default = "\033[0m"

    # Sound count / summary
    bar = "-" * 56
    print(f"{green}\n{bar}\nSound count:\n")
    count: int = 0

    events = {k: v for k, v in sorted(events.items(), key=lambda ele: ele[0])}
    for key in events:

        paths = [p for p in events[key] if p in ogg_files]

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

    # All files in the entire folder structure
    all_files: list[Path] = get_all_files(assets_folder)

    # All sound event records in the vanilla game
    script_home_path: Path = Path(__file__).absolute().resolve().parent
    vanilla_events = get_event_dictionary(
        script_home_path / Path("vanilla-sounds.json"))

    # Collect all the files that don't belong in the pack
    irrelevant_files: list[Path] = get_irrelevant_files(all_files)

    # Remove the irrelevant files from our list
    all_files = [f for f in all_files if f not in irrelevant_files]
    ogg_files = [f for f in all_files if f.suffix == ".ogg"]

    # Collect all the ogg files that have no JSON reference
    orphaned_files: list[Path] = get_orphaned_files(events, ogg_files)

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in orphaned_files]

    # Collect all the JSON references that have no corresponding ogg file
    broken_links: list[Path] = (
        get_broken_links(events, vanilla_events, ogg_files))

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in broken_links]

    invalid_file_names: list = get_invalid_file_names(ogg_files)

    # Remove the orphans from our list
    ogg_files = [f for f in ogg_files if f not in invalid_file_names]

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
        irrelevant_files,
        assets_folder)

    print_summary(events, ogg_files)


# ------------------------------------------------------
# Main program loop
# ------------------------------------------------------

# Run main program loop only if not called as a module
if __name__ == "__main__":
    main()
