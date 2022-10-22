from sys import argv

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout
)

import qb_player as qb
import qb_ui as ui


class DrumMachine_WindowComposer(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('qbeater')
        try:
            self.setWindowIcon(QIcon('icon.png'))
        except:
            pass #  Without icon
        self.setMinimumWidth(550)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.options = ui.OptionsLine()
        self.layout.addWidget(self.options)

        # Sound line id: sound line
        self._sound_lines_book = dict()
        # Button id: sound line id
        self._del_btns_book = dict()

        # Button id: sound line id
        self._sound_btns_book = dict()
        # Sound line id: set(sound button id)
        self._sound_btns_by_lines_book = dict()

        self._add_sound_line('q', 3, 4)
        self._add_sound_line('q', 3, 4)
        self._add_sound_line('q', 3, 4)

    def _clear(self) -> None:
        for sound_line_id in frozenset(self._sound_lines_book):
            self._del_sound_line(sound_line_id)

    def _hide_sound_lines(self) -> None:
        for sound_line in self._sound_lines_book.values():
            sound_line.hide()

    def _add_sound_line(self, title: str, tact_l: int, tact_n: int) -> None:
        sound_line = ui.SoundLine(tact_l=tact_l, tact_n=tact_n)
        sound_line.set_title(title)
        self.layout.addWidget(sound_line, 1)
        sound_line_id = id(sound_line)
        self._sound_lines_book[sound_line_id] = sound_line
        self._book_sound_line_btns(sound_line_id)

        self.layout.addWidget(sound_line, 1)
        self._del_btns_book[id(sound_line.delbtn)] = sound_line_id
        sound_line.delbtn.clicked.connect(self._del_sound_line_slot)

    def _book_sound_line_btns(self, sound_line_id: int) -> None:
        sound_line = self._sound_lines_book[sound_line_id]
        self._sound_btns_by_lines_book[sound_line_id] = set()
        for btn in sound_line:
            btn.clicked.connect(self._sound_btn_clicked_slot)
            btn_id = id(btn)
            self._sound_btns_book[btn_id] = sound_line_id
            self._sound_btns_by_lines_book[sound_line_id].add(btn_id)


    def _del_sound_line_slot(self) -> int:
        delbtn = self.sender()
        sound_line_id = self._del_btns_book[id(delbtn)]
        sound_line = self._sound_lines_book[sound_line_id]
        index_of_sound_line = self.layout.indexOf(sound_line)

        self._del_sound_line(sound_line_id)
        return index_of_sound_line - 1

    def _del_sound_line(self, sound_line_id: int) -> None:
        sound_line = self._sound_lines_book[sound_line_id]
        self.layout.removeWidget(sound_line)
        sound_line.hide()
        self._unbook_sound_line(sound_line_id)

    def _unbook_sound_line(self, sound_line_id) -> None:
        for btn_id in self._sound_btns_by_lines_book[sound_line_id]:
            del self._sound_btns_book[btn_id]
        del self._sound_btns_by_lines_book[sound_line_id]
        delbtn = self._sound_lines_book[sound_line_id].delbtn
        delbtn_id = id(delbtn)
        del self._del_btns_book[delbtn_id]
        del self._sound_lines_book[sound_line_id]

    def _sound_btn_clicked_slot(self) -> tuple[int]:
        btn = self.sender()
        btn_id = id(btn)
        sound_line_id = self._sound_btns_book[btn_id]
        sound_line = self._sound_lines_book[sound_line_id]

        sound_line_index = self.layout.indexOf(sound_line)
        sound_btn_index = sound_line.findbtn(btn)
        return sound_line_index - 1, sound_btn_index - 1


class DrumMachine(DrumMachine_WindowComposer):

    def __init__(self):
        super().__init__()
        self._load_basic_preset()

    def _del_sound_line_slot(self) -> None:
        sound_line_index = super()._del_sound_line_slot()

    def _sound_btn_clicked_slot(self) -> None:
        sound_line_index, sound_btn_index = super()._sound_btn_clicked_slot()

    def _load_basic_preset(self) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(argv)
    machine = DrumMachine()
    machine.show()
    exit(app.exec())
