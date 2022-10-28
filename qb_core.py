'''\
qb_sample provides tools for sounds's mapping.
'''


from typing import Callable, Iterable


class Sample():
    '''\
    Sample provides managing for list of sounds
    without any information about what sound is.
    '''

    def __init__(self, sounds: list, *args,
                 tact_l: int = 3, tact_n: int = 4) -> None:

        '''\
        'tact_l' - length of tact
        'tact_n' - number of tacts in sample

        'mapping' is used to remind what beat
        what sound should be played.
        '''

        self.tact_l = tact_l
        self.tact_n = tact_n

        self._sounds = sounds
        self._mapping = list()

        self._actual_beat_num = 0
        self._sample_len = tact_l * tact_n
        self._sounds_len = len(sounds)


    def switch(self, sound_index: int, beat_index: int) -> None:
        '''\
        Turn on/off defined sound at defined beat.
        '''
        if 0 <= sound_index < self._sounds_len and 0 <= beat_index < self._sample_len:
            self._mapping[sound_index][beat_index] ^= 1

    def beat(self) -> Iterable:
        '''\
        Yield all sounds that should be played
        at that beat for playing them.
        '''

        for sound_index, sound in enumerate(self._sounds):
            if self._mapping[sound_index][self._actual_beat_num]:
                yield sound

        self._actual_beat_num += 1
        self._actual_beat_num %= self._sample_len

    def goto_start(self) -> None:
        '''\
        Turn back play pointer to the beginning of the sample.
        '''

        self._actual_beat_num = 0

    def clear(self) -> None:
        '''\
        Refill the mapping.
        '''

        self._mapping.clear()
        self._mapping.extend(bytearray(self._sample_len) for _ in range(self._sounds_len))

    def resize(self, tact_l: int, tact_n: int) -> None:
        '''\
        Change:
            <*> The time signature. But only meter, because
                sample don't save note length.
            <*> The 'track' size (amount of tacts in the sample)

        With resizing the mapping will be cleaned
        by the 'clear' method.
        '''

        self.tact_l = tact_l
        self.tact_n = tact_n

        self._sample_len = tact_l * tact_n
        self.clear()

    def append(self, sound: object) -> None:
        '''\
        Add new sound and make mapping for it.
        '''

        self._sounds.append(sound)
        self._mapping.append(bytearray(self._sample_len))
        self._sounds_len += 1

    def remove(self, sound_index: int) -> None:
        '''\
        Remove the sound and his mapping by the index of the sound.
        '''

        if 0 <= sound_index < self._sounds_len:
            del self._sounds[sound_index]
            del self._mapping[sound_index]
            self._sounds_len -= 1


class AbstractSound():

    def __init__(self, sound_obj: object) -> None:
        pass

    def play(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def set_volume(self, volume: float) -> None:
        pass

    def source(self) -> str:
        return 'None'


class AbstractLoader():

    def __init__(self) -> None:
        self._install_sound = id
        self._draw_sound = print

    def load_sound(self, sound_path: str) -> None:
        pass

    def set_installer(self, installer: Callable) -> None:
        self._install_sound = installer

    def set_drawer(self, drawer: Callable) -> None:
        self._draw_sound = drawer


class AbstractSoundManager():

    def __init_subclass__(cls, loader: type = AbstractLoader) -> None:
        cls.__loader = loader

    def _init_loader(self) -> None:
        self._loader = type(self).__loader()
        self._loader.set_installer(self._install_sound)
        self._loader.set_drawer(print)

    def add_sound(self, sound_path: str) -> None:
        self._loader.load_sound(sound_path)

    def set_draw_sound_callback(self, callback: Callable) -> None:
        self._loader.set_drawer(callback)

    def _install_sound(self, sound: AbstractSound) -> None:
        pass


class AbstractPlayer():

    def _init_sample(self, *args, time_sign: tuple[int] = (4, 8),
                     bpm: int = 90, tact_n: int = 3) -> None:
        '''\
        The 'time signature' is a musician term, read about it on wiki.
        https://en.wikipedia.org/wiki/Time_signature
        The 'bpm' is a Beats Per Minute.
        '''

        self.time_sign = time_sign
        self.bpm = bpm

        self._sounds = list()
        self._sample: AbstractSample = Sample(self._sounds, tact_l=self.time_sign[0], tact_n=tact_n)
        self._sample.clear()  # Super important line, clear fill the mapping of the sample

    def set_bpm(self, bpm: int) -> None:
        '''\
        Read about bpm in __init__'s docs.
        This function probably will be reimplemented.
        '''

        self._set_bpm()

    def resize(self, time_sign: tuple[int] = (4, 8), tact_n: int = 3) -> None:
        '''\
        Sample.resize, but using the time signature.
        This function probably will be reimplemented.
        '''

        self._resize(time_sign, tact_n)

    def _add_sound(self, sound) -> None:
        '''\
        Minimal implementation that probably will be used
        at 'add_widget' future implementation.
        '''

        self._sample.append(sound)

    def _set_bpm(self, bpm: int) -> None:
        '''\
        Minimal implementation that probably will be used
        at 'set_bpm' future implementation.
        '''

        self.bpm = bpm

    def _resize(self, time_sign: tuple[int] = (4, 8), tact_n: int = 3) -> None:
        '''\
        Minimal implementation that probably will be used
        at 'resize' future implementation.
        '''

        self.time_sign = time_sign
        self._sample.resize(tact_l=self.time_sign[0], tact_n=tact_n)

    def _beat(self) -> Iterable:
        '''\
        Facade for the Sample.
        '''

        yield from self._sample.beat()

    def switch(self, sound_index: int, beat_index: int) -> None:
        '''\
        Facade for the Sample.
        '''

        self._sample.switch(sound_index, beat_index)

    def goto_start(self) -> None:
        '''\
        Facade for the Sample.
        '''

        self._sample.goto_start()

    def clear(self) -> None:
        '''\
        Facade for the Sample.
        '''

        self._sample.clear()

    def rem_sound(self, sound_index: int) -> None:
        '''\
        Facade for the Sample.
        '''

        self._sample.remove(sound_index)

    def get_tact_n(self) -> int:
        '''\
        Facade for the Sample.
        '''

        return self._sample.tact_n

    def get_tact_l(self) -> int:
        '''\
        Facade for the Sample.
        '''

        return self._sample.tact_l
