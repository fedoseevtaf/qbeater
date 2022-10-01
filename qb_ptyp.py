from sys import argv

from PyQt5.QtWidgets import QApplication, QMainWindow

from qb_player import Player
from qb_ui import SoundLine


player = Player((5, 4), 200, 4)
player.add('2.wav')


class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('MVP')
        self.setMinimumSize(1000, 40)

        self.line = SoundLine(self, tact_l=5, tact_n=4)
        self.line.setGeometry(0, 0, 1000, 40)
        self.line.set_title('a')

        self.btns = dict()
        for i in range(20):
            btn = self.line.getbtn(i)
            self.btns[id(btn)] = i
            btn.clicked.connect(self._switch_click)

        player.turn_on()

    def _switch_click(self) -> None:
        btn_id = id(self.sender())
        player.switch(0, self.btns[btn_id])


app = QApplication(argv)
window = Window()
window.show()
app.exec()
