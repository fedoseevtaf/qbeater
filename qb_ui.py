from typing import Iterator

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QPushButton, QLabel, QSpinBox, QSlider, QLineEdit
)


class ColoredButton(QPushButton):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.state = False
        self.clicked.connect(self._change_color)

        self._default = 'background-color: #aab4ab'
        self._clicked = 'background-color: #fe7c00'
        self._set_color()

    def reset(self) -> None:
        self.state = False
        self._set_color()

    def _set_color(self) -> None:
        if self.state:
            self.setStyleSheet(self._clicked)
        else:
            self.setStyleSheet(self._default)

    def _change_color(self) -> None:
        self.state = not self.state
        self._set_color()

    def set_uniq(self) -> None:
        '''\
        On uncommon colors to make button different.
        '''

        self._default = 'background-color: #ffb4ab'
        self._clicked = 'background-color: #fe7cff'
        self._set_color()


class SoundHeader(QWidget):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.label = QLineEdit(self)
        self.label.setGeometry(0, 0, 100, 20)
        self.btn = QPushButton(self)
        self.btn.setText('remove')
        self.btn.setGeometry(100, 0, 100, 20)

        self.delbtn = self.btn

    def set_title(self, title: str) -> None:
        self.label.setText(title)


class SoundLine(QWidget):

    def __init__(self, *args, tact_l: int, tact_n: int) -> None:
        super().__init__(*args)
        self.layout = QGridLayout(self)

        self.header = SoundHeader()
        self.delbtn = self.header.delbtn
        self.layout.addWidget(self.header, 0, 0)
        self.layout.setColumnMinimumWidth(0, 200)

        self.btns = list()
        for i in range(tact_l * tact_n):
            btn = ColoredButton()
            if not i % tact_l:
                btn.set_uniq()
            self.btns.append(btn)
            self.layout.addWidget(btn, 0, i + 1)
            self.layout.setColumnStretch(i + 1, 1)

    def __iter__(self) -> Iterator:
        return iter(self.btns)

    def clear(self) -> None:
        for btn in self.btns:
            btn.reset()

    def set_title(self, title: str) -> None:
        self.header.set_title(title)

    def getbtn(self, i: int) -> ColoredButton:
        return self.btns[i]

    def findbtn(self, btn: QPushButton) -> int:
        return self.layout.indexOf(btn)


class OptionsLine(QWidget):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setMinimumSize(380, 40)

        self.play_btn = QPushButton(self)
        self.play_btn.setGeometry(0, 0, 40, 40)
        self.play_btn.setIcon(QIcon('icons/play_btn_icon.png'))

        self.stop_btn = QPushButton(self)
        self.stop_btn.setGeometry(40, 0, 40, 40)
        self.stop_btn.setIcon(QIcon('icons/stop_btn_icon.png'))

        self.sound_path = QLineEdit(self)
        self.sound_path.setGeometry(80, 20, 100, 20)
        self.add_sound = QPushButton('Add sound', self)
        self.add_sound.setGeometry(80, 0, 100, 20)

        self._bpm_label = QLabel('BPM:', self)
        self._bpm_label.setAlignment(Qt.AlignHCenter)
        self._bpm_label.setGeometry(180, 20, 40, 20)
        self.bpm_value = QSpinBox(self)
        self.bpm_value.setRange(10, 210)
        self.bpm_value.setValue(90)
        self.bpm_value.setGeometry(220, 20, 60, 20)

        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setGeometry(180, 0, 50, 20)

        self.conf_btn = QPushButton('Config', self)
        self.conf_btn.setGeometry(230, 00, 50, 20)

        self._volume_label = QLabel('Volume:', self)
        self._volume_label.setAlignment(Qt.AlignHCenter)
        self._volume_label.setGeometry(280, 0, 100, 20)

        self.volume_value = QSlider(self)
        self.volume_value.setOrientation(Qt.Horizontal)
        self.volume_value.setRange(0, 100)
        self.volume_value.setValue(50)
        self.volume_value.setGeometry(280, 20, 100, 20)
