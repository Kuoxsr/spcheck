from objects.custom_path import CPath
from spcheck import print_warnings


def test_print_warnings_should_return_without_printing_when_warnings_list_is_empty(capsys):

    message: str = "Test message"
    print_warnings(message, [], CPath())
    captured = capsys.readouterr()

    assert captured.out == ""


def test_print_warnings_should_print_correct_warnings(capsys):

    message: str = "Test message"

    file1 = CPath("assets/minecraft/sounds/bad/file/01.ogg")
    file2 = CPath("assets/minecraft/sounds/bad/file/02.ogg")

    print_warnings(message, [file1, file2], CPath("assets/"))
    captured = capsys.readouterr()

    assert (captured.out == "\033[31m\nTest message\033[0m\n"
                            " .../minecraft/sounds/bad/file/01.ogg\n"
                            " .../minecraft/sounds/bad/file/02.ogg\n")


def test_print_warnings_should_truncate_path_at_assets_folder_or_equivalent(capsys):

    message: str = "Test message"

    file1 = CPath("assets/namespace/sounds/this/is/a/bad/file/01.ogg")
    file2 = CPath("assets/namespace/sounds/this/is/another/bad/file/02.ogg")

    print_warnings(
        message=message,
        files=[file1, file2],
        assets_folder=CPath("assets/"))

    captured = capsys.readouterr()

    assert (captured.out ==
            "\033[31m\nTest message\033[0m\n"
            " .../namespace/sounds/this/is/a/bad/file/01.ogg\n"
            " .../namespace/sounds/this/is/another/bad/file/02.ogg\n")
