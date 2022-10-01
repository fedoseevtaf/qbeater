from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QPushButton, QLabel
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
