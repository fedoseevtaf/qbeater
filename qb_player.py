from time import perf_counter as get_now
from typing import Callable

from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect

from qb_sample import Sample


class Player():

    def __init__(self, *args, time_sign: tuple[int] = (4, 8), bpm: int = 90, tact_n: int = 3) -> None:
        self.size = time_sign
        self.bpm = bpm
        self.tact_n = tact_n
        self._volume = 1.0

        self._period = 60 / self.bpm / (self.size[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

        self.sounds = list()

        self._sample = Sample(self.sounds, tact_l=self.size[0], tact_n=tact_n)
        self._sample.clear()  # Super important line, clear fill the mapping of the sample

        self._add_sound_callback = lambda t: t
        self._sounds_queue = list()
        self._sounds_slots = dict()

    def play(self) -> None:
        if self.mode is False:
            return

        beat_start = get_now()
        for sound in self._sample.beat():
            sound.play()

        time_to_next = self._period - (get_now() - beat_start)
        if time_to_next < 0:
            time_to_next = 0
        self._timer.start(int(time_to_next * 1000))

    def add_sound(self, sound_path: str) -> None:
        sound_path = QUrl.fromLocalFile(sound_path)
        sound = QSoundEffect()
        self._sounds_queue.append(sound)
        sound_slot = lambda sound=sound: self._add_sound(sound)
        self._sounds_slots[id(sound)] = sound_slot
        sound.statusChanged.connect(sound_slot)
        sound.setVolume(self._volume)
        sound.setSource(sound_path)

    def _add_sound(self, sound) -> None:
        if sound.status() < 2:
            return
        self._sounds_queue.remove(sound)
        sound.statusChanged.disconnect(self._sounds_slots[id(sound)])
        del self._sounds_slots[id(sound)]
        if sound.status() != 2: #  Ready status
            return
        self._sample.append(sound)
        self._add_sound_callback(sound.source().path())

    def set_new_sound_callback(self, callback: Callable) -> None:
        self._add_sound_callback = callback

    def set_bpm(self, bpm: int) -> None:
        self.bpm = bpm
        self._period = 60 / self.bpm / (self.size[1] / 4)

    def set_volume(self, volume: float) -> None:
        self._volume = volume
        for sound in self.sounds:
            sound.setVolume(volume)

    def resize(self, time_sign: tuple[int] = (4, 8), tact_n: int = 3) -> None:
        self.size = time_sign
        self.tact_n = tact_n
        self._period = 60 / self.bpm / (self.size[1] / 4)
        self._sample.resize(tact_l=self.size[0], tact_n=tact_n)

    def switch(self, sound_index: int, beat_index: int) -> None:
        self._sample.switch(sound_index, beat_index)

    def reset(self) -> None:
        self._sample.reset()

    def turn(self) -> None:
        self.mode = not self.mode
        self.play()

    def turn_on(self) -> None:
        self.mode = True
        self.play()

    def turn_off(self) -> None:
        self.mode = False

    def clear(self) -> None:
        self._sample.clear()

    def rem_sound(self, sound_index: int) -> None:
        self._sample.remove(sound_index)

    def get_tact_n(self) -> int:
        return self._sample.tact_n

    def get_tact_l(self) -> int:
        return self._sample.tact_l
