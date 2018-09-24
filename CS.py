#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket
import os
import signal
import threading

CSPort = DEFAULT_PORT_CS

userCredentials = { "86420" : "12345678" } # dictionary of user ids with their respective passwords


def sigInt_handler(signum,frame):
    global server
    server.close()
    exit()

signal.signal(signal.SIGINT,sigInt_handler)

def createUser(istid, password):
    userCredentials[istid] = password

def printRequirement(istid, address, requestType, directory = ''):
    print("User:" + istid + " Requirement:" + requestType + "\nIP:" + str(address[0]) + " Port:" + str(address[1]))

def authenticate(client_socket, adress):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.close()
    elif messages[0] != "AUT":
        client_socket.send("ERR AUT\n".encode())
    else:
        istid = messages[1]
        password = messages[2]
        printRequirement(istid, address, "AUT")
        if istid in userCredentials:
            if userCredentials[istid] == password:
                client_socket.send(US_CS_AUR_OK.encode())
                return handle_client_connection(client_socket, istid, address)
            else:
                client_socket.send(US_CS_AUR_NOK.encode())
                #client_socket.close()
        else:
            client_socket.send(US_CS_AUR_NEW.encode())
            createUser(istid, password)
            handle_client_connection(client_socket, istid, address)


def handle_client_connection(client_socket, istid, address):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.close()
    requirement = messages[0]
    if requirement == "DLU":
        printRequirement(istid, address, "DLU")
        del(userCredentials[istid])
        client_socket.send(US_CS_DLR_OK.encode())

""" elif requirement == "BCK":
    elif requirement == "RST":
    elif requirement == "LSD":
    elif requirement == "LSF":
    elif requirement == "DEL":      """

    #exit()


class UDP:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.state = 0



if len(sys.argv) == 3 and sys.argv[1] == "-p":
    CSPort = eval(sys.argv[2])
elif len(sys.argv) > 1:
    raise ValueError("numero errado de argumentos")
    exit()


UDPWriter, UDPReader = os.pipe()

if os.fork() == 0:
    os.close(UDPReader)
    UDPWriter = os.fdopen(UDPWriter, 'w')
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind(('', CSPort))
    while True:

        bytesAddressPair = server.recvfrom(1024)

        message = bytesAddressPair[0].decode()
        UDPWriter.write(message)
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        # Sending a reply to client

        server.sendto("RGR OK".encode(), address)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', CSPort))
server.listen(20)  # max backlog of connections

PipeList = []
BSList = []

mutex = threading.Lock()
def thread():
    os.close(UDPWriter)
    UDPReader = os.fdopen(UDPReader)
    while True:
        message = UDPReader.read()
        messages = message.split()
        BS = UDP(messages[1], messages[2])
        BSList += [BS]
        mutex.acquire()
        for e in PipeList:
            e.write(message)
        mutex.release()



while True:
    client_socket, address = server.accept()
    leitorEscravo, escritorMestre = os.pipe()
    mutex.acquire()
    PipeList += [escritorMestre]
    mutex.release()
    if os.fork() == 0:

        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        connectionClosed = False
        connectionClosed = authenticate(client_socket, address)
        exit()
