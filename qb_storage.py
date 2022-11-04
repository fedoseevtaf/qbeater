'''\
qb_storage implement qb_abs_storage stuff.
'''

from os import path as ospath
from typing import Iterable, TextIO

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QSoundEffect

from qb_abs_storage import AbstractStorage, AbstractSound
from qb_core import Sample


class Sound(AbstractSound):
    '''\
    Implement AbstractSound using QSoundEffect
    '''

    def __init__(self, sound_obj: QSoundEffect) -> None:
        '''\
        Store 'sound_obejct'.
        '''

        self.sound_obj = sound_obj

    def play(self) -> None:
        self.sound_obj.play()

    def stop(self) -> None:
        self.sound_obj.stop()

    def set_volume(self, volume: float) -> None:
        self.sound_obj.setVolume(volume)

    def source(self) -> str:
        return self.sound_obj.source().path()


class Storage(AbstractStorage):
    '''\
    Implement 'AbstractStorage' interface.

    Word about sound's adding policy:
    QSoundEffect load data asynchronously and don't raise the Exceptions.
    Therefore, there is such a complex way to add new sounds.

    Player uses '_load_sound' method to make the sound, sets the source of it,
    and call the '_store_in_queue' to sound.

    '_store_in_queue' stores the sound in the '_sounds_queue' to avoid deletion
    by the garbage collector, connects sound's status changing to the '_sound_is_loaded'
    using lambda-slot, because there is no access to the 'sender' in this scope,
    and also stores that slot in '_sounds_slots' for disconnection in the future.

    '_sound_is_loaded' checks that this sound is truly loaded (maybe with an error),
    calls the '_remove_out_queue' to sound, and if the sound is ready to play (correct),
    sound will be added by the '_install_sound' callback and drawn by the '_draw_sound' callback.
    (callbacks are inherited by the AbstractLoader)

    '_remove_out_queue' removes the sound out the '_sounds_queue',
    disconnects sound's status changing to the lambda-slot and removes it
    out the '_sounds_slots'.
    '''

    def __init__(self) -> None:
        super().__init__()
        self._sounds_queue = {}
        self._sounds_slots = {}
        self._mappings = {}

    def load_sound(self, sound_path: str, mapping: Iterable[int]) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        if sound_path == '':
            return
        self._load_sound(sound_path, mapping)

    def _load_sound(self, sound_path: str, mapping: Iterable[int]) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        sound = QSoundEffect()
        self._mappings[id(sound)] = mapping
        self._store_in_queue(sound)
        sound.setSource(QUrl.fromLocalFile(sound_path))

    def _sound_is_loaded(self, sound: QSoundEffect) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        if sound.status() < 2: #  Sound is not loaded
            return
        self._remove_out_queue(sound)
        mapping = self._mappings.pop(id(sound))
        if sound.status() == 2: #  Sound is corect
            return self._apply_callbacks(sound, mapping)
        self._display_notification(f'Error of loading the sound ({sound.source().path()})!')

    def _apply_callbacks(self, sound: QSoundEffect, mapping: Iterable[int]) -> None:
        '''\
        Read about callbacks in docs of the AbstractStorage.
        '''

        sound = Sound(sound)
        self._install_sound(sound, mapping)
        self._draw_sound(sound)
        self._update_view()

    def _store_in_queue(self, sound: QSoundEffect) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '_store_in_queue' stores the sound in the '_sounds_queue' to avoid deletion
        by the garbage collector, connects sound's status changing to the '_sound_is_loaded'
        using lambda-slot, because there is no access to the 'sender' in this scope,
        and also stores that slot in '_sounds_slots' for disconnection in the future.
        '''

        self._sounds_queue[id(sound)] = sound
        self._sounds_slots[id(sound)] = lambda sound=sound: self._sound_is_loaded(sound)
        sound.statusChanged.connect(self._sounds_slots[id(sound)])

    def _remove_out_queue(self, sound: QSoundEffect) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        del self._sounds_queue[id(sound)]
        sound.statusChanged.disconnect(self._sounds_slots[id(sound)])
        del self._sounds_slots[id(sound)]

    def upload_project(self, pjpath: str) -> None:
        '''\
        Load project from the 'path'.
        '''

        paths, mapping = self._upload_data(pjpath)
        if paths is None:
            return
        for sound_path, mapping_line in zip(paths, mapping):
            self.load_sound(sound_path, mapping_line)

    def _upload_data(self, pjpath: str) -> tuple[Iterable | None]:
        '''\
        Upload data that is loaded by unload and return it.
        '''

        try:
            paths, mapping = self.__extract_file(pjpath)
        except:
            self._display_notification(f'Error of loading the project ({pjpath})!')
            return None, None
        return paths, mapping

    def __extract_file(self, pjpath: str) -> Iterable[Iterable[str] | Iterable[Iterable[int]]]:
        file = open(pjpath)
        lines = file.readlines()
        yield self.__extract_paths(lines)
        yield self.__extract_mapping(lines)
        file.close()

    def __extract_paths(self, lines: list[str]) -> Iterable[str]:
        for i in range(0, len(lines), 2):
            yield lines[i].strip('\n')

    def __extract_mapping(self, lines: list[str]) -> Iterable[Iterable[int]]:
        for i in range(1, len(lines), 2):
            line = lines[i].strip('\n')
            yield bytes(int(char) for char in line)

    def unload_project(self, pjpath: str, sample: Sample, sounds: list[AbstractSound]) -> None:
        '''\
        Save project to the 'path'.
        '''

        try:
            file = open(pjpath, 'w')
            self.__write_data(file, sample, sounds)
            file.close()
        except:
            return self._display_notification(f'Error of saving the project ({pjpath})!')
        return

    def __write_data(self, file: TextIO, sample: Sample, sounds: list[AbstractSound]) -> None:
        for sound, mapping in zip(sounds, sample.view()):
            file.write(ospath.abspath(sound.source()))
            file.write('\n')
            file.write(''.join(map(str, mapping)))
            file.write('\n')
