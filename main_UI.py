from func import *
from PyQt5 import QtWidgets
from UI_main import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QWidget, QComboBox
import sys


class Mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.activated[str].connect(self.onActivated)
        self.comboBox_1.activated[str].connect(self.onActivated)
        self.pushButton.clicked.connect(self.push_Btn)

    def onActivated(self):
        if self.comboBox_1.currentText() == "Hamming code":
            if self.comboBox.currentText() == "Hide information":
                self.lineEdit_2.show()
                self.label_2.show()
                self.doubleSpinBox.close()
                self.label_3.close()
            else:
                self.doubleSpinBox.close()
                self.label_2.close()
                self.label_3.close()
                self.lineEdit_2.close()
        else:
            if self.comboBox.currentText() == "Hide information":
                self.lineEdit_2.show()
                self.label_2.show()
                self.doubleSpinBox.show()
                self.label_3.show()
            else:
                self.doubleSpinBox.close()
                self.label_2.close()
                self.label_3.close()
                self.lineEdit_2.close()

    def push_Btn(self):
        if self.comboBox.currentText() == "Hide information":
            if self.comboBox_1.currentText() == 'LSB-R':
                encode_LSBR(self.lineEdit.text(), '1.bmp', self.lineEdit_2.text(), self.doubleSpinBox.value())
                text = 'Секретное сообщение запаковано в контейнер 1.bmp'
                self.label_5.setText(text)
            elif self.comboBox_1.currentText() == 'LSB-M':
                encode_LSBM(self.lineEdit.text(), '2.bmp', self.lineEdit_2.text(), self.doubleSpinBox.value())
                text = 'Секретное сообщение запаковано в контейнер 2.bmp'
                self.label_5.setText(text)
            else:
                encode_HAM(self.lineEdit.text(), '3.bmp', self.lineEdit_2.text())
                text = 'Секретное сообщение запаковано в контейнер 3.bmp'
                self.label_5.setText(text)
        else:
            if self.comboBox_1.currentText() == 'LSB-R':
                decode_LSBR(self.lineEdit.text(), 'output_1.txt')
                text = 'Секретное сообщение распаковано в output_1.txt'
                self.label_5.setText(text)
            elif self.comboBox_1.currentText() == 'LSB-M':
                decode_LSBM(self.lineEdit.text(), 'output_2.txt')
                text = 'Секретное сообщение  распаковано в output_2.txt'
                self.label_5.setText(text)
            else:
                decode_HAM(self.lineEdit.text(), 'output_3.txt')
                text = 'Секретное сообщение  распаковано в output_3.txt'
                self.label_5.setText(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = Mywindow()
    application.show()

    sys.exit(app.exec())
