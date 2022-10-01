from sys import argv

from PyQt5.QtWidgets import QApplication

from qb_ui import ColoredButton, SoundHeader, SoundLine


app = QApplication(argv)
line = SoundLine(tact_l = 3, tact_n = 4)
line.show()
line.delbtn.clicked.connect(lambda: line.set_title('title'))

def click():
    print(btns[id(line.sender())])

btns = dict()
for i in range(12):
    btn = line.getbtn(i)
    btn.clicked.connect(click)
    btns[id(btn)] = i

app.exec()
