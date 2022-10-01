from sys import argv

from PyQt5.QtWidgets import QApplication

from qb_ui import ColoredButton


app = QApplication(argv)
btn = ColoredButton()
btn.show()
app.exec()
