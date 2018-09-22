#!/usr/bin/env python3

import sys
import socket
import os


CSPort = 58037

userCredentials = { "86420" : "12345678" } # dictionary of user ids with their respective passwords

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', CSPort))
server.listen(20)  # max backlog of connections





def authenticate(client_socket, adress):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if messages[0] in userCredentials:
        if userCredentials[messages[0]] == messages[1]:
            client_socket.send("OK\n".encode())
            handle_client_connection(client_socket)
        else:
            client_socket.send("NOK\n".encode())
            client_socket.close()
    else:
        client_socket.send("NEW\n".encode())
        #criar utilizador
        client_socket.close()



def handle_client_connection(client_socket):
    message = ""
    while message != "exit\n":
        message = client_socket.recv(1024).decode()
        print(message, end= '')
    client_socket.close()
    #exit()


def init():
    n_argument = len(sys.argv)
    if n_argument == 3:
        CSPort = sys.argv[2]
    elif n_argument > 1:
        raise ValueError("numero errado de argumentos")
        exit()






while True:
    client_socket, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    #pid = os.fork()
    #if pid == 0:
    authenticate(client_socket, address)
