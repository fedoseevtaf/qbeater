'''\
qb_storage implement qb_abs_storage stuff.
'''


from qb_abs_storage import AbstractStorage
from qb_core import AbstractSound, Sample


class Storage(AbstractStorage):
    '''\
    Implement storage interface.
    '''

    def upload(self, path: str) -> None:
        '''\
        Load project from the 'path'.
        '''

    def unload(self, path: str, view: Sample, sounds: list[AbstractSound]) -> None:
        '''\
        Save project to the 'path'.
        '''
