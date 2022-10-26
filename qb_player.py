from time import perf_counter as get_now

from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect

from qb_sample import AbstractPlayer


class Player(AbstractPlayer):
    '''\
    Word about adding sounds policy:
    QSoundEffect load data asynchronously and don't raise the Exceptions.
    Therefore, there is such a complex way to add new sounds.

    Player uses '_load_sound' method to make the sound, sets the source of it,
    and call the '_store_in_queue' to sound.

    '_store_in_queue' stores the sound in the '_sounds_queue' to avoid deletion
    by the garbage collector, connects sound's status changing to the '_sound_is_loaded'
    using lambda-slot, because there is no access to the 'sender' in this scope,
    and also stores that slot in '_sounds_slots' for disconnection in the future.

    '_sound_is_loaded' checks that this sound is truly loaded (maybe with an error)
    and calls '_install_sound'.

    '_install_sound' calls the '_remove_out_queue' to sound,
    and if the sound is ready to play (correct), sound will be added
    by the inherited implementation of 'add_sound',
    and also sets the volume of the sound.

    '_remove_out_queue' removes the sound out the '_sounds_queue',
    disconnects sound's status changing to the lambda-slot and removes it
    out the '_sounds_slots'.

    Read also the "Word about displaying policy" in the AbstractPlayer docs.
    '''

    def __init__(self, *args, time_sign: tuple[int] = (4, 8), bpm: int = 90, tact_n: int = 3) -> None:
        super().__init__(time_sign=time_sign, bpm=bpm, tact_n=tact_n)
        self._is_turned_on = False

        self._period = 60 / self.bpm / (self.time_sign[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

        self._sounds_queue = dict()
        self._sounds_slots = dict()

    def add_sound(self, sound_path: str) -> None:
        if sound_path == '':
            return
        self._load_sound(sound_path)

    def _load_sound(self, sound_path: str) -> None:
        sound = QSoundEffect()
        self._store_in_queue(sound)
        sound.setSource(QUrl.fromLocalFile(sound_path))

    def _sound_is_loaded(self, sound) -> None:
        if sound.status() < 2:
            #  Sound isn't loaded.
            return
        self._install_sound(sound)

    def _install_sound(self, sound) -> None:
        self._remove_out_queue(sound)
        if sound.status() != 2: #  Ready status
            return
        self._add_sound(sound, sound.source().path())
        sound.setVolume(self._volume)

    def _store_in_queue(self, sound: QSoundEffect) -> None:
        self._sounds_queue[id(sound)] = sound
        self._sounds_slots[id(sound)] = lambda sound=sound: self._sound_is_loaded(sound)
        sound.statusChanged.connect(self._sounds_slots[id(sound)])

    def _remove_out_queue(self, sound: QSoundEffect) -> None:
        del self._sounds_queue[id(sound)]
        sound.statusChanged.disconnect(self._sounds_slots[id(sound)])
        del self._sounds_slots[id(sound)]

    def play(self) -> None:
        if self._is_turned_on is False:
            return
        beat_start = get_now()
        self._play_beat()
        self._wait_next_beat(beat_start)

    def _wait_next_beat(self, beat_start: float) -> None:
        time_to_next = self._period - (get_now() - beat_start)
        if time_to_next < 0:
            time_to_next = 0
        self._timer.start(int(time_to_next * 1000))

    def _play_beat(self) -> None:
        for sound in self._sample.beat():
            sound.play()

    def set_bpm(self, bpm: int) -> None:
        super().set_bpm(bpm)
        self._period = 60 / self.bpm / (self.time_sign[1] / 4)

    def resize(self, time_sign: tuple[int] = (4, 8), tact_n: int = 3) -> None:
        super().resize(time_sign)
        self._period = 60 / self.bpm / (self.time_sign[1] / 4)

    def set_volume(self, volume: float) -> None:
        self._volume = volume
        for sound in self._sounds:
            sound.setVolume(volume)

    def turn(self) -> None:
        if self._is_turned_on:
            return self.turn_off()
        self.turn_on()

    def turn_on(self) -> None:
        self._is_turned_on = True
        self.play()

    def turn_off(self) -> None:
        self._is_turned_on = False
