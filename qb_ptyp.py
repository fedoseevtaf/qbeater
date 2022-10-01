from sys import argv

from PyQt5.QtWidgets import QApplication

from qb_ui import ColoredButton, SoundHeader, SoundLine, OptionsLine


app = QApplication(argv)
line = OptionsLine()
line.show()
app.exec()
