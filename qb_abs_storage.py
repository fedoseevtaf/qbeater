'''\
'qb_abs_storage' provides abstractions to make saving projects.
'''


from typing import Callable, Iterable, List


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

    def play(self) -> None:
        '''\
        Play using sound_obj.
        '''

    def stop(self) -> None:
        '''\
        Stop playing of sound_obj.
        '''

    def set_volume(self, volume: float) -> None:
        '''\
        Set the volume of sound object.
        '''

    def source(self) -> str:
        '''\
        Return the source path of the sound_obj.
        '''

        return ''


class AbstractStorage():
    '''\
    Implement storage interface.
    Provide an abstraction to make player
    independent of sound loading process.

    Word about displaying policy:
    The player has no tools for displaying the sound mapping
    and providing ui. Therefor the player use
    '_draw_sound' to "notify" the ui that sound is
    successfully added.

    Implement callback setters.
    '''

    def __init__(self) -> None:
        self._install_sound = print
        self._draw_sound = print
        self._update_view = print

        self._display_notification = print

    def set_notification_callback(self, callback: Callable) -> None:
        '''\
        '_display_notification' is used to notify user about errors.
        '''

        self._display_notification = callback

    def set_install_sound_callback(self, callback: Callable) -> None:
        '''\
        '_install_sound' is used to add and config sound.
        '''

        self._install_sound = callback

    def set_draw_sound_callback(self, callback: Callable) -> None:
        '''\
        '_draw_sound' is used to display a sound representation.
        '''

        self._draw_sound = callback

    def set_update_view_callback(self, callback: Callable) -> None:
        '''\
        '_update_view' is used to display an actual sound mapping.
        '''

        self._update_view = callback

    def upload_project(self, pjpath: str) -> None:
        '''\
        Load project from the 'pjpath'.
        '''

    def unload_project(self, pjpath: str, mapping: Iterable[Iterable[int]],
                       sounds: List[AbstractSound]) -> None:
        '''\
        Save project to the 'pjpath'.
        '''

    def load_sound(self, sound_path: str, mapping: Iterable[int]) -> None:
        '''\
        Method that load sound and use callbacks
        after the successful loading.
        '''


class AbstractStorageClient():
    '''\
    Implement storage interface in player.
    '''

    def __init_subclass__(cls, storage: type = AbstractStorage, **kwargs) -> None:
        cls._storage = storage
        super().__init_subclass__(**kwargs)

    def __init__(self) -> None:
        self._storage = self._storage()
        self._storage.set_install_sound_callback(self._install_sound)
        super().__init__()

    def add_sound(self, sound_path: str) -> None:
        '''\
        Facade for the 'AbstractStorage.unload_project'.
        '''

        self._storage.load_sound(sound_path, b'')

    def set_notification_callback(self, callback: Callable) -> None:
        '''\
        Read about it in docs of AbstractStorage.
        '''

        self._storage.set_notification_callback(callback)

    def set_redraw_mapping_callback(self, callback: Callable) -> None:
        '''\
        Read about it in docs of AbstractStorage.
        '''

        self._storage.set_update_view_callback(callback)

    def set_draw_sound_callback(self, callback: Callable) -> None:
        '''\
        Read about it in docs of AbstractStorage.
        '''

        self._storage.set_draw_sound_callback(callback)

    def load_pj(self, path: str) -> None:
        '''\
        Facade for the 'AbstractStorage.unload_project'.
        '''

        self._storage.upload_project(path)

    def store_pj(self, path: str) -> None:
        '''\
        Facade for the 'AbstractStorage.upload_project'.
        '''

        self._storage.unload_project(path, *self._get_view())

    def _get_view(self) -> Iterable:
        '''\
        Should be implemented.
        '''

        return
        yield

    def _install_sound(self, sound: AbstractSound, mapping: Iterable[Iterable[int]]) -> Iterable:
        '''\
        Should be implemented.
        '''
