from PyQt6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from summator import summator, number_to_decimal
from constants import BUTTON_HSIZE, BUTTON_WSIZE, WINDOW_HSIZE, WINDOW_WSIZE

import database


class MainWindow(QMainWindow):
    def __init__(self):
        """ Инициализация класса окна приложения"""
        super().__init__()
        self.resize(WINDOW_WSIZE, WINDOW_HSIZE)

        """ Настройка Layout """
        self.gridlayout = QGridLayout(self)
        self.gridlayout.setHorizontalSpacing(20)

        widget = QWidget()
        widget.setLayout(self.gridlayout)
        self.setCentralWidget(widget)

        """ Инициализация эл-тов интерфейса(кнопок и текста) """
        self.labels, self.buttons = [], []
        for i in range(3):
            self.buttons.append(list())
            self.labels.append(QLabel("0", self))
            self.gridlayout.addWidget(self.labels[i], i, 8)
            for j in range(8):
                self.buttons[i].append(QPushButton("0", self))
                self.buttons[i][j].setMaximumSize(BUTTON_WSIZE, BUTTON_HSIZE)
                if i <= 1:
                    self.buttons[i][j].setCheckable(True)
                    self.buttons[i][j].clicked.connect(self.change_button_text)
                else:
                    self.buttons[i][j].setFlat(True)
                self.gridlayout.addWidget(self.buttons[i][j], i, j)

    def change_button_text(self):
        # noinspection PyTypeChecker
        sender: QPushButton = self.sender()

        sender.setText("1") if sender.text() == "0" else sender.setText("0")
        if sender in self.buttons[0]:
            index = self.buttons[0].index(sender)
            database.first_numbers[index] = int(sender.text())
        elif sender in self.buttons[1]:
            index = self.buttons[1].index(sender)
            database.second_numbers[index] = int(sender.text())

        database.third_numbers = summator(database.first_numbers, database.second_numbers)
        for i in range(8):
            self.buttons[2][i].setText(str(database.third_numbers[i]))
        output_numbers = list(map(lambda x: number_to_decimal(x), [database.first_numbers,
                                                                   database.second_numbers,
                                                                   database.third_numbers]))
        for i in range(3):
            self.labels[i].setText(str(output_numbers[i]))
