from pathlib import Path

from spcheck import get_irrelevant_files


def test_get_irrelevant_files_should_return_list_when_files_are_irrelevant(fs):

    file1 = "/test/path/to/irrelevant/file.txt"
    file2 = "/test/path/this/is/a/relevant/file.ogg"
    file3 = "/test/path/another/irrelevant/file/.directory"

    fs.create_file(file1)
    fs.create_file(file2)
    fs.create_file(file3)

    all_files: list[Path] = [Path(file1), Path(file2), Path(file3)]

    result = get_irrelevant_files(all_files)

    assert len(result) == 2
    assert Path(file1) in result
    assert Path(file3) in result


def test_get_irrelevant_files_should_return_empty_list_when_files_are_relevant(fs):

    file1 = "/relevant/file/in/a/different/path.ogg"
    file2 = "/test/path/this/is/a/relevant/file.ogg"
    file3 = "/test/path/relevant/file/testplan.ogg"

    fs.create_file(file1)
    fs.create_file(file2)
    fs.create_file(file3)

    all_files: list[Path] = [Path(file1), Path(file2), Path(file3)]

    result = get_irrelevant_files(all_files)

    assert len(result) == 0


def test_get_irrelevant_files_should_be_sorted_alphabetically(fs):

    file1 = "/irrelevant/file/in/a/different/path.txt"
    file2 = "/second/irrelevant_file/file.png"
    file3 = "/another/irrelevant/file/.directory"

    fs.create_file(file1)
    fs.create_file(file2)
    fs.create_file(file3)

    all_files: list[Path] = [Path(file1), Path(file2), Path(file3)]

    result = get_irrelevant_files(all_files)

    assert len(result) == 3
    assert result[0] == Path(file3)
    assert result[1] == Path(file1)
    assert result[2] == Path(file2)
