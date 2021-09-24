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
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QListWidget
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect, QSize, pyqtSignal
import resources
from db import DataBase
import json
import os
import sys


class ListWidget(QListWidget):
    def __init__(self, *args):
        super().__init__()

    def addItems(self, *args):
        super().addItems(*args)
        args = args[0]
        self.kw_args = dict(zip(args, range((len(args)))))
        print(self.kw_args)


class Label(QLabel):
    labelClicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.labelClicked.emit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.menu()

    def initUI(self):
        self.statusBar().showMessage('Ready')

        self.setFixedSize(250, 200)
        self.setWindowTitle('SQL-script loader')

        self.w = QWidget(self)
        self.setCentralWidget(self.w)

        self.name_conn = QComboBox(self)
        self.loadConn(self.name_conn)

        self.label_file_name = QLabel(self.w)
        self.label_file_name.setWordWrap(True)

        self.open_btn = QPushButton(self.w)
        self.open_btn.setText('Open file')
        self.open_btn.pressed.connect(self.openFile)
        self.load_btn = QPushButton(self.w)
        self.load_btn.setText('Load file')
        self.load_btn.setEnabled(False)
        self.load_btn.pressed.connect(self.loadFile)
        self.load_btn.move(100, 0)

        self.grid = QGridLayout(self.w)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label_file_name, 1, 0)
        self.grid.addWidget(self.name_conn, 1, 1)
        self.grid.addWidget(self.open_btn, 2, 0)
        self.grid.addWidget(self.load_btn, 2, 1)

    def menu(self):
        setAct = QAction('Configure the connection', self)
        setAct.setShortcut('Ctrl+N')
        setAct.triggered.connect(self.setConn)
        delConnAct = QAction('Drop the connection', self)
        delConnAct.triggered.connect(self.delConn)
        aboutAct = QAction('About', self)
        aboutAct.triggered.connect(self.about)
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        menu = self.menuBar()
        mainMenu = menu.addMenu('File')
        mainMenu.addAction(setAct)
        mainMenu.addAction(delConnAct)
        mainMenu.addSeparator()
        mainMenu.addAction(exitAct)
        helpMenu = menu.addMenu('Help')
        helpMenu.addAction(aboutAct)

    def loadConn(self, widget):
        try:
            with open('config.json', 'r') as file:
                data = json.load(file)
                items = [i for i in data]
                print(items)
        except Exception:
            return ['no connections']
        else:
            widget.clear()
            widget.addItems(items)

    def openFile(self):
        try:
            self.path_script = QFileDialog.getOpenFileNames(
                self, None, None, "*.sql"
            )[0][0]
        except IndexError:
            None
        else:
            self.label_file_name.setText(self.path_script)
            self.load_btn.setEnabled(True)

    def loadFile(self):
        with DataBase(*self.getConfig()) as cursor:
            if cursor.execute(open(self.path_script).read()):
                mes = 'The script load successfully!'
            else:
                mes = 'Error'
        self.statusBar().showMessage(mes)

    def getConfig(self):
        config_name = self.name_conn.currentText()
        with open('config.json', 'r') as file:
            data = json.load(file)
            config = [i for i in data if i == config_name][0]
            print(config)
            db_type = config['dbms']
        return [
            {
                'user': config['user'],
                'password': config['password'],
                'host': config['ip-address']['host'],
                'port': config['ip-address']['port'],
                'database': config['database']
            },
            db_type
        ]

    def setConn(self):
        self.conn = Settings(self)
        self.conn.exec_()
        self.loadConn(self.name_conn)

    def delConn(self):
        self.del_connect = Deleter(self)
        self.del_connect.exec_()
        self.loadConn(self.name_conn)

    def about(self):
        pass


