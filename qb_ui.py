from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QPushButton, QLabel, QSpinBox, QSlider, QLineEdit
)


class ColoredButton(QPushButton):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.state = False
        self.clicked.connect(self._change_color)

        self._default = 'background-color: #00b4ab'
        self._clicked = 'background-color: #fe7c00'
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
        self.label = QLabel(self)
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

    def set_title(self, title: str) -> None:
        self.header.set_title(title)

    def getbtn(self, i: int) -> ColoredButton:
        return self.btns[i]


class OptionsLine(QWidget):

    def __init__(self, *args) -> None:
        super().__init__(*args)

        self.sound_title = QLineEdit(self)
        self.sound_title.setGeometry(0, 0, 100, 20)
        self.add_sound = QPushButton('Add sound', self)
        self.add_sound.setGeometry(100, 0, 100, 20)

        self._bpm_label = QLabel('BPM:', self)
        self._bpm_label.setGeometry(200, 0, 40, 20)
        self.bpm_value = QSpinBox(self)
        self.bpm_value.setRange(10, 210)
        self.bpm_value.setValue(90)
        self.bpm_value.setGeometry(240, 0, 60, 20)

        self.clearbtn = QPushButton('Clear', self)
        self.clearbtn.setGeometry(300, 0, 50, 20)

        self.confbtn = QPushButton('Config', self)
        self.confbtn.setGeometry(350, 0, 50, 20)

        self.volume_value = QSlider(self)
        self.volume_value.setOrientation(Qt.Horizontal)
        self.volume_value.setRange(0, 100)
        self.volume_value.setValue(50)
        self.volume_value.setGeometry(400, 0, 100, 20)
