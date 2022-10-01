from time import perf_counter as get_now
from typing import Iterable

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound

from qb_sample import Sample


class SoundIsUnfined(Exception):
    pass


class Player():

    def __init__(self, time_sign: tuple[int] = (3, 4), bpm: int = 90, nbeats_limit: int = 20) -> None:
        self.size = time_sign
        self.bpm = bpm

        self._nbeats_limit = nbeats_limit

        self._period = 60 / self.bpm / (self.size[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

        self.sounds = list()
        self.titles = list()

        tact_n = (self._nbeats_limit // self.size[0]) * self.size[0]
        self._sample = Sample(self.sounds, self.titles, tact_l=self.size[0], tact_n=tact_n)
        self._sample.clear()  # Super important line, clear fill the mapping of the sample

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

    def setbpm(self, bpm: int) -> None:
        self.bpm = bpm
        self._period = 60 / self.bpm / (self.size[1] / 4)

    def resize(self, time_sign: tuple[int] = (3, 2), nbeats_limit: int = 20) -> None:
        self.size = time_sign[0], 2 ** time_sign[1]
        self._nbeats_limit = nbeats_limit
        self._period = 60 / self.bpm / (self.size[1] / 4)
        tact_n = (self._nbeats_limit // self.size[0]) * self.size[0]
        self._sample.resize(tact_l=self.size[0], tact_n=(tact_n)

    def switch(self, sound_index: int, beat_index: int) -> None:
        self._sample.switch(sound_index, beat_index)

    def reset(self) -> None:
        self._sample.reset()

    def turn(self) -> None:
        self.mode ^= True
        self.play()

    def turn_on(self) -> None:
        self.mode = True
        self.play()

    def turn_off(self) -> None:
        self.mode = False

    def clear(self) -> None:
        self._sample.clear()

    def add(self, sound_path: str, sound_title: str = 'Sound') -> None:
        try:
            sound = QSound(sound_path)
        except:
            raise SoundIsUnfined
        self._sample.append(sound, sound_title)

    def rem(self, sound_index: int) -> None:
        self._sample.remove(sound_index)

    def titles(self) -> Iterable:
        yield from self.titles
