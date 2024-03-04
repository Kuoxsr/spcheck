import pytest

from spcheck import get_real_path


def test_get_real_path_should_add_sounds_json_when_only_a_folder_specified(fs):

    file = fs.create_file("/test/folder/only/sounds.json")
    result = get_real_path(["/test/folder/only"])
    assert str(result) == file.path


def test_get_real_path_should_raise_exception_when_path_is_not_a_json_file(fs):

    file = fs.create_file("/test/folder/sounds.txt")

    with pytest.raises(ValueError) as result:
        get_real_path([file.path])

    assert result.value.args[0] == f"specified file: {file.path} is not a JSON file"


def test_get_real_path_should_raise_exception_when_path_does_not_exist(fs):

    fs.create_file("/this/is/a/real/path/sounds.json")
    invalid = "/not/a/real/path/sounds.json"

    with pytest.raises(FileNotFoundError) as result:
        get_real_path([invalid])

    assert result.value.args[0] == (f"Specified path not found. "
                                    f"{invalid} is not a valid filesystem path.")

