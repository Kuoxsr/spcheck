from pathlib import Path

from spcheck import print_warnings


def test_print_warnings_should_return_without_printing_when_warnings_list_is_empty(capsys):

    message: str = "Test message"
    print_warnings(message, [], Path())
    captured = capsys.readouterr()

    assert captured.out == ""


def test_print_warnings_should_print_correct_warnings(capsys):

    message: str = "Test message"

    file1 = Path("/bad/file/01.ogg")
    file2 = Path("/bad/file/02.ogg")

    print_warnings(message, [file1, file2], Path("/bad/"))
    captured = capsys.readouterr()

    assert (captured.out == "\033[31m\nTest message\033[0m\n"
                            " .../file/01.ogg\n"
                            " .../file/02.ogg\n")
