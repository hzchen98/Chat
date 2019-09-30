# -*- coding: utf-8 -*-
#!/usr/bin/python

from window.tkinter_window import Mainwindow
from _thread import start_new_thread
from socketserver import BaseRequestHandler, TCPServer
from tkinter import Tk
from tools.socket_tools import *

class MyTCPSocketHandler(BaseRequestHandler): #servidor tcp de escucha para la difusión del servidor principal

    def handle(self): # función que salta en cuanto recive un paquete
        self.data = self.request.recv(1024)
        data = self.data.decode(encoding="UTF-8").split("$$")
        host, message = data[0], data[1]
        print("{} wrote:\n".format(host), message)

        if message == "*new client*" or host not in connected_list:
            connected_list.append(host)
            app.add_connect(host)
            message = "Ha entrado a la conversación"
        if message == "*delete*":
            app.delete_connect(host, connected_list)
            message = "Se ha salido de la conversación!"

        app.receive_message(host, message)

def main_tkinter(send_host, users_list):
    height = 800
    width = 550
    root = Tk()
    root.title("Chat 1.0")
    root.geometry("800x550")
    root.resizable(width=False, height=False) #deshabilita el redimensionamiento de la ventana
    global app
    app = Mainwindow(height, width, send_host, users_list, root)
    app.mainloop()

if __name__ == '__main__':
    server = search_server()
    local_ip= get_myIp()
    #send_host = ("192.168.1.134", 10001)
    send_host = (server, 10001)
    listen_host = (local_ip, 9999)
    print(listen_host)
    global connected_list
    connected_list = [local_ip]
    server = TCPServer(listen_host, MyTCPSocketHandler) #servidor de escuha
    try:
        start_new_thread(server.serve_forever, ())
        main_tkinter(send_host, connected_list)
    except Exception as er:
        print(er)
        pass
    finally:
        sock = socket()
        sock.connect(send_host)
        sock.send("*quit*".encode(encoding="UTF-8")) #mensaje de salida al servidor central
        server.server_close()
