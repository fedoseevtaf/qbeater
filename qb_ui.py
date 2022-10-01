from PyQt5.QtWidgets import (
    QWidget, QGridLayout,
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout
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


class SoundHeader(QWidget):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 100, 20)
        self.btn = QPushButton(self)
        self.btn.setText('remove')
        self.btn.setGeometry(100, 0, 100, 20)

        self.click = self.btn.clicked

    def set_title(self, title: str) -> None:
        self.label.setText(title)
