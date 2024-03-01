import sys

from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication
from widgets import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont('resources/lcd.14.otf')  # Добавление шрифта в БД QT
    executable = MainWindow()
    executable.show()

    sys.exit(app.exec())
