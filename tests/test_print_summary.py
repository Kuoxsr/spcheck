from objects.custom_path import Path
from spcheck import print_summary


def test_print_summary_should_return_empty_list_when_no_events_to_report(capsys):

    events: dict[str, list[Path]] = {}
    ogg_files: list[Path] = []
    print_summary(events, ogg_files)
    capture = capsys.readouterr()

    bar = "-" * 56
    assert capture.out == (f"\033[32m\n{bar}\nSound count:\n"
                           f"\n\nTotal sounds: 0\n{bar}\033[0m\n")


def test_print_summary_should_return_list_when_there_are_events_to_report(capsys):

    file1: Path = Path("/path/file01.ogg")

    file2: Path = Path("/path/file02.ogg")
    file2.is_symbolic_link = True
    file2.target_path = Path("/alternate/path/to/file02.ogg")

    file3: Path = Path("/path/file03.ogg")

    file4: Path = Path("/path/file04.ogg")

    file5: Path = Path("/path/file05.ogg")
    file5.is_symbolic_link = True
    file5.target_path = Path("/another/different/path/this/time/to/file05.ogg")

    file6: Path = Path("/path/file06.ogg")

    ogg_files = [file1, file2, file3, file4, file5, file6]

    events: dict[str, list[Path]] = {
        "test03.event.name": [file6],
        "test02.event.name": [file4, file5],
        "test01.event.name": [file1, file2, file3]
    }

    print_summary(events, ogg_files)
    capture = capsys.readouterr()

    bar = "-" * 56
    assert capture.out == (f"\033[32m\n{bar}\nSound count:\n"
                           f"\ntest01.event.name -> 3"
                           f"\ntest02.event.name -> 2"
                           f"\ntest03.event.name -> 1"
                           f"\n\nTotal sounds: 6\n{bar}\033[0m\n")


def test_print_summary_should_sort_event_names_alphabetically(capsys, fs):

    file1: Path = Path("/path/file01.ogg")
    file2: Path = Path("/path/file02.ogg")
    file3: Path = Path("/path/file03.ogg")
    file4: Path = Path("/path/file04.ogg")
    file5: Path = Path("/path/file05.ogg")
    file6: Path = Path("/path/file06.ogg")

    ogg_files = [file1, file2, file3, file4, file5, file6]

    events: dict[str, list[Path]] = {
        "test03.event.name": [file6],
        "test02.event.name": [file4, file5],
        "test01.event.name": [file1, file2, file3]
    }

    print_summary(events, ogg_files)
    capture = capsys.readouterr()

    bar = "-" * 56
    assert capture.out == (f"\033[32m\n{bar}\nSound count:\n"
                           f"\ntest01.event.name -> 3"
                           f"\ntest02.event.name -> 2"
                           f"\ntest03.event.name -> 1"
                           f"\n\nTotal sounds: 6\n{bar}\033[0m\n")
