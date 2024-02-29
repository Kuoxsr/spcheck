from pathlib import Path

import pytest

from spcheck import get_broken_links


def test_get_broken_links_should_not_raise_error_when_vanilla_sounds_is_empty():

    events: dict[str, list[Path]] = {"test": [Path("/dummy")]}
    vanilla_events: dict[str, list[Path]] = {}

    try:
        get_broken_links(events, vanilla_events)
    except UnboundLocalError:
        pytest.fail("Unexpected UnboundLocalError...")


def test_get_broken_links_should_return_list_when_links_have_no_file_and_vanilla_sounds_not_specified(fs):

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    path1: Path = Path("/path/to/linked/villager.death/file01.ogg")
    path2: Path = Path("/path/to/unlinked/villager.death/file02.ogg")
    fs.create_file("/path/to/linked/villager.death/file01.ogg")

    path3: Path = Path("/path/to/linked/cow.ambient/file01.ogg")
    path4: Path = Path("/path/to/unlinked/cow.ambient/file02.ogg")
    fs.create_file("/path/to/linked/cow.ambient/file01.ogg")

    events: dict[str, list[Path]] = {
        "entity.villager.death": [path1, path2],
        "entity.cow.ambient": [path3, path4]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events)
    assert len(result) == 2


def test_get_broken_links_should_return_empty_list_when_links_match_files(fs):

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    path1: Path = Path("/path/to/linked/villager.death/file01.ogg")
    fs.create_file("/path/to/linked/villager.death/file01.ogg")

    path3: Path = Path("/path/to/linked/cow.ambient/file01.ogg")
    fs.create_file("/path/to/linked/cow.ambient/file01.ogg")

    events: dict[str, list[Path]] = {
        "entity.villager.death": [path1],
        "entity.cow.ambient": [path3]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events)
    assert len(result) == 0


def test_get_broken_links_should_return_empty_list_when_links_match_symlinked_files(fs):

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    event_path = "/path/to/file.ogg"
    path: Path = Path(event_path)
    actual_file: str = "/actual/path/to/linked/cow.ambient/file01.ogg"
    fs.create_file(actual_file)
    fs.create_symlink(event_path, actual_file)

    events: dict[str, list[Path]] = {"entity.villager.death": [path]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events)
    assert len(result) == 0

