'''\
qb_player provides Player class that should be used
as core implementation for ui.
'''


from time import perf_counter as get_now
from typing import Iterable

from PyQt5.QtCore import QTimer

from qb_abs_storage import AbstractStorageClient, AbstractSound
from qb_core import AbstractSampleClient
from qb_storage import Storage


class Player(AbstractSampleClient, AbstractStorageClient, storage=Storage):
    '''\
    Implementation for ui.
    '''

    def __init__(self, /, time_sign: tuple[int] = (4, 8), bpm: int = 90, tact_n: int = 3) -> None:
        super().__init__(time_sign=time_sign, bpm=bpm, tact_n=tact_n)

        self._volume = 0
        self._is_turned_on = False

        self._period = 60 / self.bpm / (self.time_sign[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

    def _install_sound(self, sound: AbstractSound, mapping: Iterable[int]) -> None:
        self._add_sound(sound, mapping)
        sound.set_volume(self._volume)

    def _get_view(self) -> Iterable:
        yield self.view()
        yield self._sounds

    def play(self) -> None:
        '''\
        Run and implement playing cycle.
        '''

        if self._is_turned_on is False:
            return
        beat_start = get_now()
        self._play_beat()
        self._wait_next_beat(beat_start)

    def _wait_next_beat(self, beat_start: float) -> None:
        '''\
        Preset timer to the next beat time with
        correction by the actual beat playing time,
        to avoid slow bpm, because of long play running.
        '''

        time_to_next = self._period - (get_now() - beat_start)
        time_to_next = max(time_to_next, 0)
        self._timer.start(int(time_to_next * 1000))

    def _play_beat(self) -> None:
        '''\
        Play all the sounds that should be played at
        that beat.
        '''

        for sound in self._beat():
            sound.play()

    def set_bpm(self, bpm: int) -> None:
        '''\
        Reuse inherited 'set_bpm' and set a '_period'.
        '''

        self._set_bpm(bpm)
        self._period = 60 / self.bpm / (self.time_sign[1] / 4)

    def resize(self, time_sign: tuple[int] = (4, 8), tact_n: int = 3) -> None:
        '''\
        Reuse inherited 'resize' and set a '_period'.
        '''

        self._resize(time_sign, tact_n)
        self._period = 60 / self.bpm / (self.time_sign[1] / 4)

    def set_volume(self, volume: float) -> None:
        '''\
        Update volume of all sounds.
        '''

        for sound in self._sounds:
            sound.set_volume(volume)
        self._volume = volume

    def turn(self) -> None:
        '''\
        Method for encapsulation play on/off logic.
        '''

        if self._is_turned_on:
            return self.turn_off()
        self.turn_on()

    def turn_on(self) -> None:
        '''\
        Start playing.
        '''

        self._is_turned_on = True
        self.play()

    def turn_off(self) -> None:
        '''\
        Turn off, but the playing process must be stopped by itself.
        '''

        self._is_turned_on = False
