import pytest

from objects.custom_path import Path
from spcheck import get_broken_links


def test_get_broken_links_should_not_raise_error_when_vanilla_sounds_is_empty():

    events: dict[str, list[Path]] = {"test": [Path("/dummy")]}
    vanilla_events: dict[str, list[Path]] = {}
    ogg_files: list[Path] = []

    try:
        get_broken_links(events, vanilla_events, ogg_files)
    except UnboundLocalError:
        pytest.fail("Unexpected UnboundLocalError...")


def test_get_broken_links_should_return_list_when_json_does_not_match_files_including_vanilla():

    path1: Path = Path("/path/to/linked/villager.death/file01.ogg")
    path2: Path = Path("/path/to/unlinked/villager.death/file02.ogg")
    path3: Path = Path("/path/to/linked/cow.ambient/file01.ogg")
    path4: Path = Path("/path/to/unlinked/cow.ambient/file02.ogg")

    ogg_files: list[Path] = [Path(path1), Path(path3)]

    events: dict[str, list[Path]] = {
        "entity.villager.death": [path1, path2],
        "entity.cow.ambient": [path3, path4]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 2
    assert result[0] == path2
    assert result[1] == path4


def test_get_broken_links_should_return_empty_list_when_json_matches_vanilla():

    path1: Path = Path("/path/to/linked/villager.death/file01.ogg")
    path2: Path = Path("/path/to/unlinked/villager.death/file02.ogg")
    path3: Path = Path("mob/goat/step1.ogg")
    path4: Path = Path("/path/to/linked/cow.ambient/file01.ogg")
    path5: Path = Path("/path/to/unlinked/cow.ambient/file02.ogg")

    ogg_files: list[Path] = [Path(path1), Path(path4)]

    events: dict[str, list[Path]] = {
        "entity.villager.death": [path1, path2],
        "entity.goat.step": [path3],
        "entity.cow.ambient": [path4, path5]}

    vanilla_events: dict[str, list[Path]] = {"entity.goat.step": [Path("mob/goat/step1.ogg")]}

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 2
    assert result[0] == path2
    assert result[1] == path5


def test_get_broken_links_should_return_empty_list_when_json_matches_files():

    path1: Path = Path("/path/to/linked/villager.death/file01.ogg")
    path3: Path = Path("/path/to/linked/cow.ambient/file01.ogg")

    ogg_files: list[Path] = [Path(path1), Path(path3)]

    events: dict[str, list[Path]] = {
        "entity.villager.death": [path1],
        "entity.cow.ambient": [path3]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 0


def test_get_broken_links_should_return_empty_list_when_links_match_symlinked_files():

    event_path = "/path/to/file.ogg"
    actual_file: str = "/actual/path/to/linked/cow.ambient/file01.ogg"

    fancy_path = Path(event_path)
    fancy_path.target_path = actual_file
    ogg_files: list[Path] = [fancy_path]

    events: dict[str, list[Path]] = {"entity.villager.death": [Path(event_path)]}

    vanilla_events: dict[str, list[Path]] = {"entity.villager.death": [Path("dummy")]}

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 0


def test_get_broken_links_should_return_list_when_json_matches_symlinked_files_that_cannot_be_resolved():

    path: Path = Path("/path/to/file.ogg")
    path.is_symbolic_link = True  # providing this with no target makes this broken

    ogg_files: list[Path] = [path]

    events: dict[str, list[Path]] = {"entity.villager.death": [path]}
    vanilla_events: dict[str, list[Path]] = {}

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 1
    assert result[0] == path
