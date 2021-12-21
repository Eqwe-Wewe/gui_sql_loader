from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
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
import unnamed_pkg.resources
from unnamed_pkg.db import DataBase
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

    def takeItem(self, item: str):
        super().takeItem(self.kw_args[item])
        self.kw_args.pop(item)


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

        self.setFixedSize(350, 200)
        self.setWindowTitle('SQL-script loader')

        self.w = QWidget(self)
        self.setCentralWidget(self.w)

        self.name_conn = QComboBox(self)
        self.loadConn(self.name_conn)

        self.label_file_name = QListWidget(self.w)
        self.label_file_name.setWordWrap(True)

        self.add_btn = QPushButton(self.w)
        self.add_btn.setText('Add file')
        self.add_btn.pressed.connect(self.addFile)
        self.send_btn = QPushButton(self.w)
        self.send_btn.setText('Send data')
        self.send_btn.setEnabled(False)
        self.send_btn.pressed.connect(self.sendData)
        self.send_btn.move(100, 0)

        self.grid = QGridLayout(self.w)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label_file_name, 1, 0)
        self.grid.addWidget(self.name_conn, 1, 1)
        self.grid.addWidget(self.add_btn, 2, 0)
        self.grid.addWidget(self.send_btn, 2, 1)

    def menu(self):
        addConnAct = QAction('Add connection', self)
        addConnAct.setShortcut('Ctrl+N')
        addConnAct.triggered.connect(self.setConn)
        confConnAct = QAction('Configure connection', self)
        confConnAct.triggered.connect(self.confConn)
        delConnAct = QAction('Drop the connection', self)
        delConnAct.triggered.connect(self.delConn)
        aboutAct = QAction('About', self)
        aboutAct.triggered.connect(self.about)
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        menu = self.menuBar()
        mainMenu = menu.addMenu('File')
        mainMenu.addAction(addConnAct)
        mainMenu.addAction(confConnAct)
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
        except Exception:
            return ['no connections']
        else:
            widget.clear()
            widget.addItems(items)

    def addFile(self):
        try:
            self.path_scripts = QFileDialog.getOpenFileNames(
                self, None, None, "*.sql"
            )[0]
        except IndexError:
            None
        else:
            self.label_file_name.addItems(self.path_scripts)
            if len(self.path_scripts) > 0:
                self.send_btn.setEnabled(True)

    def sendData(self):
        for path in self.path_scripts:
            with DataBase(*self.getConfig()) as cursor:
                if cursor.execute(open(path).read()):
                    mes = 'The script load successfully!'
                else:
                    mes = 'Error'
        self.statusBar().showMessage(mes)

    def getConfig(self):
        config_name = self.name_conn.currentText()
        with open('config.json', 'r') as file:
            data = json.load(file)
            config = [i for i in data if i == config_name][0]
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
        self.conn = addConnect(self)
        self.conn.exec_()
        self.loadConn(self.name_conn)

    def confConn(self):
        self.del_connect = configureConnect(self)
        self.del_connect.exec_()
        self.loadConn(self.name_conn)

    def delConn(self):
        self.del_connect = Deleter(self)
        self.del_connect.exec_()
        self.loadConn(self.name_conn)

    def about(self):
        self.inst_about = About(self)
        self.inst_about.exec_()


class Settings(QDialog):
    def __init__(self, parent):
        super().__init__()
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
        self.lst_dbms.addItems(['MySQL', 'PostgreSQL'])

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
            try:
                json.dump(json_data, file, indent=3, ensure_ascii=False)
            except Exception as err:
                message = err
            else:
                message = 'config create successfully!'
            finally:
                self.msg.information(self, 'info', message)
                self.close()

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

class addConnect(Settings, QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Add connection")


class configureConnect(Settings, QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.lst_label = QLabel('list of connections')
        self.lst_combobox = QComboBox(self)
        Window.loadConn(self, self.lst_combobox)
        self.lst_combobox.currentTextChanged.connect(self.change_prop_qline)
        self.g.addWidget(self.lst_label, 0, 0)
        self.g.addWidget(self.lst_combobox, 0, 1)
        self.change_prop_qline()
        self.setWindowTitle("Configure connection")

    def change_prop_qline(self):
        with open('config.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        name_conn = json_data[self.lst_combobox.currentText()]
        self.setName.setText(self.lst_combobox.currentText())
        self.setUser.setText(name_conn['user'])
        self.setPassword.setText(name_conn['password'])
        self.setHost.setText(name_conn['ip-address']['host'])
        self.setPort.setText(name_conn['ip-address']['port'])
        self.setDatabase.setText(name_conn['database'])
        self.lst_dbms.setCurrentText(name_conn['dbms'])
            

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
        self.check_lst_for_emp()
        
    def drop_conn_json(self):
        self.lst.takeItem(self.conn)
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        data.pop(self.conn)
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=3, ensure_ascii=False)
            self.msg.information(self, 'info', 'config delete!')
        self.check_lst_for_emp()    

    def check_lst_for_emp(self):
        if self.lst.count() == 0:
            self.lst.addItem('empty')
            self.lst.setStyleSheet(
                """
                    QListWidget {
                        color: grey
                    }
                """
            )
            self.lst.itemClicked.disconnect(self.select_conn)
            self.del_button.setEnabled(False)
        else:
            self.del_button.setEnabled(True)

    def select_conn(self, conn):
        self.conn = conn.text()


class About(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.label = QLabel(self)
        self.label.setText(
            """
            <div style= margin-left:10px>
              <br>
              author: Sergey Samchuk
              <br>date: 10.2021
              <br>
              <p>This application is designed to download and execute SQL scripts.
              <br>It works with the following DBMS:
              <ul>
                  <li>MySQL</li>
                  <li>PostgreSQL</li>
              </ul>
            </div>
            
            """
        )
        self.button = QPushButton('Ok', self)
        self.button.setMaximumWidth(70)
        self.button.pressed.connect(self.close)
        self.h_layout = QVBoxLayout(self)
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.setWindowTitle("About")
        self.setFixedSize(350, 200)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
