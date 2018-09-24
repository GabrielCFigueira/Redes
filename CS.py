#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket
import os
import signal
import multiprocessing

CSPort = DEFAULT_PORT_CS

global userCredentials# dictionary of user ids with their respective passwords


def sigInt_handler(signum,frame):
    global server
    server.close()
    exit(0)

signal.signal(signal.SIGINT,sigInt_handler)

def addToDict(dict, key, value):
    dict[key] = value

def printRequirement(istid, address, requestType, directory = ''):
    print("User:" + istid + " Requirement:" + requestType + "\nIP:" + str(address[0]) + " Port:" + str(address[1]))

def TCPFunc(client_socket, adress, userCredentials, BSList):
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
                handle_client_connection(client_socket, istid, address)
            else:
                client_socket.send(US_CS_AUR_NOK.encode())
                client_socket.close()
        else:
            client_socket.send(US_CS_AUR_NEW.encode())
            addToDict(userCredentials, istid, password)
            client_socket.close()

def handle_client_connection(client_socket, istid, address):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.send("EXI\n".encode())
        client_socket.close()
    requirement = messages[0]
    if requirement == "DLU":
        printRequirement(istid, address, "DLU")
        del(userCredentials[istid]) #replace with abstraction func
        client_socket.send(US_CS_DLR_OK.encode())

    """ elif requirement == "BCK":
        elif requirement == "RST":
        elif requirement == "LSD":
        elif requirement == "LSF":
        elif requirement == "DEL":  """

    client_socket.close()


class UDP:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


"""
#UDPWriter, UDPReader = os.pipe()

    if os.fork() == 0:
    os.close(UDPReader)
    UDPWriter = os.fdopen(UDPWriter, 'w') """

def UDPFunc(BSList):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind(('', CSPort))
    while True:

        bytesAddressPair = server.recvfrom(1024)

        message = bytesAddressPair[0].decode()
        messages = message.split()
        BS = UDP(messages[1], messages[2])
        BSList += [BS]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)

        # Sending a reply to client

        server.sendto("RGR OK".encode(), address)


if len(sys.argv) == 3 and sys.argv[1] == "-p":
    CSPort = eval(sys.argv[2])
elif len(sys.argv) > 1:
    raise ValueError("numero errado de argumentos")
    exit()

manager = multiprocessing.Manager()
userCredentials = manager.dict()
userCredentials["86420"] = "12345678" #exemplo
BSList = manager.list(range(10))

UDPProcess = multiprocessing.Process(target=UDPFunc, args=(BSList,))
UDPProcess.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', CSPort))
server.listen(20)  # max backlog of connections

"""
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
"""



while True:
    client_socket, address = server.accept()
    #leitorEscravo, escritorMestre = os.pipe()
    #mutex.acquire()
    #PipeList += [escritorMestre]
    #mutex.release()
    #if os.fork() == 0:
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    TCPProcess = multiprocessing.Process(target=TCPFunc, args=(client_socket,
address, userCredentials, BSList))
    TCPProcess.start()
