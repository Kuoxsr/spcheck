import pytest

from objects.sound_event_handler import SoundEventHandler
from objects.custom_path import CPath
from spcheck import get_broken_links


def test_get_broken_links_should_not_raise_error_when_vanilla_sounds_is_empty():

    root_folder = CPath("assets/")
    vanilla_events = SoundEventHandler(root_folder)

    events = SoundEventHandler(
        root_folder=root_folder,
        json_events={"test": {"sounds": ["dummy"]}})

    try:
        get_broken_links(events, vanilla_events, [])
    except UnboundLocalError:
        pytest.fail("Unexpected UnboundLocalError...")


def test_get_broken_links_should_return_list_when_json_does_not_match_files_including_vanilla():

    path1: str = "path/to/linked/villager.death/file01"
    path2: str = "path/to/unlinked/villager.death/file02"
    path3: str = "path/to/linked/cow.ambient/file01"
    path4: str = "path/to/unlinked/cow.ambient/file02"

    ogg_files: list[CPath] = [
        CPath("assets/minecraft/sounds/" + path1 + ".ogg"),
        CPath("assets/minecraft/sounds/" + path3 + ".ogg")]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1, path2]},
            "entity.cow.ambient": {"sounds": [path3, path4]}})

    vanilla_events = SoundEventHandler(
        CPath("assets/"),
        {"entity.villager.death": {"sounds": ["dummy"]}})

    result = get_broken_links(events, vanilla_events, ogg_files)

    assert len(result) == 2

    assert result[0] == CPath(
        "assets/minecraft/sounds/path/to/unlinked/cow.ambient/file02.ogg")

    assert result[1] == CPath(
        "assets/minecraft/sounds/path/to/unlinked/villager.death/file02.ogg")


def test_get_broken_links_should_return_list_when_some_json_does_not_match_some_vanilla():

    path1: str = "path/to/villager.death/file01"
    path2: str = "path/to/bad/villager.death/file02"
    path3: str = "path/to/cow.ambient/file03"
    path4: str = "path/to/cow.ambient/file04"
    path5: str = "path/to/bad/witch.celebrate/file05"
    path6: str = "path/to/witch.celebrate/file06"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1, path2]},
            "entity.cow.ambient": {"sounds": [path3, path4]},
            "entity.witch.celebrate": {"sounds": [path5, path6]}})

    vanilla_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1]},
            "entity.cow.ambient": {"sounds": [path3, path4]},
            "entity.witch.celebrate": {"sounds": [path6]}})

    result = get_broken_links(events, vanilla_events, [])

    assert len(result) == 2

    assert result[0] == CPath(
        "assets/minecraft/sounds/path/to/bad/villager.death/file02.ogg")

    assert result[1] == CPath(
        "assets/minecraft/sounds/path/to/bad/witch.celebrate/file05.ogg")


def test_get_broken_links_should_return_list_that_is_sorted_alphabetically():

    path1: str = "path/to/villager.death/file01"
    path2: str = "path/to/slime.squish/file02"

    vanilla_events = SoundEventHandler(CPath("assets/"))

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1]},
            "entity.slime.squish": {"sounds": [path2]}})

    result = get_broken_links(events, vanilla_events, [])

    assert len(result) == 2

    assert result[0] == CPath(
        "assets/minecraft/sounds/path/to/slime.squish/file02.ogg")

    assert result[1] == CPath(
        "assets/minecraft/sounds/path/to/villager.death/file01.ogg")


def test_get_broken_links_should_return_empty_list_when_json_matches_vanilla():

    path1: str = "path/to/linked/villager.death/file01"
    path2: str = "path/to/unlinked/villager.death/file02"
    path3: str = "mob/goat/step1"
    path4: str = "path/to/linked/cow.ambient/file01"
    path5: str = "path/to/unlinked/cow.ambient/file02"

    ogg_files: list[CPath] = [
        CPath(f"assets/minecraft/sounds/{path1}.ogg"),
        CPath(f"assets/minecraft/sounds/{path4}.ogg")]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1, path2]},
            "entity.goat.step": {"sounds": [path3]},
            "entity.cow.ambient": {"sounds": [path4, path5]}})

    vanilla_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.goat.step": {"sounds": ["mob/goat/step1"]}})

    result = get_broken_links(events, vanilla_events, ogg_files)

    assert len(result) == 2

    assert result[0] == CPath(
        "assets/minecraft/sounds/path/to/unlinked/cow.ambient/file02.ogg")

    assert result[1] == CPath(
        "assets/minecraft/sounds/path/to/unlinked/villager.death/file02.ogg")


def test_get_broken_links_should_return_empty_list_when_json_matches_files():

    path1: str = "path/to/linked/villager.death/file01"
    path3: str = "path/to/linked/cow.ambient/file01"

    ogg_files: list[CPath] = [
        CPath(f"assets/minecraft/sounds/{path1}.ogg"),
        CPath(f"assets/minecraft/sounds/{path3}.ogg")]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [path1]},
            "entity.cow.ambient": {"sounds": [path3]}})

    vanilla_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": ["dummy"]}})

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 0


def test_get_broken_links_should_return_empty_list_when_links_match_symlinked_files():

    event_path: str = "path/to/file"
    actual_file: str = "/actual/path/to/linked/cow.ambient/file01.ogg"

    fancy_path = CPath(f"assets/minecraft/sounds/{event_path}.ogg")
    fancy_path.target_path = actual_file
    ogg_files: list[CPath] = [fancy_path]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": [event_path]}})

    vanilla_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": ["dummy"]}})

    result = get_broken_links(events, vanilla_events, ogg_files)
    assert len(result) == 0


def test_get_broken_links_should_return_list_when_json_matches_symlinked_files_that_cannot_be_resolved():

    # providing this with no target makes this broken
    file: CPath = CPath("path/to/file.ogg")
    file.is_symbolic_link = True
    ogg_files: list[CPath] = [file]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "entity.villager.death": {"sounds": ["path/to/file"]}})

    vanilla_events = SoundEventHandler(CPath("assets/"))

    result = get_broken_links(events, vanilla_events, ogg_files)

    assert len(result) == 1
    assert result[0] == CPath("assets/minecraft/sounds/path/to/file.ogg")
