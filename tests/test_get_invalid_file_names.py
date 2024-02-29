from pathlib import Path

from spcheck import get_invalid_file_names


def test_get_invalid_file_names_should_return_list_when_names_are_invalid():

    path1: Path = Path("/this/is/AN/invalid/file")
    path2: Path = Path("/this/is/another/bad/f+le")
    path3: Path = Path("/this/file_name/should-w0rk.well")
    path4: Path = Path("/a/b@d/path/to/file")
    path5: Path = Path("/.another/good-path/to_fi1e")

    events: dict[str, list[Path]] = {
        "entity.villager.ambient": [path1, path2, path3],
        "entity.witch.celebrate": [path4, path5]}

    result = get_invalid_file_names(events)
    assert len(result) == 3
    assert result[0] == path1
    assert result[1] == path2
    assert result[2] == path4


def test_get_invalid_file_names_should_return_empty_list_when_names_are_valid():

    path1: Path = Path(".this/1s/a/v4lid-_-file")
    path2: Path = Path("/this/is_another/go0d/file")
    path3: Path = Path("/this/file_name/should-w0rk.well")
    path4: Path = Path("/a/perfectly/cromulent/path/to/file")
    path5: Path = Path("/an9ther/.good-path/to_fi1e")

    events: dict[str, list[Path]] = {
        "entity.villager.hurt": [path1, path2, path3],
        "entity.slime.jump": [path4, path5]}

    result = get_invalid_file_names(events)
    assert len(result) == 0
