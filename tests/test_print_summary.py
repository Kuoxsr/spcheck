from objects.custom_path import Path
from spcheck import print_summary


def test_print_summary_should_indicate_empty_list_when_no_events_to_report(capsys):

    events: dict[str, list[Path]] = {}
    print_summary(events)
    capture = capsys.readouterr()

    bar = "-" * 56
    assert capture.out == (f"\033[32m\n{bar}\nSound count:\n"
                           f"\n\nTotal sounds: 0\n{bar}\033[0m\n")


def test_print_summary_should_sort_event_names_alphabetically(capsys, fs):

    file1: Path = Path("/path/file01")
    file2: Path = Path("/path/file02")
    file3: Path = Path("/path/file03")
    file4: Path = Path("/path/file04")
    file5: Path = Path("/path/file05")
    file6: Path = Path("/path/file06")

    fs.create_file(file1)
    fs.create_file(file2)
    fs.create_file(file3)
    fs.create_file(file4)
    fs.create_file(file5)
    fs.create_file(file6)

    events: dict[str, list[Path]] = {
        "test03.event.name": [file6],
        "test02.event.name": [file4, file5],
        "test01.event.name": [file1, file2, file3]
    }

    print_summary(events)
    capture = capsys.readouterr()

    bar = "-" * 56
    assert capture.out == (f"\033[32m\n{bar}\nSound count:\n"
                           f"\ntest01.event.name -> 3"
                           f"\ntest02.event.name -> 2"
                           f"\ntest03.event.name -> 1"
                           f"\n\nTotal sounds: 6\n{bar}\033[0m\n")
