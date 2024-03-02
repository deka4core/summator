from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QLabel, QGraphicsOpacityEffect
from summator import summator, number_to_decimal
from constants import *

import database


class MainWindow(QMainWindow):
    def __init__(self):
        """ Инициализация класса окна приложения"""
        super().__init__()
        self.setFixedSize(WINDOW_WSIZE, WINDOW_HSIZE)  # Фиксированное окно
        self.setStyleSheet(open("resources/summator_ui.css").read())  # Подключение UI-css файла

        """ Настройка основного виджета"""
        widget = QWidget()
        self.setObjectName("CentralWidget")
        self.setCentralWidget(widget)

        """ Инициализация эл-тов интерфейса(кнопок и текста) """
        self.labels, self.buttons = [], []  # Матрица элементов интерфейса
        for i in range(3):
            self.buttons.append(list())
            self.labels.append(QLabel("0", self))

            labels_opacity = QGraphicsOpacityEffect()
            labels_opacity.setOpacity(LCD_LABEL_OPACITY)  # Непрозрачность LCD-текста
            self.labels[i].setGraphicsEffect(labels_opacity)

            if i < 2:
                self.labels[i].setGeometry(LGROUP_LEFT_MARGIN + (i * LABEL_LEFT_MARGIN), LGROUP_TOP_MARGIN, LABEL_WSIZE,
                                           LABEL_HSIZE)
            else:
                self.labels[i].setGeometry(LGROUP_LEFT_MARGIN - 10, LGROUP_TOP_MARGIN + 425, LABEL_WSIZE, LABEL_HSIZE)

            for j in range(BITNESS):
                self.buttons[i].append(QPushButton(self))
                self.buttons[i][j].setGeometry(BGROUP_LEFT_MARGIN + (j * BUTTON_LEFT_MARGIN + BUTTON_WSIZE),
                                               BGROUP_TOP_MARGIN + (i * BUTTON_TOP_MARGIN), BUTTON_WSIZE, BUTTON_HSIZE)
                if i <= 1:
                    self.buttons[i][j].setCheckable(True)  # Два ряда кнопок можно прожать
                    self.buttons[i][j].clicked.connect(self.change_button_image)

    def change_button_image(self):
        """ QEvent на нажатие по первым двум рядам кнопок.
            Изменяет изображение на кнопке, а так же обновляет результаты вычислений.
        """
        sender: QPushButton = self.sender()  # Хранение объекта, вызвавшего метод.

        """ Обновление значений в БД """
        if sender in self.buttons[0]:
            index = self.buttons[0].index(sender)
            database.first_numbers[index] = sender.isChecked()
        elif sender in self.buttons[1]:
            index = self.buttons[1].index(sender)
            database.second_numbers[index] = sender.isChecked()

        """ Вычисление результата и отображение на экране """
        database.third_numbers = summator(database.first_numbers, database.second_numbers)
        for i in range(BITNESS):
            self.buttons[2][i].setStyleSheet('QPushButton {background-image:url(' +
                                             f"resources/button_{database.third_numbers[i]}.png" + ');}')

        output_numbers = list(map(lambda x: number_to_decimal(x), [database.first_numbers,
                                                                   database.second_numbers,
                                                                   database.third_numbers]))
        for i in range(3):
            self.labels[i].setText(str(output_numbers[i]))
