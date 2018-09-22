#!/usr/bin/env python3

import sys
import socket
import os


CSPort = 58037

userCredentials = { "86420" : "12345678" } # dictionary of user ids with their respective passwords

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', CSPort))
server.listen(20)  # max backlog of connections


def createUser(istid, password):
    userCredentials[istid] = password



def authenticate(client_socket, adress):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    istid = messages[1]
    if messages[0] != "AUT":
        client_socket.send("ERR AUT\n".encode())
    elif messages[1] in userCredentials:
        if userCredentials[messages[1]] == messages[2]:
            client_socket.send("AUR OK\n".encode())
            handle_client_connection(client_socket)
        else:
            client_socket.send("AUR NOK\n".encode())
            #client_socket.close()
    else:
        client_socket.send("AUR NEW\n".encode())
        createUser(messages[1], messages[2])
        handle_client_connection(client_socket, istid)



def handle_client_connection(client_socket, istid):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if messages[0] == "DLU":
        del(userCredentials[istid])
""" elif messages[0] == "DLR":
    elif messages[0] == "BCK":
    elif messages[0] == "BKR":
    elif messages[0] == "RST":
    elif messages[0] == "RSR":
    elif messages[0] == "LSD":
    elif messages[0] == "LDR":
    elif messages[0] == "LSF":
    elif messages[0] == "LFD":
    elif messages[0] == "LSD":
    elif messages[0] == "DEL":
    elif messages[0] == "DDR":       """


    #exit()





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
