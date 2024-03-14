import pytest

from sound_event_handler import SoundEventHandler, SoundEvent
from custom_path import CPath


# --------------------------------------------------------------
# get_event_dictionary
# --------------------------------------------------------------

def test_get_event_dictionary_should_handle_list_of_dictionaries():

    event1: str = "entity.villager.ambient"

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [
                {"name": sound1},
                {"name": sound2},
                {"name": sound3}]}})

    result: dict[str, SoundEvent] = events.get_event_dictionary()

    assert len(result) == 1
    assert len(result[event1]) == 1
    assert len(result[event1]["sounds"]) == 3
    assert type(result[event1]["sounds"]) is list

    for sound in result[event1]["sounds"]:
        assert type(sound) is dict


def test_get_event_dictionary_should_convert_string_sounds_to_sound_dictionaries():

    event1: str = "entity.villager.ambient"

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    # Here, we are deliberately putting strings in place of
    # sound dictionaries to make sure our object handles the
    # processing of Mojang-style non-dictionary references
    # correctly. Our preference is to convert them to dict
    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={event1: {"sounds": [sound1, sound2, sound3]}})

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

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: int = 420

    # Here, we are deliberately putting an int into the sounds
    # to make sure the parsing routine raises a ValueError
    json_events: dict = {event1: {"sounds": [{"name": sound1}, sound2, sound3]}}

    with pytest.raises(ValueError) as result:
        SoundEventHandler(CPath("assets/"), json_events)

    assert str(result.value) == "Expected dict | str got <class 'int'>: value 420"


# --------------------------------------------------------------
# get_event_names
# --------------------------------------------------------------

def test_get_event_names_should_return_event_names_only():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    result: list[str] = events.get_event_names()

    assert len(result) == 3
    assert event1 in result
    assert event2 in result
    assert event3 in result


def test_get_event_names_should_sort_event_names_alphabetically():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

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

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [
                {"name": sound2}, {"name": sound3}, {"name": sound1}]}})

    result: list[str] = events.get_sounds(event1)

    assert len(result) == 3
    assert "path/to/file01" in result
    assert "path/to/file02" in result
    assert "path/to/file03" in result


def test_get_sounds_should_sort_sounds_alphabetically():

    event1: str = "entity.villager.ambient"

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [
                {"name": sound2}, {"name": sound3}, {"name": sound1}]}})

    result: list[str] = events.get_sounds(event1)

    assert len(result) == 3
    assert result[0] == "path/to/file01"
    assert result[1] == "path/to/file02"
    assert result[2] == "path/to/file03"


def test_get_sounds_should_return_sounds_for_just_the_event_specified():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    result: list[str] = events.get_sounds(event2)

    assert len(result) == 1
    assert result[0] == "path/to/squish01"


def test_get_sounds_should_return_all_sounds_from_any_event():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    result: list[str] = events.get_sounds()

    assert len(result) == 5
    assert "path/to/file01" in result
    assert "path/to/file02" in result
    assert "path/to/squish01" in result
    assert "path/to/cackle01" in result
    assert "path/to/cackle02" in result


# --------------------------------------------------------------
# get_sound_files
# --------------------------------------------------------------

def test_get_sound_files_should_return_sounds_when_sounds_exist():

    event1: str = "entity.villager.ambient"

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [
                {"name": sound2}, {"name": sound3}, {"name": sound1}]}})

    result: list[CPath] = events.get_sound_files(event1)

    assert len(result) == 3
    assert CPath("assets/minecraft/sounds/path/to/file01.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/file02.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/file03.ogg") in result


def test_get_sound_files_should_sort_sounds_alphabetically():

    event1: str = "entity.villager.ambient"

    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"
    sound3: str = "path/to/file03"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [
                {"name": sound2}, {"name": sound3}, {"name": sound1}]}})

    result: list[str] = events.get_sound_files(event1)

    assert len(result) == 3
    assert result[0] == CPath("assets/minecraft/sounds/path/to/file01.ogg")
    assert result[1] == CPath("assets/minecraft/sounds/path/to/file02.ogg")
    assert result[2] == CPath("assets/minecraft/sounds/path/to/file03.ogg")


def test_get_sound_files_should_return_sounds_for_just_the_event_specified():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    result: list[str] = events.get_sound_files(event2)

    assert len(result) == 1
    assert result[0] == CPath("assets/minecraft/sounds/path/to/squish01.ogg")


