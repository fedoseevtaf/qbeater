from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QPushButton, QLabel
)


class ColoredButton(QPushButton):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self._set_default_color()
        self.state = True
        self.clicked.connect(self._change_color)

    def _change_color(self) -> None:
        if self.state:
            self.setStyleSheet('background-color: #fe7c00')
        else:
            self._set_default_color()
        self.state = not self.state

    def _set_default_color(self) -> None:
        self.setStyleSheet('background-color: #00b4ab')