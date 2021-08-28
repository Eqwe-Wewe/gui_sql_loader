import sys
import os
from PyQt5.QtWidgets import (
    QWidget,
    # QVBoxLayout,
    QApplication,
    # QTableWidgetItem,
    QLabel,
    QPushButton,
    QHBoxLayout,
    # QMainWindow
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # QMainWindow.setFixedSize(200, 100)
        self.setFixedSize(250, 150)
        self.g_layout = QHBoxLayout(self)
        self.open_btn = QPushButton(self)
        self.open_btn.setText('Open file')
        self.open_btn.pressed.connect(self.open)
        self.g_layout.addWidget(self.open_btn)
        self.load_btn = QPushButton(self)
        self.load_btn.setText('Load file')
        self.load_btn.pressed.connect(self.load)
        self.g_layout.addWidget(self.load_btn)
        self.pref_btn = QPushButton(self)
        self.pref_btn.setText('Preference connect')
        self.pref_btn.pressed.connect(self.pref)
        self.g_layout.addWidget(self.pref_btn)

    def open(self):
        pass

    def load(self):
        pass

    def pref(self):
        pass


def main():
    app = app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = Window()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
