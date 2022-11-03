'''\
qb_storage implement qb_abs_storage stuff.
'''

from os import path as ospath
from typing import Iterable

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

    def load_sound(self, sound_path: str) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        if sound_path == '':
            return
        self._load_sound(sound_path)

    def _load_sound(self, sound_path: str) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        sound = QSoundEffect()
        self._store_in_queue(sound)
        sound.setSource(QUrl.fromLocalFile(sound_path))

    def _sound_is_loaded(self, sound: QSoundEffect) -> None:
        '''\
        Read a "Word about sound's adding policy" in the class docs.
        '''

        if sound.status() > 1: #  Sound is loaded
            self._remove_out_queue(sound)

        if sound.status() == 2: #  Sound is corect
            self._add_sound(sound)

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

    def _add_sound(self, sound: QSoundEffect) -> None:
        sound_id = id(sound)
        sound = Sound(sound)
        self._preset_sound(sound, sound_id)
        self._draw_sound(sound)
        self._update_view()

    def _preset_sound(self, sound: AbstractSound, mapping_id: int) -> None:
        try:
            self._install_sound(sound, self._mappings[mapping_id])
            del self._mappings[mapping_id]
        except KeyError:
            self._install_sound(sound)

    def upload_project(self, pjpath: str) -> None:
        '''\
        Load project from the 'path'.
        '''

        paths, mapping = self._upload_data(pjpath)
        if paths is None:
            return
        for sound_path, mapping_line in zip(paths, mapping):
            sound = QSoundEffect()
            self._mappings[id(sound)] = mapping_line
            self._store_in_queue(sound)
            sound.setSource(QUrl.fromLocalFile(sound_path))

    def _upload_data(self, pjpath: str) -> tuple[Iterable | None]:
        '''\
        Upload data that is loaded by unload and return it.
        '''

        try:
            file = open(pjpath)
            lines = file.readlines()
            paths = tuple(lines[i][:-1] for i in range(0, len(lines), 2))
            view = []
            for i in range(1, len(lines), 2):
                line = lines[i]
                view.append(bytes(int(char) for char in line[:-1]))
            file.close()
        except:
            return None, None
        return paths, view

    def unload_project(self, pjpath: str, view: Sample, sounds: list[AbstractSound]) -> None:
        '''\
        Save project to the 'path'.
        '''

        with open(pjpath, 'w') as file:
            for sound, view_line in zip(sounds, view.view()):
                file.write(ospath.abspath(sound.source()))
                file.write('\n')
                for flag in view_line:
                    file.write(str(int(flag)))
                file.write('\n')
