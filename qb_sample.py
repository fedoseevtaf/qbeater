from typing import Iterable


class Sample():

    def __init__(self, sounds: list, *args,
                 tact_l: int = 3, tact_n: int = 4) -> None:
        '''\
        'tact_l' - length of tact
        'tact_n' - number of tacts in sample

        Sample get lists of sounds and them titles, manage
        that list without any information about what sound is.

        'mapping' is used to remind what time (beat)
        what sound should be played.
        '''

        self.actual_beat_num = 0

        self.tact_l = tact_l
        self.tact_n = tact_n

        self._sample_len = tact_l * tact_n
        self._sounds_len = len(sounds)

        self.sounds = sounds
        self.mapping = list()

    def switch(self, sound_index: int, beat_index: int) -> None:
        '''\
        The 'switch' should be used to turn on/off
        defined sound at defined tact.
        '''
        if 0 <= sound_index < self._sounds_len and 0 <= beat_index < self._sample_len:
            self.mapping[sound_index][beat_index] ^= 1

    def beat(self) -> Iterable:
        '''\
        Yield all sounds that should play at that beat.
        '''

        for sound_index, sound in enumerate(self.sounds):
            if self.mapping[sound_index][self.actual_beat_num]:
                yield sound

        self.actual_beat_num += 1
        self.actual_beat_num %= self._sample_len

    def reset(self) -> None:
        self.actual_beat_num = 0

    def clear(self) -> None:
        self.mapping.clear()
        self.mapping.extend(bytearray(self._sample_len) for _ in range(self._sounds_len))

    def resize(self, tact_l: int, tact_n: int = None) -> None:
        '''\
        'resize' method shoud be used if you need to change:
            <*> The time signature. But only meter, because
                sample don't save note length.
            <*> The 'track' size (amount of tacts in the sample)

        With resizing all the sound sequence will be cleaned
        by the 'clear' method.
        '''

        self.tact_l = tact_l
        self.tact_n = tact_n

        self._sample_len = tact_l * tact_n
        self.clear()

    def append(self, sound: object) -> None:
        self.sounds.append(sound)
        self.mapping.append(bytearray(self._sample_len))
        self._sounds_len += 1

    def remove(self, sound_index: int) -> None:
        if 0 <= sound_index < self._sounds_len:
            del self.sounds[sound_index]
            del self.mapping[sound_index]
            self._sounds_len -= 1
