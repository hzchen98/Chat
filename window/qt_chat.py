# -*- coding: utf-8 -*-
from window.qt_chat_window import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket
from tools.generate_sha256 import generate_hash
import _thread


def main_qt(host):
    app = QtWidgets.QApplication(sys.argv)
    window = Chat(host)
    window.setWindowTitle("ChatDAM 1.0")
    window.show()
    app.exec_()


class Chat(Ui_MainWindow, QMainWindow):

    def __init__(self, host):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.host = host
        self.setupUi(self)
        self.setupFunctions()

    def setupFunctions(self):
        self.textEdit.setFocus()
        self.sendButton.clicked.connect(self.sendMessage)
        self.clearButton.clicked.connect(self.textEdit.clear)

    def sendMessage(self):
        message = self.textEdit.toPlainText()
        if message == "":
            return
        message = message.encode()
        sock = socket.socket()
        sock.bind()
        sock.connect((self.host))
        _thread.start_new_thread(sock.send, (message,))
        _thread.start_new_thread(sock.close, ())
        self.textEdit.clear()

    def keyPressEvent(self, event):
        if event.key() == (Qt.Key_Control and Qt.Key_Backspace):
            self.textEdit.clear()
        if event.key() == (Qt.Key_Return):
            self.sendMessage()

    def input_chatBrowser(self, message):
        message += "\n"
        self.chatBrowser.append(message)

    def add_connected(self, client):
        self.connectedList.addItem(client)

    def drop_connected(self, client):
        search = self.connectedList.findItems(client, Qt.MatchExactly)
        self.connectedList.takeItem(self.connectedList.row(search[0]))

    def receive_message(self, tu):
        while 1:
            data = self.sock.recv(4096)
            message = data.decode().strip()
            if message != "":
                self.chatBrowser.setText(message+"\n")
