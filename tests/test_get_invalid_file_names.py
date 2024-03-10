from objects.custom_path import CPath
from spcheck import get_invalid_file_names


def test_get_invalid_file_names_should_return_list_when_names_are_invalid():

    path1: CPath = CPath("/this/is/AN/invalid/file")
    path2: CPath = CPath("/this/is/another/bad/f+le")
    path3: CPath = CPath("/this/file_name/should-w0rk.well")
    path4: CPath = CPath("/a/b@d/path/to/file")
    path5: CPath = CPath("/.another/good-path/to_fi1e")

    result = get_invalid_file_names([path1, path2, path3, path4, path5])

    assert len(result) == 3
    assert path1 in result
    assert path2 in result
    assert path4 in result


def test_get_invalid_file_names_should_return_alphabetized_list_when_names_are_invalid():

    path1: CPath = CPath("/this/is/AN/invalid/file")
    path2: CPath = CPath("/this/is/another/bad/f+le")
    path3: CPath = CPath("/this/file_name/should-w0rk.well")
    path4: CPath = CPath("/a/b@d/path/to/file")
    path5: CPath = CPath("/.another/good-path/to_fi1e")

    result = get_invalid_file_names([path1, path2, path3, path4, path5])

    assert len(result) == 3
    assert result[0] == path4
    assert result[1] == path1
    assert result[2] == path2


def test_get_invalid_file_names_should_return_empty_list_when_names_are_valid():

    path1: CPath = CPath(".this/1s/a/v4lid-_-file")
    path2: CPath = CPath("/this/is_another/go0d/file")
    path3: CPath = CPath("/this/file_name/should-w0rk.well")
    path4: CPath = CPath("/a/perfectly/cromulent/path/to/file")
    path5: CPath = CPath("/an9ther/.good-path/to_fi1e")

    result = get_invalid_file_names([path1, path2, path3, path4, path5])

    assert len(result) == 0
