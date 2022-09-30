from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

from qb_player import Player


sounds = list(f'{i}.wav' for i in range(1, 4))


class Window(QMainWindow):

    def __init__(self, parent = None) -> None:
        super().__init__()

        self.player = Player((3, 2), 110, sounds)
        self.player.play()

        for index in range(0, 3 * 4):
            self.player.switch(0, index)

        for index in range(0, 3 * 4, 2):
            self.player.switch(1, index)

        self.player.switch(2, 0)
        self.player.switch(2, 1)
        self.player.switch(2, 3)

        self.player.switch(2, 6)
        self.player.switch(2, 7)
        self.player.switch(2, 9)

        self.btn = QPushButton(self)
        self.btn.clicked.connect(self.play)

    def play(self):
        self.player.reset()
        self.player.turn()


app = QApplication([])
window = Window()
window.show()
app.exec()
