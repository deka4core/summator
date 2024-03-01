from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel
from summator import summator, number_to_decimal
from constants import BUTTON_HSIZE, BUTTON_WSIZE, WINDOW_HSIZE, WINDOW_WSIZE, BITNESS, BGROUP_LEFT_MARGIN, \
    BGROUP_TOP_MARGIN, BUTTON_LEFT_MARGIN, BUTTON_TOP_MARGIN, LGROUP_LEFT_MARGIN, LGROUP_TOP_MARGIN, \
    LABEL_LEFT_MARGIN, LABEL_HSIZE, LABEL_WSIZE

import database


class MainWindow(QMainWindow):
    def __init__(self):
        """ Инициализация класса окна приложения"""
        super().__init__()
        self.setFixedSize(WINDOW_WSIZE, WINDOW_HSIZE)
        self.setStyleSheet(open("resources/summator_ui.css").read())

        """ Настройка основного виджета"""
        widget = QWidget()
        self.setObjectName("CentralWidget")
        self.setCentralWidget(widget)

        """ Инициализация эл-тов интерфейса(кнопок и текста) """
        self.labels, self.buttons = [], []
        for i in range(3):
            self.buttons.append(list())
            self.labels.append(QLabel("0", self))
            self.labels[i].setGeometry(LGROUP_LEFT_MARGIN + (i * LABEL_LEFT_MARGIN), LGROUP_TOP_MARGIN, LABEL_WSIZE,
                                       LABEL_HSIZE)
            for j in range(BITNESS):
                print(f"Button{i}{j} POS: {BGROUP_LEFT_MARGIN + (j * BUTTON_LEFT_MARGIN + BUTTON_WSIZE)}, "
                      f"{BGROUP_TOP_MARGIN + (i * BUTTON_TOP_MARGIN)} SIZE: {BUTTON_WSIZE, BUTTON_HSIZE}")
                self.buttons[i].append(QPushButton(self))
                self.buttons[i][j].setGeometry(BGROUP_LEFT_MARGIN + (j * BUTTON_LEFT_MARGIN + BUTTON_WSIZE),
                                               BGROUP_TOP_MARGIN + (i * BUTTON_TOP_MARGIN), BUTTON_WSIZE, BUTTON_HSIZE)
                self.buttons[i][j].setCheckable(True)
                if i <= 1:
                    self.buttons[i][j].clicked.connect(self.change_button_image)

    def change_button_image(self):
        """ QEvent на нажатие по первым двум рядам кнопок
            Изменяет значения на кнопке, а так же обновляет результаты вычислений
        """
        # noinspection PyTypeChecker
        sender: QPushButton = self.sender()

        """ Обработка QEvent на QPushButton """
        if sender in self.buttons[0]:
            index = self.buttons[0].index(sender)
            database.first_numbers[index] = sender.isChecked()
        elif sender in self.buttons[1]:
            index = self.buttons[1].index(sender)
            database.second_numbers[index] = sender.isChecked()

        """ Вычисление результата и отображение на экране """
        database.third_numbers = summator(database.first_numbers, database.second_numbers)
        for i in range(BITNESS):
            self.buttons[2][i].setChecked(database.third_numbers[i])
        output_numbers = list(map(lambda x: number_to_decimal(x), [database.first_numbers,
                                                                   database.second_numbers,
                                                                   database.third_numbers]))
        for i in range(3):
            self.labels[i].setText(str(output_numbers[i]))
