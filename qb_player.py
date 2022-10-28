from time import perf_counter as get_now

from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect

from qb_core import AbstractPlayer, AbstractSoundManager, AbstractSound, AbstractLoader


class Sound(AbstractSound):

    def __init__(self, sound_obj: QSoundEffect) -> None:
        self.sound_obj = sound_obj

    def play(self) -> None:
        self.sound_obj.play()

    def stop(self) -> None:
        self.sound_obj.stop()

    def set_volume(self, volume: float) -> None:
        self.sound_obj.setVolume(volume)

    def source(self) -> str:
        return self.sound_obj.source().path()


class SoundLoader(AbstractLoader):
    '''\
    Word about sound's adding policy:
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

    Word about displaying policy:
    The player has no tools for displaying the sound mapping
    and providing ui. Therefor the player use
    '_draw_sound_callback' to "notify" the ui that sound is
    successfully added to the sample.
    '''

    def __init__(self) -> None:
        self._sounds_queue = dict()
        self._sounds_slots = dict()

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
            sound = Sound(sound)
            self._install_sound(sound)
            self._draw_sound(sound)

    def _store_in_queue(self, sound: QSoundEffect) -> None:
        '''\C:/users/user/desktop/1.wav
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


class Player(AbstractPlayer, AbstractSoundManager, loader=SoundLoader):

    def __init__(self, *args, time_sign: tuple[int] = (4, 8), bpm: int = 90, tact_n: int = 3) -> None:
        self._init_sample(time_sign=time_sign, bpm=bpm, tact_n=tact_n)
        self._init_loader()

        self._volume = 0
        self._is_turned_on = False

        self._period = 60 / self.bpm / (self.time_sign[1] / 4)
        self._timer = QTimer()
        self._timer.timeout.connect(self.play)

    def _install_sound(self, sound: AbstractSound) -> None:
        self._add_sound(sound)
        sound.set_volume(self._volume)

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
        if time_to_next < 0:
            time_to_next = 0
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

        self._resize(time_sign)
        self._period = 60 / self.bpm / (self.time_sign[1] / 4)

    def set_volume(self, volume: float) -> None:
        '''\
        Update volume of all sounds.
        '''

        self._volume = volume
        for sound in self._sounds:
            sound.set_volume(volume)

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
