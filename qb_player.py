from time import perf_counter as get_now

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound

from qb_sample import Sample


MusicSize = tuple[int]
'''\
Not a completely musician size:
    <*> 3/4 is 3, 2         (2 ^ 2 = 4)
    <*> 5/8 is 5, 3         (2 ^ 3 = 8)
    <*> 4/16 is 4, 4        (2 ^ 4 = 16)
'''


class Player():

    def __init__(self, music_size: MusicSize = (3, 2), bpm: int = 100,
                 sounds: list[str] = None, titles: dict = None) -> None:
        self.size = music_size[0], 2 ** music_size[1]
        self.bpm = bpm

        self._period = 60 / self.bpm / (self.size[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

        self.mode: bool = False  # Is player turned on

        self.titles = list()
        if not (titles is None):
            self.titles.extend((titles[sound]  if sound in titles else 'Sound')
                               for sound in self.sounds)
        self.sounds = list(map(QSound, sounds))

        self._sample = Sample(self.size[0], 4,
                             self.sounds, list(), self.titles)
        self._sample.clear()  # Super important line, clear fill the mappimg of the sample

    def play(self) -> None:
        beat_start = get_now()
        if self.mode is True:
            for sound in self._sample.beat():
                sound.play()

        time_to_next = self._period - (get_now() - beat_start)
        if time_to_next < 0:
            time_to_next = 0
        self._timer.start(int(time_to_next * 1000))

    def switch(self, sound_index: int, beat_index: int) -> None:
        self._sample.switch(sound_index, beat_index)

    def reset(self) -> None:
        self._sample.reset()

    def turn(self) -> None:
        self.mode ^= True

    def turn_on(self) -> None:
        self.mode = True

    def turn_off(self) -> None:
        self.mode = False

    def clear(self) -> None:
        self._sample.clear()

    def add(self, sound_path: str, sound_title: str = 'Sound') -> None:
        self._sample.append(QSound(sound_path), sound_title)

    def rem(self, sound_index: int) -> None:
        self._sample.remove(sound_index)