def test_get_sound_files_should_return_all_sounds_from_any_event():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    result: list[str] = events.get_sound_files()

    assert len(result) == 5
    assert CPath("assets/minecraft/sounds/path/to/file01.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/file02.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/squish01.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/cackle01.ogg") in result
    assert CPath("assets/minecraft/sounds/path/to/cackle02.ogg") in result


def test_get_sound_files_should_build_the_path_correctly_including_namespace():

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            "test.event.name": {"sounds": [
                {"name": "namespace:block/beacon/activate/beacon-activate"}]}})

    result: list[str] = events.get_sound_files()

    assert len(result) == 1
    assert result[0] == CPath(
        "assets/namespace/sounds/block/beacon/activate/beacon-activate.ogg")


# --------------------------------------------------------------
# get_sound_files_in
# --------------------------------------------------------------

def test_get_sound_files_in_should_return_list_if_files_exist_in_other_handler():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    alternate_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound1}]},
            event2: {"sounds": [{"name": "path/unique/to/this"}]},
            event3: {"sounds": [{"name": sound5}]}})

    result = alternate_events.get_sound_files_in(events)

    assert len(result) == 2
    assert result[0] == CPath("assets/minecraft/sounds/path/to/cackle02.ogg")
    assert result[1] == CPath("assets/minecraft/sounds/path/to/file01.ogg")


def test_get_sound_files_in_should_return_empty_list_if_no_files_match_in_other_handler():

    event1: str = "entity.villager.ambient"
    sound1: str = "path/to/file01"
    sound2: str = "path/to/file02"

    event2: str = "entity.slime.squish"
    sound3: str = "path/to/squish01"

    event3: str = "entity.witch.celebrate"
    sound4: str = "path/to/cackle01"
    sound5: str = "path/to/cackle02"

    events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={
            event1: {"sounds": [{"name": sound2}, {"name": sound1}]},
            event2: {"sounds": [{"name": sound3}]},
            event3: {"sounds": [{"name": sound4}, {"name": sound5}]}})

    alternate_events = SoundEventHandler(
        root_folder=CPath("assets/"),
        json_events={event1: {"sounds": [{"name": "path/unique/to/this"}]}})

    result = alternate_events.get_sound_files_in(events)

    assert len(result) == 0


# --------------------------------------------------------------
# get_namespace
# --------------------------------------------------------------

def test_get_namespace_should_separate_namespace_correctly():

    sound_name: str = "test-namespace:/path/to/file01"

    events = SoundEventHandler(
        root_folder=CPath("/"),
        json_events={"dummy": {"sounds": ["dummy"]}})

    result: str = events.get_namespace(sound_name)

    assert result == "test-namespace"


def test_get_namespace_should_fall_back_on_minecraft_when_no_namespace_specified():

    sound_name: str = "path/to/file01"
    events = SoundEventHandler(
        root_folder=CPath("/"),
        json_events={"dummy": {"sounds": ["dummy"]}})

    result: str = events.get_namespace(sound_name)

    assert result == "minecraft"


def test_get_namespace_should_fall_back_on_minecraft_when_namespace_is_zero_width():

    sound_name: str = ":/path/to/file01"

    events = SoundEventHandler(
        root_folder=CPath("/"),
        json_events={"dummy": {"sounds": ["dummy"]}})

    result: str = events.get_namespace(sound_name)

    assert result == "minecraft"


# --------------------------------------------------------------
# get_sound_path
# --------------------------------------------------------------

def test_get_sound_path_should_build_the_path_correctly_even_if_ogg_file_contains_the_namespace_name():

    sound1: str = "namespace:file/contains-namespace"

    events = SoundEventHandler(
        root_folder=CPath("storage"),
        json_events={"test": {"sounds": [sound1]}}
    )
    result = events.get_sound_path(sound1)

    assert result == CPath(
        "storage/namespace/sounds/file/contains-namespace.ogg")


def test_get_sound_path_should_build_the_path_correctly_even_if_ogg_file_is_the_namespace_name():

    sound1: str = "namespace:file/namespace"

    events = SoundEventHandler(
        root_folder=CPath("storage"),
        json_events={"test": {"sounds": [sound1]}}
    )
    result = events.get_sound_path(sound1)

    assert result == CPath(
        "storage/namespace/sounds/file/namespace.ogg")


def test_get_sound_path_should_not_stomp_on_a_file_when_the_file_contains_a_dot():

    sound1: str = "namespace:file/name.space"

    events = SoundEventHandler(
        root_folder=CPath("storage"),
        json_events={"test": {"sounds": [sound1]}}
    )
    result = events.get_sound_path(sound1)

    assert result == CPath(
        "storage/namespace/sounds/file/name.space.ogg")

