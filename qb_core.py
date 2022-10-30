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
        'tact_l' - length of tact (metre)
        'tact_n' - number of tacts in sample

        '_mapping' is used to remind what beat
        what sound should be played.
        '''

        self.tact_l = tact_l
        self.tact_n = tact_n

        self._sounds = sounds
        self._mapping = list()

        self._actual_beat_num = 0
        self._sample_len = tact_l * tact_n
        self._sounds_len = len(sounds)


    def view(self) -> Iterable[Iterable[int]]:
        '''\
        'view' maskes representation of the mapping.
        '''

        for map_line in self._mapping:
            yield (_ for _ in map_line)


    def switch(self, sound_index: int, beat_index: int) -> None:
        '''\
        Turn on/off defined sound at defined beat.
        '''

        if 0 <= sound_index < self._sounds_len and 0 <= beat_index < self._sample_len:
            self._mapping[sound_index][beat_index] ^= 1

    def beat(self) -> Iterable:
        '''\
        'beat' yields all sounds that should be played
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
        Fill the mapping to the empty state.
        '''

        self._mapping.clear()
        self._mapping.extend(bytearray(self._sample_len) for _ in range(self._sounds_len))

    def resize(self, tact_l: int, tact_n: int) -> None:
        '''\
        Change:
            <*> The time signature. But only metre, because
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
    '''\
    Provide an abstraction to make Player independent
    of sounds.
    '''

    def __init__(self, sound_obj: object) -> None:
        '''\
        The AbstractSound (and sub-type) object is a
        facade of 'sound_obj'.
        '''

        pass

    def play(self) -> None:
        '''\
        Play using sound_obj.
        '''

        pass

    def stop(self) -> None:
        '''\
        Stop playing of sound_obj.
        '''

        pass

    def set_volume(self, volume: float) -> None:
        '''\
        Set the volume of sound object.
        '''

        pass

    def source(self) -> str:
        '''\
        Return the source path of the sound_obj.
        '''

        return ''


class AbstractLoader():
    '''\
    Provide an abstraction to make player
    independent of sound loading process.

    Implement callback setters.
    '''

    def __init__(self) -> None:
        '''\
        '_install_sound' and '_draw_sound' is callbacks
        to the player and ui.
        '''

        self._install_sound = id
        self._draw_sound = print

    def load_sound(self, sound_path: str) -> None:
        '''\
        Method that load sound and use callbacks
        after the successful loading.
        '''

        pass

    def set_installer(self, installer: Callable) -> None:
        '''\
        Set callback that will be used by player.
        '''

        self._install_sound = installer

    def set_drawer(self, drawer: Callable) -> None:
        '''\
        Set callback that will be used by ui.
        '''

        self._draw_sound = drawer


class AbstractSoundLoaderClient():
    '''\
    Controller that install the loader to the player and
    make facade for it.
    '''

    def __init_subclass__(cls, /, loader: type = AbstractLoader, **kwargs) -> None:
        '''\
        Store common implementation for instances of the 'cls'.
        '''

        cls.__loader = loader
        super().__init_subclass__(**kwargs)

    def _init_loader(self) -> None:
        '''\
        Init loader for the instance.
        '''

        self._loader = type(self).__loader()
        self._loader.set_installer(self._install_sound)
        self._loader.set_drawer(print)

    def add_sound(self, sound_path: str) -> None:
        '''\
        Implement interface for a ui.
        '''

        self._loader.load_sound(sound_path)

    def set_draw_sound_callback(self, callback: Callable) -> None:
        '''\
        Implement interface for a ui.
        '''

        self._loader.set_drawer(callback)

    def _install_sound(self, sound: AbstractSound) -> None:
        '''\
        Should be implemented in a player to make adding of sounds.
        '''

        pass


class AbstractSampleClient():
    '''\
    Controller that install the sample to the player and
    make facade for it.
    '''

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

    def view(self) -> Iterable[Iterable[int]]:
        '''\
        Facade for the Sample.
        '''

        yield from self._sample.view()

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
