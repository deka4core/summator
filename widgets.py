from PyQt5.QtCore import QObject
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

        self.labels, self.buttons = [], []  # Матрица элементов интерфейса
        self.initialize_buttons_and_labels()

    def update_event(self):
        """ QEvent на нажатие по первым двум рядам кнопок.
            Изменяет изображение на кнопке, а так же обновляет результаты вычислений.
        """
        sender: QObject = self.sender()  # Хранение объекта, вызвавшего метод.
        self.update_database_data(sender)
        self.display_result()

    def update_database_data(self, obj: QObject):
        """ Обновление значений в БД.
        :param obj: Источник сигнала.
        """
        if obj in self.buttons[0]:
            index = self.buttons[0].index(obj)
            database.first_numbers[index] = obj.isChecked()
        elif obj in self.buttons[1]:
            index = self.buttons[1].index(obj)
            database.second_numbers[index] = obj.isChecked()

    @staticmethod
    def calculate_numbers() -> list:
        """ Вычисление результата
        :return list: Список из трех десятичных чисел
        """
        database.third_numbers = summator(database.first_numbers, database.second_numbers)
        return list(map(lambda x: number_to_decimal(x), [database.first_numbers,
                                                         database.second_numbers,
                                                         database.third_numbers]))

    def initialize_buttons_and_labels(self):
        """ Инициализация эл-тов интерфейса(кнопок и текста) """
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
                    self.buttons[i][j].clicked.connect(self.update_event)

    def display_result(self):
        """ Вычисление результата и отображение на экране """
        output_numbers = self.calculate_numbers()
        if not (-128 <= sum(output_numbers[:2]) <= 127):
            for i in range(BITNESS):
                self.buttons[2][i].setStyleSheet('QPushButton {background-image:url(resources/button_0.png);}')
            for i in range(2):
                self.labels[i].setText(str(output_numbers[i]))
            self.labels[2].setText(str('Error'))
        else:
            for i in range(BITNESS):
                self.buttons[2][i].setStyleSheet('QPushButton {background-image:url(' +
                                                 f"resources/button_{database.third_numbers[i]}.png" + ');}')
            for i in range(3):
                self.labels[i].setText(str(output_numbers[i]))
