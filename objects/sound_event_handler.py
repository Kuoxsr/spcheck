import json
from typing import TypedDict, NotRequired

from pathlib import Path




class Sound(TypedDict):
    name: str
    volume: NotRequired[float]
    pitch: NotRequired[float]
    weight: NotRequired[int]
    stream: NotRequired[bool]
    attenuation_distance: NotRequired[int]
    preload: NotRequired[bool]
    type: NotRequired[str]


class SoundEvent(TypedDict):
    replace: NotRequired[bool]
    sounds: list[Sound]
    subtitle: NotRequired[str]


class SoundEventHandler:
    def __init__(self, root_folder: Path, json_events: dict):
        self.root_folder: Path = root_folder
        self.raw_json: dict = json_events
        self.events: dict[str, SoundEvent] = self._parse_json()

    def _parse_json(self) -> dict[str, SoundEvent]:
        """
        Mojang's vanilla sounds.json contains many examples of lists of
        plain strings instead of dictionaries like our Sound object.
        We want to convert those here, so we don't need to expect
        to handle them later on.
        """
        json_dict: dict[str, SoundEvent] = self.raw_json
        for key, event in json_dict.items():

            new_sounds: list[Sound] = []
            for sound in event['sounds']:

                if isinstance(sound, dict):
                    new_sounds.append(sound)
                    continue

                if isinstance(sound, str):
                    new_sounds.append(Sound(name=sound))
                    continue

                # If we make it here, the data type is wrong
                raise ValueError(
                    f"Expected dict | str got {type(sound)}: value {sound}")

            event['sounds'] = new_sounds

        return json_dict

    def get_event_dictionary(self) -> dict[str, SoundEvent]:
        """Return the events as a dictionary of SoundEvent"""
        return self.events

    def get_event_names(self):
        """Return a simple list of all the sound event names"""
        return sorted(list(self.events.keys()))

    def get_sounds(self, event_name: str = None):
        """
        Extract the references to sound files in the data structure
        as they appear in the sounds.json file (no suffixes)
        """
        sound_files: list[str] = []
        event_names: list[str] = (
            [event_name] if event_name is not None else self.get_event_names())

        for key in event_names:

            for sound in self.events[key]['sounds']:
                sound_files.append(sound['name'])

        return sorted(sound_files)  # noqa

    def get_sound_files(self, event_name: str = None):
        """
        Extract the references to sound files in the data structure
        as file paths (with ".ogg" suffix)
        """
        sounds = self.get_sounds(event_name)
        sound_files = [self.get_sound_path(s) for s in sounds]
        return sorted(sound_files)  # noqa

    def get_sound_files_in(self, other_sound_event_handler):
        """Return a list of sound files that also exist in another instance"""

        this = self.get_sound_files()
        other = other_sound_event_handler.get_sound_files()

        result = set(this).intersection(other)
        return sorted(result)  # noqa

    @staticmethod
    def get_namespace(sound_name: str) -> str:
        """Extract the namespace from a sound record"""

        namespace: str = "minecraft"

        if ":" in sound_name:
            parts = sound_name.split(":")

            if len(parts[0]) > 0:
                namespace = parts[0]

        return namespace

    def get_sound_path(self, sound_name: str) -> Path:
        """Create a real path from a sound record"""

        namespace: str = "minecraft"
        sound_path: str = sound_name

        if ":" in sound_name:
            parts: list[str] = sound_name.split(":")
            namespace: str = parts[0]
            sound_path: str = parts[1]

        # Start with the root folder, unless sound_path already has it
        result: str = (
                str(self.root_folder) + "/" +
                namespace +
                "/sounds/" +
                sound_path + ".ogg")

        # Finish it off with the suffix
        return Path(result)
