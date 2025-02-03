import calc
import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

data = calc.read_data("data.txt")

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(1000)
        self.setFixedHeight(1300)

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 9))

        self.setWindowTitle("Многомерная интерполяция")
        self.x_label = QtWidgets.QLabel()
        self.x_label.setText("x: ")
        self.x = QtWidgets.QLineEdit()
        self.y_label = QtWidgets.QLabel()
        self.y_label.setText("y: ")
        self.y = QtWidgets.QLineEdit()
        self.z_label = QtWidgets.QLabel()
        self.z_label.setText("z: ")
        self.z = QtWidgets.QLineEdit()

        self.nx_label = QtWidgets.QLabel()
        self.nx_label.setText("nx: ")
        self.nx = QtWidgets.QLineEdit()
        self.ny_label = QtWidgets.QLabel()
        self.ny_label.setText("ny: ")
        self.ny = QtWidgets.QLineEdit()
        self.nz_label = QtWidgets.QLabel()
        self.nz_label.setText("nz: ")
        self.nz = QtWidgets.QLineEdit()
        
        self.x_option_label = QtWidgets.QLabel()
        self.x_option_label.setText("Интерполяция по x:")
        self.x_option = QtWidgets.QComboBox()
        self.x_option.addItem("Алгоритм Ньютона")
        self.x_option.addItem("Алгоритм Сплайнов")

        self.y_option_label = QtWidgets.QLabel()
        self.y_option_label.setText("Интерполяция по y:")
        self.y_option = QtWidgets.QComboBox()
        self.y_option.addItem("Алгоритм Ньютона")
        self.y_option.addItem("Алгоритм Сплайнов")

        self.z_option_label = QtWidgets.QLabel()
        self.z_option_label.setText("Интерполяция по z:")
        self.z_option = QtWidgets.QComboBox()
        self.z_option.addItem("Алгоритм Ньютона")
        self.z_option.addItem("Алгоритм Сплайнов")
        
        self.btn = QtWidgets.QPushButton()
        self.btn.setText("Рассчитать")
        self.btn.clicked.connect(self.process)
        
        self.answer = QtWidgets.QLabel()
        self.answer.setText("Ответ: ")

        w = QtWidgets.QWidget()
        start = QtWidgets.QVBoxLayout()
        w.setLayout(start)
        self.setCentralWidget(w)
        
        start.addWidget(self.x_label)
        start.addWidget(self.x)
        start.addWidget(self.y_label)
        start.addWidget(self.y)
        start.addWidget(self.z_label)
        start.addWidget(self.z)
        start.addStretch()
        start.addWidget(self.nx_label)
        start.addWidget(self.nx)
        start.addWidget(self.ny_label)
        start.addWidget(self.ny)
        start.addWidget(self.nz_label)
        start.addWidget(self.nz)
        start.addStretch()
        start.addWidget(self.x_option_label)
        start.addWidget(self.x_option)
        start.addWidget(self.y_option_label)
        start.addWidget(self.y_option)
        start.addWidget(self.z_option_label)
        start.addWidget(self.z_option)
        start.addStretch()
        start.addWidget(self.btn)
        start.addWidget(self.answer)
        w.setFont(QtGui.QFont("Times", 12))

    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()
        
    def process(self):
        try:
            x = float(self.x.text())
            y = float(self.y.text())
            z = float(self.z.text())
            nx = int(self.nx.text())
            ny = int(self.ny.text())
            nz = int(self.nz.text())
            modex = int(self.x_option.currentIndex())
            modey = int(self.y_option.currentIndex())
            modez = int(self.z_option.currentIndex())
            if x < 0 or x > 5:
                self.show_message("x должен лежать в интервале от 0 до 5")
                return
            if y < 0 or y > 5:
                self.show_message("y должен лежать в интервале от 0 до 5")
                return
            if z < 0 or z > 5:
                self.show_message("z должен лежать в интервале от 0 до 5")
                return
            if nx < 0 or nx > 4:
                self.show_message("nx должен лежать в интервале от 0 до 4")
                return
            if ny < 0 or ny > 4:
                self.show_message("ny должен лежать в интервале от 0 до 4")
                return
            if nz < 0 or nz > 4:
                self.show_message("nz должен лежать в интервале от 0 до 4")
                return
            ans = calc.f_x_y_z(data, nx, ny, nz, x, y, z, modex, modey, modez)
            self.answer.setText(f"Ответ: {ans: 10.6f}")
        except ValueError:
            self.show_message("Ошибка ввода параметров окружности")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()