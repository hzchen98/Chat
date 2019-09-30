# -*- coding: utf-8 -*-
from tkinter import Frame, Text, Y, Listbox, RIGHT, DISABLED, Button, NORMAL, Scrollbar
from socket import socket, AF_INET, SOCK_STREAM
from _thread import start_new_thread

class Mainwindow(Frame):

    def __init__(self, height, width, server_host, users_list, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.height = height
        self.width = width
        self.server_host = server_host
        self.pack()
        self.createWidgets()
        self.setupFunctions()
        self.insert_text("Has entrado a la conversación!")
        self.add_connect(users_list[0])

    def createWidgets(self):
        self.chat_browser_scrollBar = Scrollbar(self.master)
        self.chat_browser_scrollBar.place(x=self.width-15, y=0, height=self.height*0.5)
        self.chat_browser = Text(self.master, yscrollcommand=self.chat_browser_scrollBar.set)
        self.chat_browser.place(x=0, y=0, width=self.width-15, height=self.height * 0.5)
        self.chat_browser.config(state=DISABLED)
        self.chat_browser_scrollBar.config(command=self.chat_browser.yview)
        self.text_writter = Text(self.master)
        self.text_writter.place(x=0, y=(self.height * 0.5) + 5, height=140)
        self.connected_list = Listbox(self.master)
        self.connected_list.place(x=self.width + 5, y=0, height=self.height * 0.5, width=self.width * 0.44)
        self.send_button = Button(self.master, text="Enviar", command=self.send_message)
        self.send_button.place(x=self.width * 1.22, y=self.height / 2 + 15, height=40, width=100)
        self.clear_button = Button(self.master, text="Borrar", command=self.clear_text)
        self.clear_button.place(x=self.width * 1.22, y=self.height / 2 + 80, height=40, width=100)


    def setupFunctions(self):
        self.text_writter.bind_all("<Return>", self.send_key_pressed)
        self.text_writter.bind_all("<BackSpace>", self.clear_key_pressed)

    def send_key_pressed(self, event):
        self.send_message()

    def clear_key_pressed(self, event):
        self.clear_text()

    def receive_message(self, host, message):
        text = host+":\n\t"+message
        self.insert_text(text)

    def insert_text(self, message):
        message += "\n"
        self.chat_browser.config(state=NORMAL)
        self.chat_browser.insert("end", message)
        self.chat_browser.config(state=DISABLED)
        self.chat_browser.see("end")

    def add_connect(self, item):
        color = "white"
        if self.connected_list.size() % 2 == 1:
            color = "#eaeae1"
        self.connected_list.insert("end", item)
        self.connected_list.itemconfig("end", bg=color)

    def delete_connect(self, item, list):
        list.remove(item)
        self.connected_list.delete(0, "end")
        for i in list:
            self.add_connect(i)

    def reset_connected_list(self, list):
        self.connected_list.delete(0, "end")
        for i in list:
            self.add_connect(i)

    def clear_text(self):
        self.text_writter.delete("1.0", "end")

    def send_message(self, text=None):
        message = text
        if not message:
            message = self.text_writter.get("1.0", "end")
            message = message.strip()
            self.text_writter.delete("1.0", "end")
        if not message:
            return

        print("Enviando mensaje:", message)
        start_new_thread(self.send_sock, (message,))

    def send_sock(self, message):
        message = message.encode(encoding="UTF-8")
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.server_host))
        sock.send(message)
        sock.close()
