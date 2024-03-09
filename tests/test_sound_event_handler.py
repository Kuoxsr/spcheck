import pytest

from SoundEventHandler import SoundEventHandler, SoundEvent
from custom_path import Path


# --------------------------------------------------------------
# get_event_dictionary
# --------------------------------------------------------------

def test_get_event_dictionary_should_handle_list_of_dictionaries():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound1}"}}, '
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: dict[str, SoundEvent] = events.get_event_dictionary()

    assert len(result) == 1
    assert len(result[event1]) == 1
    assert len(result[event1]["sounds"]) == 3
    assert type(result[event1]["sounds"]) is list

    for sound in result[event1]["sounds"]:
        assert type(sound) is dict


def test_get_event_dictionary_should_convert_string_sounds_to_sound_dictionaries():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    # Here, we are deliberately putting strings in place of
    # sound dictionaries to make sure our object handles the
    # processing of Mojang-style non-dictionary references
    # correctly. Our preference is to convert them to dict
    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'"{sound1}", '
                        f'"{sound2}", '
                        f'"{sound3}"'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: dict[str, SoundEvent] = events.get_event_dictionary()

    assert len(result) == 1
    assert len(result[event1]) == 1
    assert len(result[event1]["sounds"]) == 3
    assert type(result[event1]["sounds"]) is list

    # Every "sound" reference should be a dict
    for sound in result[event1]["sounds"]:
        assert type(sound) is dict


def test_get_event_dictionary_should_raise_value_error_when_sound_is_wrong_data_type():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: int = 420

    # Here, we are deliberately putting an int into the sounds
    # to make sure the parsing routine raises a ValueError
    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound1}"}}, '
                        f'"{sound2}", '
                        f'{sound3}'
                        f']}}}}')

    with pytest.raises(ValueError) as result:
        SoundEventHandler(json_events)

    assert str(result.value) == "Expected dict | str got <class 'int'>: value 420"


# --------------------------------------------------------------
# get_event_names
# --------------------------------------------------------------

def test_get_event_names_should_return_event_names_only():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_event_names()

    assert len(result) == 3
    assert event1 in result
    assert event2 in result
    assert event3 in result


def test_get_event_names_should_sort_event_names_alphabetically():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_event_names()

    assert len(result) == 3
    assert result[0] == "entity.slime.squish"
    assert result[1] == "entity.villager.ambient"
    assert result[2] == "entity.witch.celebrate"


# --------------------------------------------------------------
# get_sounds
# --------------------------------------------------------------

def test_get_sounds_should_return_sounds_when_sounds_exist():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}, '
                        f'{{"name": "{sound1}"}} '
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sounds(event1)

    assert len(result) == 3
    assert "/path/to/file01" in result
    assert "/path/to/file02" in result
    assert "/path/to/file03" in result


def test_get_sounds_should_sort_sounds_alphabetically():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}, '
                        f'{{"name": "{sound1}"}} '
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sounds(event1)

    assert len(result) == 3
    assert result[0] == "/path/to/file01"
    assert result[1] == "/path/to/file02"
    assert result[2] == "/path/to/file03"


def test_get_sounds_should_return_sounds_for_just_the_event_specified():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sounds(event2)

    assert len(result) == 1
    assert result[0] == "/path/to/squish01"


def test_get_sounds_should_return_all_sounds_from_any_event():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sounds()

    assert len(result) == 5
    assert "/path/to/file01" in result
    assert "/path/to/file02" in result
    assert "/path/to/squish01" in result
    assert "/path/to/cackle01" in result
    assert "/path/to/cackle02" in result


# --------------------------------------------------------------
# get_sound_files
# --------------------------------------------------------------

def test_get_sound_files_should_return_sounds_when_sounds_exist():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}, '
                        f'{{"name": "{sound1}"}} '
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[Path] = events.get_sound_files(event1)

    assert len(result) == 3
    assert Path("/path/to/file01.ogg") in result
    assert Path("/path/to/file02.ogg") in result
    assert Path("/path/to/file03.ogg") in result


def test_get_sound_files_should_not_add_suffix_if_string_already_contains_one():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02.ogg"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}, '
                        f'{{"name": "{sound1}"}} '
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sound_files(event1)

    assert len(result) == 3
    assert Path("/path/to/file01.ogg") in result
    assert Path("/path/to/file02.ogg") in result
    assert Path("/path/to/file03.ogg") in result


def test_get_sound_files_should_sort_sounds_alphabetically():

    event1: str = "entity.villager.ambient"

    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"
    sound3: str = "/path/to/file03"

    json_events: str = (f'{{"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound3}"}}, '
                        f'{{"name": "{sound1}"}} '
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sound_files(event1)

    assert len(result) == 3
    assert result[0] == Path("/path/to/file01.ogg")
    assert result[1] == Path("/path/to/file02.ogg")
    assert result[2] == Path("/path/to/file03.ogg")


def test_get_sound_files_should_return_sounds_for_just_the_event_specified():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sound_files(event2)

    assert len(result) == 1
    assert result[0] == Path("/path/to/squish01.ogg")


def test_get_sound_files_should_return_all_sounds_from_any_event():

    event1: str = "entity.villager.ambient"
    sound1: str = "/path/to/file01"
    sound2: str = "/path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "/path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "/path/to/cackle01"
    sound5: str = "/path/to/cackle02"

    json_events: str = (f'{{'
                        f'"{event1}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound2}"}}, '
                        f'{{"name": "{sound1}"}}'
                        f']}}, '
                        f'"{event2}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound3}"}}'
                        f']}}, '
                        f'"{event3}": {{'
                        f'"sounds": ['
                        f'{{"name": "{sound4}"}}, '
                        f'{{"name": "{sound5}"}}'
                        f']}}}}')

    events: SoundEventHandler = SoundEventHandler(json_events)

    result: list[str] = events.get_sound_files()

    assert len(result) == 5
    assert Path("/path/to/file01.ogg") in result
    assert Path("/path/to/file02.ogg") in result
    assert Path("/path/to/squish01.ogg") in result
    assert Path("/path/to/cackle01.ogg") in result
    assert Path("/path/to/cackle02.ogg") in result


# --------------------------------------------------------------
# get_namespace
# --------------------------------------------------------------

def test_get_namespace_should_separate_namespace_correctly():

    sound_name: str = "test-namespace:/path/to/file01"
    events = SoundEventHandler('{"dummy": {"sounds": ["dummy"]}}')

    result: str = events.get_namespace(sound_name)

    assert result == "test-namespace"


def test_get_namespace_should_fall_back_on_minecraft_when_no_namespace_specified():

    sound_name: str = "/path/to/file01"
    events = SoundEventHandler('{"dummy": {"sounds": ["dummy"]}}')

    result: str = events.get_namespace(sound_name)

    assert result == "minecraft"


def test_get_namespace_should_fall_back_on_minecraft_when_namespace_is_zero_width():

    sound_name: str = ":/path/to/file01"
    events = SoundEventHandler('{"dummy": {"sounds": ["dummy"]}}')

    result: str = events.get_namespace(sound_name)

    assert result == "minecraft"
