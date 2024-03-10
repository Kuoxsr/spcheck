from objects.custom_path import CPath
from spcheck import get_irrelevant_files


def test_get_irrelevant_files_should_return_list_when_files_are_irrelevant():

    file1: CPath = CPath("/test/path/to/irrelevant/file.txt")
    file2: CPath = CPath("/test/path/this/is/a/relevant/file.ogg")
    file3: CPath = CPath("/test/path/another/irrelevant/file/.directory")

    all_files: list[CPath] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 2
    assert file1 in result
    assert file3 in result


def test_get_irrelevant_files_should_return_empty_list_when_files_are_relevant():

    file1: CPath = CPath("/relevant/file/in/a/different/path.ogg")
    file2: CPath = CPath("/test/path/this/is/a/relevant/file.ogg")
    file3: CPath = CPath("/test/path/relevant/file/testplan.ogg")

    all_files: list[CPath] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 0


def test_get_irrelevant_files_should_be_sorted_alphabetically():

    file1: CPath = CPath("/irrelevant/file/in/a/different/path.txt")
    file2: CPath = CPath("/second/irrelevant_file/file.png")
    file3: CPath = CPath("/another/irrelevant/file/.directory")

    all_files: list[CPath] = [file1, file2, file3]

    result = get_irrelevant_files(all_files)

    assert len(result) == 3
    assert result[0] == file3
    assert result[1] == file1
    assert result[2] == file2
