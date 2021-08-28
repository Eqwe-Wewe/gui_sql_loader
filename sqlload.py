import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    # QVBoxLayout,
    QApplication,
    QAction,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMenuBar,
    QMenu,
    QStatusBar,
    qApp,
    QGridLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.menu()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        
        #self.setFixedSize(250, 150)
        self.setWindowTitle('SQL-script loader')

        self.w = QWidget(self)
        self.setCentralWidget(self.w)

        self.label_open = QLabel(self.w)
        self.label_open.setText('✓')
        self.label_load = QLabel(self.w)
        self.label_load.setText('✓')

        
        self.open_btn = QPushButton(self.w)
        self.open_btn.setText('Open file')
        self.open_btn.pressed.connect(self.openFile)
        self.load_btn = QPushButton(self.w)
        self.load_btn.setText('Load file')
        self.load_btn.pressed.connect(self.loadFile)
        self.load_btn.move(100, 0)

        self.grid = QGridLayout(self.w)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label_open, 1, 0)
        self.grid.addWidget(self.label_load, 1, 1)
        self.grid.addWidget(self.open_btn, 2, 0)
        self.grid.addWidget(self.load_btn, 2, 1)

        
    def menu(self):
        setAct = QAction('Configure the connection', self)
        setAct.setShortcut('Ctrl+N')
        setAct.triggered.connect(self.setConn)
        aboutAct = QAction('About', self)
        aboutAct.triggered.connect(self.about)
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        menu = self.menuBar()
        mainMenu = menu.addMenu('File')
        mainMenu.addAction(setAct)
        mainMenu.addSeparator()
        mainMenu.addAction(exitAct)
        helpMenu = menu.addMenu('Help')
        helpMenu.addAction(aboutAct)

    def openFile(self):
        pass

    def loadFile(self):
        pass

    def setConn(self):
        pass

    def about(self):
        pass


def main():
    app = app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
