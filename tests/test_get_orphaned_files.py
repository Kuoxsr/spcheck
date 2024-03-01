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

