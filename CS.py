#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket
import os
import signal
import multiprocessing
import datetime

CSPort = DEFAULT_PORT_CS

global userCredentials# dictionary of user ids with their respective passwords


def sigInt_handler(signum,frame):
    global server
    server.close()
    exit(0)

signal.signal(signal.SIGINT,sigInt_handler)


def printRequirement(istid, address, requestType, directory = ''):
    print("User:" + istid + " Requirement:" + requestType + "\nIP:" + str(address[0]) + " Port:" + str(address[1]))

def TCPFunc(client_socket, adress, userCredentials, BSList):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.close()
        exit(0)
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
        exit(0)
    requirement = messages[0]
    if requirement == "DLU":
        printRequirement(istid, address, "DLU")
        removeFromDict(userCredentials, istid)
        client_socket.send(US_CS_DLR_OK.encode())

    elif requirement == "BCK":
        printRequirement(istid, address, "BCK")
        dir = Dir(messages[2], BSList[0])
        #register user in BS
        n_files = eval(messages[3])
        for e in range(n_files):
            name = messages[4 + e*4]
            date = messages[5 + e*4].split('.')
            time = messages[6 + e*4].split('.')
            size = eval(messages[7 + e*4])
            print(name + " " + messages[5 + e*4] + " " + messages[6 + e*4] + " " + str(size))
            date = datetime.date(date[2], date[1], date[0])
            time = datetime.time(time[2], time[1], time[0])
            file = File(name, date, time, size)
            dir.addFile(file)

        userCredentials[istid].addDir(dir)


    """ elif requirement == "RST":
        elif requirement == "LSD":
        elif requirement == "LSF":
        elif requirement == "DEL":  """

    client_socket.close()


class BS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port


class User:
    def __init__(self, istid, password):
        self.istid = istid
        self.password = password
        self.dirs = []
    def addDir(self, dir):
        self.dirs += [dir]
    def removeDir(self, dirName):
        for e in range(len(self.dirs)):
            if self.dirs[e].getName() == dirName:
                del(self.dirs[e])
    def getIstid(self):
        return self.istid
    def getPassword(self):
        return self.password



class Dir:
    def __init__(self, name, bs):
        self.name = name
        self.files = []
        self.bs = bs

    def getName(self):
        return self.name

    def getBS(self):
        return self.bs

    def addFile(self, file):
        self.files += [file]


#D = datetime.date(year, month, dia) to create date type
#H = datetime.time(hour, minutes, seconds) to create time type


class File:
    def __init__(self, name, date, time, size):
        self.name = name
        self.date = date
        self.time = time
        self.size = size

    def equals(self, file):
        return self.name == file.getName()

    def olderThan(self, file):
        if self.date > file.getDate():
            return True
        elif self.date < file.getDate():
            return False
        else:
            if self.time < file.getTime():
                return True
            else:
                return False

    def getName(self):
        return file.name

    def getDate(self):
        return self.date

    def getTime(self):
        return self.time

    def getSize(self):
        return self.size




"""
#UDPWriter, UDPReader = os.pipe()

    if os.fork() == 0:
    os.close(UDPReader)
    UDPWriter = os.fdopen(UDPWriter, 'w') """

def UDPFunc(BSList):
    global server
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind(('', CSPort))
    while True:

        message, address = server.recvfrom(1024)
        ip, port = address
        message = message.decode().split()
        if message[0] == "REG":
            bs = BS(ip, port)
            BSList += [bs]
            server.sendto("RGR OK".encode(), (ip, port))
        elif message[0] == "UNR":
            for e in range(len(BSList)):
                if BSList[e].getIp() == ip:
                    del(BSList[e])
            server.sendto("UAR OK".encode(), (ip,port))

        clientIP  = "Client IP Address:{}".format(ip)

        print(clientIP + " " + str(port))

        # Sending a reply to client


if len(sys.argv) == 3 and sys.argv[1] == "-p":
    CSPort = eval(sys.argv[2])
elif len(sys.argv) > 1:
    raise ValueError("numero errado de argumentos")
    exit()

manager = multiprocessing.Manager()
userCredentials = manager.dict()
userCredentials["86420"] = "12345678" #exemplo
BSList = manager.list()

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
