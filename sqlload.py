import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    # QVBoxLayout,
    QApplication,
    QAction,
    # QTableWidgetItem,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMenuBar,
    QMenu,
    QStatusBar,
    qApp,
    QTextEdit,
    QGridLayout,
    QDialog,
    QComboBox,
    QLineEdit
    # QMainWindow
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QSize


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.menu()

    def initUI(self):
        self.statusBar().showMessage('Ready')

        # self.setFixedSize(250, 150)
        self.setWindowTitle('SQL-script loader')

        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)
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
        # exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menu = self.menuBar()
        mainMenu = menu.addMenu('File')
        mainMenu.addAction(setAct)
        mainMenu.addSeparator()
        mainMenu.addAction(exitAct)
        helpMenu = menu.addMenu('Help')
        helpMenu.addAction(aboutAct)

        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(exitAct)

    def openFile(self):
        pass

    def loadFile(self):
        pass

    def setConn(self):
        self.conn = Settings(self)

        self.conn.exec_()

    def about(self):
        pass


class Settings(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle("Configure the connection")
        self.user = QLabel('user')
        self.password = QLabel('password')
        self.host = QLabel('host')
        self.port = QLabel('port')
        self.database = QLabel('database')
        self.dbms = QLabel('database system')

        self.setUser = QLineEdit(self)
        self.setPassword = QLineEdit(self)
        self.setPassword.setEchoMode(QLineEdit.Password)
        self.setHost = QLineEdit(self)
        self.setPort = QLineEdit(self)
        self.setDatabase = QLineEdit(self)
        self.lst_dbms = QComboBox(self)
        self.lst_dbms.addItems(['MySQL', 'PostgresSQL'])

        self.btn = QPushButton("Configure", self)
        self.btn.pressed.connect(self.configure)
        self.btn_echo = QPushButton('echo', self)
        self.btn_echo.setFixedWidth(20)
        self.btn_echo.pressed.connect(self.echoOn)

        self.status = QStatusBar()

        self.g = QGridLayout(self)
        self.g.addWidget(self.user, 1, 0)
        self.g.addWidget(self.setUser, 1, 1)
        self.h = QHBoxLayout(self)
        self.h.addWidget(self.password)
        self.h.addWidget(self.btn_echo)
        self.g.addLayout(self.h, 2, 0)
        self.g.addWidget(self.setPassword, 2, 1)
        self.g.addWidget(self.host, 3, 0)
        self.g.addWidget(self.setHost, 3, 1)
        self.g.addWidget(self.port, 4, 0)
        self.g.addWidget(self.setPort, 4, 1)
        self.g.addWidget(self.database, 5, 0)
        self.g.addWidget(self.setDatabase, 5, 1)
        self.g.addWidget(self.dbms, 6, 0)
        self.g.addWidget(self.lst_dbms, 6, 1)
        self.g.addWidget(self.btn, 7, 0, 1, 0)
        self.g.addWidget(self.status, 8, 0)

    def configure(self):
        self.status.showMessage('Success')

    def echoOn(self):
        pass
        '''
        self.echo = True
        if self.echo is True:
            #self.psw_val = self.setPassword.text()
            #self.setPassword.setEchoMode(QLineEdit.PasswordEchoOnEdit)
            #self.g.addWidget(self.setPassword, 2, 1)
        '''


def main():
    app = app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
