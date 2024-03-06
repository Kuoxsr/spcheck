from objects.custom_path import Path
from spcheck import get_orphaned_files


# TODO: parametrize this test
def test_get_orphaned_files_should_return_list_when_files_are_not_linked_by_json():

    file1: Path = Path("/test/path/to/file.ogg")
    events: dict[str, list[Path]] = {"test.sound.event": []}
    ogg_files: list[Path] = [file1]

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 1
    assert result[0] == Path(file1)


def test_get_orphaned_files_should_return_alphabetized_list_when_multiple_files_are_not_linked_by_json():

    file1: Path = Path("/test/path/to/volatile.ogg")
    file2: Path = Path("/test/path/to/absinthe.ogg")
    file3: Path = Path("/test/path/to/file.ogg")
    events: dict[str, list[Path]] = {"test.sound.event": []}
    ogg_files: list[Path] = [file1, file2, file3]

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 3
    assert result[0] == file2
    assert result[1] == file3
    assert result[2] == file1


def test_get_orphaned_files_should_return_empty_list_when_everything_linked_correctly():

    file1: Path = Path("/test/path/to/file.ogg")
    events: dict[str, list[Path]] = {"test.sound.event": [file1]}
    ogg_files: list[Path] = [file1]

    result = get_orphaned_files(events, ogg_files)

    assert len(result) == 0


def test_get_orphaned_files_should_return_empty_list_when_file_is_referenced_by_a_symlink():

    path1: Path = Path("/path/to/file.ogg")
    path1.is_symbolic_link = True
    path1.target_path = Path("/actual/path/to/linked/cow.ambient/file01.ogg")
    ogg_files: list[Path] = [path1]

    events: dict[str, list[Path]] = {"test.sound.event": [path1]}

    result = get_orphaned_files(events, ogg_files)
    assert len(result) == 0


def test_get_orphaned_files_should_not_return_broken_links_as_orphans():
    """
    A symlink that doesn't point to anything shouldn't be counted
    as an orphan, because after the zip process, it won't exist
    in the package.
    """

    path1: Path = Path("/path/to/file.ogg")
    path1.is_symbolic_link = True
    path1.target_path = Path("/actual/path/to/linked/cow.ambient/file01.ogg")
    ogg_files: list[Path] = [path1]

    events: dict[str, list[Path]] = {"test.sound.event": [path1]}

    result = get_orphaned_files(events, ogg_files)
    assert len(result) == 0

