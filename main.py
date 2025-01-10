from PySide6.QtWidgets import QApplication
import sys
from dashboard import Dashboard
from auth import Auth

app = QApplication(sys.argv)
window = Auth()
window.show()

with open("styles.css", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

app.exec()

