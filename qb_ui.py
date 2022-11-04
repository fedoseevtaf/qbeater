'''\
qb_ui provide ui templates.
'''


from typing import Iterator

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QDialog,
    QPushButton, QLabel, QSpinBox, QSlider, QLineEdit, QComboBox
)


class ConfigWindow(QDialog):
    '''\
    Used to set time signature and number of tacts.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.setModal(True)
        self.setWindowTitle('config')
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setFixedSize(300, 60)

        self._metre = QLabel(' Metre', self)
        self._metre.setGeometry(0, 0, 100, 30)
        self.metre = QSpinBox(self)
        self.metre.setGeometry(100, 5, 50, 20)
        self.metre.setRange(2, 7)

        self._length = QLabel(' Length', self)
        self._length.setGeometry(0, 30, 100, 30)
        self.length = QComboBox(self)
        for i in range(1, 6):
            self.length.addItem(str(2 ** i))
        self.length.setGeometry(100, 35, 50, 20)

        self._tacts = QLabel(' Tacts', self)
        self._tacts.setGeometry(150, 0, 100, 30)
        self.tacts = QSpinBox(self)
        self.tacts.setGeometry(250, 5, 50, 20)
        self.tacts.setRange(2, 5)

        self.ok_btn = QPushButton('OK', self)
        self.ok_btn.setGeometry(250, 31, 50, 28)


class ColoredButton(QPushButton):
    '''\
    Implement color policy of the button.
    '''

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.state = False
        self.clicked.connect(self.change_color)

        self._default = 'background-color: #aab4ab'
        self._clicked = 'background-color: #fe7c00'
        self._set_color()

    def reset(self) -> None:
        '''\
        Set to default color.
        '''

        self.state = False
        self._set_color()

    def _set_color(self) -> None:
        if self.state:
            self.setStyleSheet(self._clicked)
        else:
            self.setStyleSheet(self._default)

    def change_color(self) -> None:
        '''\
        Switch button color, 'change_color' is used on click.
        '''

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
    '''\
    Store sound title and remove button.
    '''

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.label = QLineEdit(self)
        self.label.setGeometry(0, 0, 100, 20)
        self.btn = QPushButton(self)
        self.btn.setText('remove')
        self.btn.setGeometry(100, 0, 100, 20)

        self.delbtn = self.btn

    def set_title(self, title: str) -> None:
        '''\
        Change title, to preset for example.
        '''

        self.label.setText(title)


class SoundLine(QWidget):
    '''\
    Use layout to display beat buttons.
    '''

    def __init__(self, *args, tact_l: int, tact_n: int) -> None:
        super().__init__(*args)
        self.layout = QGridLayout(self)

        self.header = SoundHeader()
        self.delbtn = self.header.delbtn
        self.layout.addWidget(self.header, 0, 0)
        self.layout.setColumnMinimumWidth(0, 200)

        self.btns = []
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
        '''\
        'Off' all buttons.
        '''

        for btn in self.btns:
            btn.reset()

    def set_title(self, title: str) -> None:
        '''\
        Facade of SoundHeader.
        '''
        self.header.set_title(title)

    def getbtn(self, i: int) -> ColoredButton:
        '''\
        'getbtn' is used to bind click.
        '''

        return self.btns[i]

    def findbtn(self, btn: QPushButton) -> int:
        '''\
        'getbtn' is used to bind click.
        '''

        return self.layout.indexOf(btn)


class OptionsLine(QWidget):
    '''\
    Store all control buttons and fields.
    '''

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setMinimumSize(380, 70)

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
        self._volume_label.setGeometry(480, 0, 100, 20)

        self.volume_value = QSlider(self)
        self.volume_value.setOrientation(Qt.Horizontal)
        self.volume_value.setRange(0, 100)
        self.volume_value.setValue(50)
        self.volume_value.setGeometry(480, 20, 100, 20)

        self.pjload_path = QLineEdit(self)
        self.pjload_path.setGeometry(280, 20, 100, 20)
        self.pjload = QPushButton('Load project', self)
        self.pjload.setGeometry(280, 0, 100, 20)

        self.pjstore_path = QLineEdit(self)
        self.pjstore_path.setGeometry(380, 20, 100, 20)
        self.pjstore = QPushButton('Store project', self)
        self.pjstore.setGeometry(380, 0, 100, 20)

        self.notification_line = QLabel('Welcome, thank you for using our software!', self)
        self.notification_line.setAlignment(Qt.AlignHCenter)
        self.notification_line.setGeometry(0, 50, 580, 20)
