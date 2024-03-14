from sound_event_handler import SoundEventHandler
from objects.custom_path import CPath
from spcheck import get_orphaned_files


def test_get_orphaned_files_should_return_list_when_files_are_not_linked_by_json():

    file1: CPath = CPath("minecraft/sounds/test/path/to/file.ogg")
    ogg_files: list[CPath] = [file1]

    events = SoundEventHandler(
        root_folder=CPath("/"),
        json_events={"dummy": {"sounds": []}})

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 1
    assert result[0] == CPath(file1)


def test_get_orphaned_files_should_return_alphabetized_list_when_multiple_files_are_not_linked_by_json():

    file1: CPath = CPath("minecraft/sounds/test/path/to/volatile.ogg")
    file2: CPath = CPath("minecraft/sounds/test/path/to/absinthe.ogg")
    file3: CPath = CPath("minecraft/sounds/test/path/to/file.ogg")

    ogg_files: list[CPath] = [file1, file2, file3]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={"dummy": {"sounds": []}})

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 3
    assert result[0] == file2
    assert result[1] == file3
    assert result[2] == file1


def test_get_orphaned_files_should_return_empty_list_when_everything_linked_correctly():

    file1: str = "assets/minecraft/sounds/test/path/to/file.ogg"
    ogg_files: list[CPath] = [CPath(file1)]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={"dummy": {"sounds": [file1]}})

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 0


def test_get_orphaned_files_should_return_empty_list_when_file_is_referenced_by_a_symlink():

    path1: CPath = CPath("assets/minecraft/sounds/path/to/file.ogg")
    path1.is_symbolic_link = True
    path1.target_path = CPath("/actual/path/to/linked/cow.ambient/file01.ogg")
    ogg_files: list[CPath] = [path1]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={"dummy": {"sounds": [str(path1)]}})

    result = get_orphaned_files(events, ogg_files)
    assert len(result) == 0


def test_get_orphaned_files_should_not_return_broken_links_as_orphans():
    """
    A symlink that doesn't point to anything shouldn't be counted
    as an orphan, because after the zip process, it won't exist
    in the package.
    """
    path1: CPath = CPath("assets/minecraft/sounds/path/to/file.ogg")
    path1.is_symbolic_link = True
    path1.target_path = CPath("/actual/path/to/linked/cow.ambient/file01.ogg")
    ogg_files: list[CPath] = [path1]

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={"dummy": {"sounds": [str(path1)]}})

    result = get_orphaned_files(events, ogg_files)
    assert len(result) == 0

