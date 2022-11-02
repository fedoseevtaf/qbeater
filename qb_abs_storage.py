'''\
'qb_abs_storage' provides abstractions to make saving projects.
'''


from typing import Callable

from qb_core import Sample, AbstractSound


class AbstractStorage():
    '''\
    Implement storage interface.
    '''

    def __init__(self) -> None:
        self._add_sound_callback = print
        self._switch_callback = print

    def set_add_sound_callback(self, func: Callable) -> None:
        '''\
        Set basic callback.
        '''

        self._add_sound_callback = func

    def set_switch_callback(self, func: Callable) -> None:
        '''\
        Set basic callback.
        '''

        self._switch_callback = func

    def upload(self, path: str) -> None:
        '''\
        Load project from the 'path'.
        '''

    def unload(self, path: str, view: Sample, sounds: list[AbstractSound]) -> None:
        '''\
        Save project to the 'path'.
        '''


class AbstractStorageClient():
    '''\
    Implement storage interface in player.
    '''

    def __init_subclass__(cls, storage: type = AbstractStorage) -> None:
        cls._storage = storage
        super().__init_subclass__()

    def __init__(self) -> None:
        self._storage = self._storage()
        self._storage.set_add_sound_callback(self.add_sound)
        self._storage.set_switch_callback(self._switch_interface_for_storage)
        super().__init__()

    def _switch_interface_for_storage(self, beat_index: int) -> None:
        '''\
        Make switch for storage independent by sound.
        '''

        self.switch(0, beat_index)

    def load_pj(self, path: str) -> None:
        '''\
        Facade for the 'AbstractStorage.unload'.
        '''

        self._storage.upload(path)

    def store_pj(self, path: str) -> None:
        '''\
        Facade for the 'AbstractStorage.upload'.
        '''

        self._storage.unload(path, self._sample, self._sounds)
