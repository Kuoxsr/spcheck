from objects.custom_path import Path
from spcheck import get_irrelevant_files


def test_get_irrelevant_files_should_return_list_when_files_are_irrelevant():

    file1: Path = Path("/test/path/to/irrelevant/file.txt")
    file2: Path = Path("/test/path/this/is/a/relevant/file.ogg")
    file3: Path = Path("/test/path/another/irrelevant/file/.directory")

    all_files: list[Path] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 2
    assert file1 in result
    assert file3 in result


def test_get_irrelevant_files_should_return_empty_list_when_files_are_relevant():

    file1: Path = Path("/relevant/file/in/a/different/path.ogg")
    file2: Path = Path("/test/path/this/is/a/relevant/file.ogg")
    file3: Path = Path("/test/path/relevant/file/testplan.ogg")

    all_files: list[Path] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 0


def test_get_irrelevant_files_should_be_sorted_alphabetically():

    file1: Path = Path("/irrelevant/file/in/a/different/path.txt")
    file2: Path = Path("/second/irrelevant_file/file.png")
    file3: Path = Path("/another/irrelevant/file/.directory")

    all_files: list[Path] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 3
    assert result[0] == file3
    assert result[1] == file1
    assert result[2] == file2
