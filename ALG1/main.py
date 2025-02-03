import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import calc as c

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Интерполяционные полиномы Ньютона и Эрмита")

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

        self.first_table = QtWidgets.QTableWidget(self)
        self.first_table.setFont(QtGui.QFont("Times", 9))
        self.first_table.setColumnCount(4)
        self.first_table.setHorizontalHeaderLabels(
            ["x", "y", "y'", "y''"])
        for i in range(5):
            self.first_table.insertRow(i)


        self.second_table = QtWidgets.QTableWidget(self)
        self.second_table.setFont(QtGui.QFont("Times", 9))
        self.second_table.setColumnCount(5)
        self.second_table.setHorizontalHeaderLabels(
            ["Степень", "y(x)(Ньютон)", "Корень(Ньютон)", "y(x)(Эрмит)", "Корень(Эрмит)"])

        self.info = QtWidgets.QLabel()
        self.info.setText("Программа для работы с интерполяционными многочленами Ньютона и Эрмита\n")
        self.info.adjustSize()

        self.add_empty_fir = QtWidgets.QPushButton()
        self.add_empty_fir.setFixedWidth(400)
        self.add_empty_fir.setText("Добавить пустую строку")
        self.add_empty_fir.clicked.connect(self.add_fir)
        self.add_empty_fir.setFont(QtGui.QFont("Times", 9))


        self.clear_fir = QtWidgets.QPushButton()
        self.clear_fir.setFixedWidth(400)
        self.clear_fir.setText("Очистить входную таблицу")
        self.clear_fir.clicked.connect(lambda: self.clear_all(1))
        self.clear_fir.setFont(QtGui.QFont("Times", 9))


        self.main_process_btn = QtWidgets.QPushButton()
        self.main_process_btn.setFixedWidth(400)
        self.main_process_btn.setText("Рассчитать y(x) для степеней от 0 до 10")
        self.main_process_btn.clicked.connect(self.main_process)
        self.main_process_btn.setFont(QtGui.QFont("Times", 9))

        self.delete_fir_btn = QtWidgets.QPushButton()
        self.delete_fir_btn.setFixedWidth(400)
        self.delete_fir_btn.setText("Удалить выбранную строку")
        self.delete_fir_btn.clicked.connect(self.delete_first)
        self.delete_fir_btn.setFont(QtGui.QFont("Times", 9))

        self.file_input_btn = QtWidgets.QPushButton()
        self.file_input_btn.setFixedWidth(400)
        self.file_input_btn.setText("Ввести данные из файла")
        self.file_input_btn.clicked.connect(self.input)
        self.file_input_btn.setFont(QtGui.QFont("Times", 9))

        self.file_input_label = QtWidgets.QLabel()
        self.file_input_label.setText("Путь до файла: ")
        self.file_input_label.setFont(QtGui.QFont("Times", 9))

        self.file_input = QtWidgets.QLineEdit()
        self.file_input.setFont(QtGui.QFont("Times", 9))

        self.x_input_label = QtWidgets.QLabel()
        self.x_input_label.setText("Значение аргумента x: ")
        self.x_input_label.setFont(QtGui.QFont("Times", 9))

        self.x_input = QtWidgets.QLineEdit()
        self.x_input.setFont(QtGui.QFont("Times", 9))


        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 9))

        w = QtWidgets.QWidget()
        start = QtWidgets.QVBoxLayout()
        start.addWidget(self.info)
        l = QtWidgets.QGridLayout()
        w.setLayout(start)
        l.addWidget(self.file_input_label, 0, 0)
        l.addWidget(self.file_input, 1, 0)
        l.addWidget(self.file_input_btn, 2, 0)
        l.addWidget(self.x_input_label, 3, 0)
        l.addWidget(self.x_input, 4, 0)
        l.addWidget(self.add_empty_fir, 5, 0)
        l.addWidget(self.delete_fir_btn, 6, 0)
        l.addWidget(self.clear_fir, 7, 0)
        l.addWidget(self.first_table, 8, 0)
        l.addWidget(self.second_table, 9, 0)
        l.addWidget(self.main_process_btn, 10, 0)
        start.addLayout(l)
        self.setCentralWidget(w)

    def input(self):
        file_name = self.file_input.text()
        if not file_name:
            self.show_message("Введите путь до файла")
            return 1
        array = []
        rc = c.read_data(file_name, array)
        if rc == -1:
            self.show_message("Файла по заданному пути не существует")
            return 1
        elif rc == -2:
            self.show_message("Ошибка при чтении файла")
            return 1
        else:
            self.first_table.setRowCount(0)
            length = len(array)
            for i in range(length):
                self.first_table.insertRow(i)
                self.first_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(array[i][0])))
                self.first_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(array[i][1])))
                self.first_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(array[i][2])))
                self.first_table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(array[i][3])))


    # Функция проверки корректности введенных x, y, y', y''
    def check_line(self, i):
        try:
            x = self.first_table.item(i, 0)
            y = self.first_table.item(i, 1)
            y_der1 = self.first_table.item(i, 2)
            y_der2 = self.first_table.item(i, 3)
            if not x and not y and not y_der1 and not y_der2:
                return 2     # если строка пуста, не считаем ошибкой
            if not x or not y or not y_der1 or not y_der2:
                return 1     # если заполнены не все ячейки в строке
            if x and y and y_der1 and y_der1:
                x = float(x.text())
                y = float(y.text())
                y_der1 = float(y_der1.text())
                y_der2 = float(y_der2.text())
            return 0
        except ValueError:
            return -1
        except Exception:
            return -2

    # Функция добавляет пустую строку в таблицу
    def add_fir(self):
        row_pos = self.first_table.rowCount()
        self.first_table.insertRow(row_pos)

    # Функция вывода сообщения об ошибке
    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    # Функция очистки таблицы
    def clear_all(self, tabnum):
        if tabnum == 1:
            self.first_table.clearContents()

    # Функция подготовки данных для рассчета задачи
    def main_process(self):
        i = 0
        array = []
        for i in range (self.first_table.rowCount()):
            rc = self.check_line(i)
            if rc == 0:
                x = float(self.first_table.item(i, 0).text())
                y = float(self.first_table.item(i, 1).text())
                y_der1 = float(self.first_table.item(i, 2).text())
                y_der2 = float(self.first_table.item(i, 3).text())
                array.append([x, y, y_der1, y_der2])
            elif rc == 1:
                self.show_message(f"В строке {i + 1} входной таблицы заполнены не все ячейки")
                return 1
            elif rc == -1:
                self.show_message(f"Некорректные данные в строке {i + 1} входной таблицы")
                return 1
            elif rc == -2:
                self.show_message("Неизвестная ошибка")
                return 1
        if len(array) == 0:
            self.show_message("Входная таблица пуста")
            return 2
        array.sort(key=lambda el: el[0])
        x = float(self.x_input.text())
        self.second_table.setRowCount(0)
        inverted = c.invert_table(array)
        for i in range(11):
            # подсчет значения полинома i-й степени методом Ньютона
            self.second_table.insertRow(i)
            interval = c.find_optimal_newton(array, x, i)
            if not interval:
                self.second_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
                self.second_table.setItem(i, 1, QtWidgets.QTableWidgetItem("Ошибка"))
                self.second_table.resizeColumnsToContents()
            else:
                self.second_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
                self.second_table.setItem(i, 1, QtWidgets.QTableWidgetItem(f"{c.newton_alg(interval, x):10.8f}"))
                self.second_table.resizeColumnsToContents()
            # подсчет значения полинома i-й степени методом Эрмита
            interval = c.find_optimal_hermit(array, x, i)
            if not interval:
                self.second_table.setItem(i, 3, QtWidgets.QTableWidgetItem("Ошибка"))
                self.second_table.resizeColumnsToContents()
            else:
                self.second_table.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{c.hermit_alg(interval, x):10.8f}"))
                self.second_table.resizeColumnsToContents()
            print("am")
            # подсчет корня полиномом i-й степени методом Ньютона (обратная интерполяция)
            interval = c.find_optimal_newton(inverted, 0, i)
            '''print(f"newton {i}")
            print(interval)'''
            if not interval:
                self.second_table.setItem(i, 2, QtWidgets.QTableWidgetItem("Ошибка"))
                self.second_table.resizeColumnsToContents()
            else:
                self.second_table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{c.newton_alg(interval, 0):10.8f}"))
                self.second_table.resizeColumnsToContents()
            # подсчет корня полиномом i-й степени методом Эрмита (обратная интерполяция)
            interval = c.find_optimal_hermit(inverted, 0, i)
            '''print(f"hermit {i}")
            print(interval)'''
            if not interval:
                self.second_table.setItem(i, 4, QtWidgets.QTableWidgetItem("Ошибка"))
                self.second_table.resizeColumnsToContents()
            else:
                self.second_table.setItem(i, 4, QtWidgets.QTableWidgetItem(f"{c.hermit_alg(interval, 0):10.8f}"))
                self.second_table.resizeColumnsToContents()

    # Функция удаления выбранной строки в первой таблице
    def delete_first(self):
        if self.first_table.activated and self.first_table.currentRow() != -1:
            self.first_table.removeRow(self.first_table.currentRow())
            self.first_table.selectionModel().clearCurrentIndex()
        else:
            self.show_message("Не выбрана строка")


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()