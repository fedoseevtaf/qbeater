from sys import argv

from PyQt5.QtWidgets import QApplication

from qb_ui import ColoredButton, SoundHeader


app = QApplication(argv)
header = SoundHeader()
header.show()
header.click.connect(lambda: header.set_title('title'))
app.exec()
