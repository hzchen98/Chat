# -*- coding: utf-8 -*-
import socketserver
import atexit
from tools.socket_tools import *
from socket import *
import _thread

#self.admin_pass = '29de6dc7be7dbc85f8e78fd4f2275a514a1dcf09515f4dcf1cfcc9863e6c73b2' #sha256 mingzhi
class MyTCPSocketHandler(socketserver.BaseRequestHandler):

    def handle(self): #acción a realizar cuando recibe una paquete
        message_client = self.client_address[0]

        if message_client not in client_list:
            print(message_client + " has connected")
            client_list.append(message_client)
            self.send_allClient("*new client*", no_send_client=message_client)
            return

        self.data = self.request.recv(1024)
        message = self.data.decode(encoding="UTF-8")
        print("{} wrote:\n".format(message_client))
        print(message)
        if message == "*quit*":
            print(message_client+ " has disconnected!")
            client_list.remove(message_client)
            message = "*delete*"

        self.send_allClient(message)

    def send_allClient(self, message, no_send_client=None): #difusión del mensaje
        for client in client_list:
            if no_send_client == client:
                continue
            _thread.start_new_thread(send_client, (client, message))
            #self.send_client(client, message)

def send_client(client, message):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((client, 9999))
    send_message = client[0]+"$$"+message
    try:
        sock.send(send_message.encode(encoding="UTF-8"))
    except Exception as er:
        print(er)
    finally:
        sock.close()

if __name__ == "__main__":
    HOST, PORT = get_myIp2(), 10001
    client_firstTime = []
    client_list = []

    server = socketserver.TCPServer((HOST, PORT), MyTCPSocketHandler)
    try:
        print("Server on %s and port %s" % (HOST, PORT))
        server.serve_forever()
        atexit.register(server.close_request, ())
    except Exception as er:
        print(er)
        server.server_close()
