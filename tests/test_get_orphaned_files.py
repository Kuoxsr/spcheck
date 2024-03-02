from pathlib import Path

from spcheck import get_orphaned_files


# TODO: parametrize this test
def test_get_orphaned_files_should_return_list_when_files_are_not_linked_by_json(fs):

    file1: str = "/test/path/to/file.ogg"
    fs.create_file(file1)
    events: dict[str, list[Path]] = {"test.sound.event": []}
    ogg_files: list[Path] = [Path(file1)]

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 1
    assert result[0] == Path(file1)


def test_get_orphaned_files_should_return_empty_list_when_everything_linked_correctly(fs):

    file1: str = "/test/path/to/file.ogg"
    fs.create_file(file1)
    events: dict[str, list[Path]] = {"test.sound.event": [Path(file1)]}
    ogg_files: list[Path] = [Path(file1)]

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 0


def test_get_orphaned_files_should_return_empty_list_when_file_is_referenced_by_a_symlink(fs):

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    event_path = "/path/to/file.ogg"
    path: Path = Path(event_path)
    actual_file: str = "/actual/path/to/linked/cow.ambient/file01.ogg"
    fs.create_file(actual_file)
    fs.create_symlink(event_path, actual_file)

    events: dict[str, list[Path]] = {"test.sound.event": [path]}

    result = get_orphaned_files(events, [Path(event_path)])
    assert len(result) == 0


def test_get_orphaned_files_should_not_return_broken_links_as_orphans(fs):
    """
    A symlink that doesn't point to anything shouldn't be counted
    as an orphan, because after the zip process, it won't exist
    in the package.
    :param fs: fake filesystem
    :return: None
    """

    # TODO: sound events contain ".ogg" and probably shouldn't
    # ...seems like a hack to include the ".ogg" in the sound events list
    event_path = "/path/to/file.ogg"
    path: Path = Path(event_path)
    link_target: str = "/actual/path/to/linked/cow.ambient/file01.ogg"
    fs.create_symlink(event_path, link_target)

    events: dict[str, list[Path]] = {"test.sound.event": [path]}

    result = get_orphaned_files(events, [Path(event_path)])
    assert len(result) == 0

