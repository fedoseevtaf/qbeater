'''\
'qbeater' is a main program.
'''


import sys
from typing import Tuple

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout
)

from qb_abs_storage import AbstractSound
import qb_player as qb
import qb_ui as ui


class DrumMachineWindowComposer(QWidget):
    '''\
    Controll widget's position.
    '''

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('qbeater')
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setMinimumWidth(700)

        self.cf_window = None

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.options = ui.OptionsLine()
        self.layout.addWidget(self.options)

        # Sound line id: sound line
        self._sound_lines_book = {}
        # Button id: sound line id
        self._del_btns_book = {}

        # Button id: sound line id
        self._sound_btns_book = {}
        # Sound line id: set(sound button id)
        self._sound_btns_by_lines_book = {}

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

    def _unbook_sound_line(self, sound_line_id: int) -> None:
        for btn_id in self._sound_btns_by_lines_book[sound_line_id]:
            del self._sound_btns_book[btn_id]
        del self._sound_btns_by_lines_book[sound_line_id]
        delbtn = self._sound_lines_book[sound_line_id].delbtn
        delbtn_id = id(delbtn)
        del self._del_btns_book[delbtn_id]
        del self._sound_lines_book[sound_line_id]

    def _sound_btn_clicked_slot(self) -> Tuple[int]:
        btn = self.sender()
        btn_id = id(btn)
        sound_line_id = self._sound_btns_book[btn_id]
        sound_line = self._sound_lines_book[sound_line_id]

        sound_line_index = self.layout.indexOf(sound_line)
        sound_btn_index = sound_line.findbtn(btn)
        return sound_line_index - 1, sound_btn_index - 1


class DrumMachine(DrumMachineWindowComposer):
    '''\
    Main App use DrumMachineWindowComposer to make ui for Player.
    '''

    def __init__(self):
        super().__init__()
        self.player = qb.Player()
        self._load_basic_sounds()
        self._set_volume()
        self._set_bpm()

        self.options.add_sound.clicked.connect(self._add_sound_clicked)
        self.player.set_draw_sound_callback(self._display_new_sound)
        self.player.set_redraw_mapping_callback(self._redraw_mapping)
        self.player.set_notification_callback(self.options.notification_line.setText)

        self.options.play_btn.clicked.connect(self._play_clicked)
        self.options.stop_btn.clicked.connect(self._stop_clicked)

        self.options.volume_value.valueChanged.connect(self._set_volume)
        self.options.bpm_value.valueChanged.connect(self._set_bpm)
        self.options.clear_btn.clicked.connect(self._clear)

        self.options.conf_btn.clicked.connect(self._make_config_window)
        self.options.pjload.clicked.connect(self._pjload_clicked)
        self.options.pjstore.clicked.connect(self._pjstore_clicked)

    def _redraw_mapping(self) -> None:
        for mapping_line, sound_line in zip(self.player.view(),
                                            self._sound_lines_book.values()):
            for flag, btn in zip(mapping_line, sound_line):
                btn.reset()
                if flag:
                    btn.change_color()

    def _pjload_clicked(self) -> None:
        pjpath = self.options.pjload_path.text()
        self.player.load_pj(pjpath)

    def _pjstore_clicked(self) -> None:
        pjpath = self.options.pjstore_path.text()
        self.player.store_pj(pjpath)

    def _make_config_window(self) -> None:
        self.cf_window = ui.ConfigWindow()
        self.player.turn_off()
        self.cf_window.show()
        self.cf_window.ok_btn.clicked.connect(self._reconfig)

    def _reconfig(self) -> None:
        time_sign = (self.cf_window.metre.value(), int(self.cf_window.length.currentText()))
        tact_n = self.cf_window.tacts.value()
        self.player.resize(time_sign, tact_n)
        self._redraw_lines()
        self.cf_window.hide()
        del self.cf_window

    def _clear_field(self) -> None:
        titles = list('' for _ in range(len(self._sound_lines_book)))
        for line_index in range(len(self._sound_lines_book)):
            sound_line = self.layout.itemAt(1).widget()
            line_id = id(sound_line)
            titles[line_index] = sound_line.header.label.text()
            self._del_sound_line(line_id)
        return titles

    def _redraw_lines(self) -> None:
        titles = self._clear_field()
        for title in titles:
            self._add_sound_line(title, self.player.get_tact_l(), self.player.get_tact_n())

    def _clear(self) -> None:
        for sound_line in self._sound_lines_book.values():
            sound_line.clear()
        self.player.clear()

    def _set_bpm(self) -> None:
        bpm = self.options.bpm_value.value()
        self.player.set_bpm(bpm)

    def _set_volume(self) -> None:
        volume = self.options.volume_value.value() / 100
        self.player.set_volume(volume)

    def _play_clicked(self) -> None:
        self.player.turn_on()
        self.player.play()

    def _stop_clicked(self) -> None:
        self.player.turn_off()
        self.player.goto_start()

    def _add_sound_clicked(self) -> None:
        sound_path = self.options.sound_path.text()
        self.player.add_sound(sound_path)

    def _display_new_sound(self, sound: AbstractSound) -> None:
        self._add_sound_line(sound.source(), self.player.get_tact_l(), self.player.get_tact_n())

    def _del_sound_line_slot(self) -> None:
        sound_line_index = super()._del_sound_line_slot()
        self.player.rem_sound(sound_line_index)

    def _sound_btn_clicked_slot(self) -> None:
        sound_line_index, sound_btn_index = super()._sound_btn_clicked_slot()
        self.player.switch(sound_line_index, sound_btn_index)

    def _load_basic_sounds(self) -> None:
        self.player.load_pj('basic.qbp')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    machine = DrumMachine()
    machine.show()
    sys.exit(app.exec())