class Settings(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Configure the connection")
        self.name = QLabel('connection name')
        self.user = QLabel('user')
        self.password = QLabel('password')
        self.host = QLabel('host')
        self.port = QLabel('port')
        self.database = QLabel('database')
        self.dbms = QLabel('database system')

        self.setName = QLineEdit(self)
        self.setUser = QLineEdit(self)
        self.setPassword = QLineEdit(self)
        self.setPassword.setEchoMode(QLineEdit.Password)
        self.setHost = QLineEdit(self)
        self.setPort = QLineEdit(self)
        self.setDatabase = QLineEdit(self)
        self.lst_dbms = QComboBox(self)
        self.lst_dbms.addItems(['MySQL', 'PostgreSQL', 'SQLite'])

        self.btn = QPushButton("Configure", self)
        self.btn.pressed.connect(self.configure)

        self.echo = True
        self.echo_label = Label(self)
        self.echo_label.setPixmap(
            QPixmap(':/source/close_eye.png').scaled(
                20,
                20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        self.echo_label.setFixedSize(20, 20)
        self.echo_label.labelClicked.connect(self.echoAction)

        self.msg = QMessageBox(self)

        self.g = QGridLayout(self)
        self.g.addWidget(self.name, 1, 0)
        self.g.addWidget(self.setName, 1, 1)
        self.g.addWidget(self.user, 2, 0)
        self.g.addWidget(self.setUser, 2, 1)
        self.h = QHBoxLayout(self)
        self.h.addWidget(self.password)
        self.h.addWidget(self.echo_label)
        self.g.addLayout(self.h, 3, 0)
        self.g.addWidget(self.setPassword, 3, 1)
        self.g.addWidget(self.host, 4, 0)
        self.g.addWidget(self.setHost, 4, 1)
        self.g.addWidget(self.port, 5, 0)
        self.g.addWidget(self.setPort, 5, 1)
        self.g.addWidget(self.database, 6, 0)
        self.g.addWidget(self.setDatabase, 6, 1)
        self.g.addWidget(self.dbms, 7, 0)
        self.g.addWidget(self.lst_dbms, 7, 1)
        self.g.addWidget(self.btn, 8, 0, 1, 0)

    def configure(self):
        if not os.path.exists('config.json'):
            with open('config.json', 'w', encoding='utf-8') as file:
                data = {}
                json_data = json.dump(data, file, indent=3)
                file.write(json_data)

        with open('config.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        with open('config.json', 'w', encoding='utf-8') as file:
            json_data[self.setName.text()] = {
                'user': self.setUser.text(),
                'password': self.setPassword.text(),
                'ip-address': {
                    'host': self.setHost.text(),
                    'port': self.setPort.text()
                },
                'database': self.setDatabase.text(),
                'dbms': self.lst_dbms.currentText()
            }
            print(json_data)
            try:
                json.dump(json_data, file, indent=3, ensure_ascii=False)
            except Exception as err:
                message = err
            else:
                message = 'config create successfully!'
            finally:
                self.msg.information(self, 'info', message)

    def echoAction(self):
        if self.echo is True:
            self.setPassword.setEchoMode(QLineEdit.Normal)
            self.echo = False
            echo_icon = ':/source/open_eye.png'
        else:
            self.setPassword.setEchoMode(QLineEdit.Password)
            self.echo = True
            echo_icon = ':/source/close_eye.png'
        self.echo_label.setPixmap(
            QPixmap(echo_icon).scaled(
                20,
                20,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )


class Deleter(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.lst = ListWidget(self)
        Window.loadConn(self, self.lst)
        self.lst.itemClicked.connect(self.select_conn)

        self.del_button = QPushButton('Delete connection', self)
        self.del_button.setMaximumWidth(150)
        self.del_button.clicked.connect(self.drop_conn_json)

        self.h_layout = QVBoxLayout(self)
        self.h_layout.addWidget(self.lst, alignment=Qt.AlignCenter)
        self.h_layout.addWidget(self.del_button, alignment=Qt.AlignCenter)

        self.msg = QMessageBox(self)

    def drop_conn_json(self):
        self.lst.takeItem(self.lst.kw_args[self.conn])
        self.lst.kw_args.pop(self.conn)
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.pop(self.conn)
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=3, ensure_ascii=False)
            self.msg.information(self, 'info', 'config delete!')

        # Window.name_conn.removeItem(Window.name_conn.currentIndex())

    def select_conn(self, conn):
        self.conn = conn.text()


def main():
    app = app = QApplication(sys.argv)
    # app.setStyle('Fusion')
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
