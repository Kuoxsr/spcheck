import pytest

from contextlib import nullcontext as does_not_raise
from spcheck import get_real_path


def test_get_real_path_should_add_sounds_json_when_only_a_folder_specified(fs):

    file = fs.create_file("/test/folder/only/sounds.json")
    result = get_real_path(["/test/folder/only"])
    assert str(result) == file.path


@pytest.mark.parametrize(
    "file_path, expectation", [
        ("/test/folder/sounds.txt", pytest.raises(ValueError)),
        ("/test/folder/sounds.json", does_not_raise()),
        ("/test/folder/pack.zip", does_not_raise())
    ]
)
def test_get_real_path_should_raise_exception_when_path_is_not_a_supported_file(fs, file_path, expectation):

    file = fs.create_file(file_path)

    with expectation as result:
        get_real_path([file.path])

    if result is not None:
        assert result.value.args[0] == (
            f"specified file: {file.path} is not a supported file\n"
            f"Supported formats are currently .json and .zip")


def test_get_real_path_should_raise_exception_when_path_does_not_exist(fs):

    fs.create_file("/this/is/a/real/path/sounds.json")
    invalid = "/not/a/real/path/sounds.json"

    with pytest.raises(FileNotFoundError) as result:
        get_real_path([invalid])

    assert result.value.args[0] == (
        f"Specified path not found. "
        f"{invalid} is not a valid filesystem path.")
