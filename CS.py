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

def printRequirement(istid, address, requestType, directory = ''):
    print("User:" + istid + " Requirement:" + requestType + "\nIP:" + str(address[0]) + " Port:" + str(address[1]))

def authenticate(client_socket, adress):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.close()
        return True
    elif messages[0] != "AUT":
        client_socket.send("ERR AUT\n".encode())
    else:
        istid = messages[1]
        password = messages[2]
        printRequirement(istid, address, "AUT")
        if istid in userCredentials:
            if userCredentials[istid] == password:
                client_socket.send("AUR OK\n".encode())
                return handle_client_connection(client_socket, istid, address)
            else:
                client_socket.send("AUR NOK\n".encode())
                #client_socket.close()
        else:
            client_socket.send("AUR NEW\n".encode())
            createUser(istid, password)
            return handle_client_connection(client_socket, istid, address)
    return False


def handle_client_connection(client_socket, istid, address):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.close()
        return True
    requirement = messages[0]
    if requirement == "DLU":
        printRequirement(istid, address, "DLU")
        del(userCredentials[istid])
        client_socket.send("DLR OK\n".encode())
    return False
""" elif requirement == "BCK":
    elif requirement == "RST":
    elif requirement == "LSD":
    elif requirement == "LSF":
    elif requirement == "LSD":
    elif requirement == "DEL":      """

    #exit()





if len(sys.argv) == 3 and sys.argv[1] == "-p":
    CSPort = eval(sys.argv[2])
elif n_argument > 1:
    raise ValueError("numero errado de argumentos")
    exit()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', CSPort))
server.listen(20)  # max backlog of connections


while True:
    client_socket, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    connectionClosed = False
    while not connectionClosed:
        connectionClosed = authenticate(client_socket, address)
