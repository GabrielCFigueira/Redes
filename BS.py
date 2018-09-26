import socket
import sys
import os
import signal
import multiprocessing

i = 0
BSport = 59000
CSname = socket.gethostname()
CSport = 58037
global userCredentials
userCredentials = { "86420" : "12345678" }
bufferSize   = 1024
msgFromClient=""
manager = multiprocessing.Manager()
userCredentials = manager.dict()


if(len(sys.argv) != 1):
    while(i<len(sys.argv)):
        if(sys.argv[i]=="-b"):
            BSport = eval(sys.argv[i+1])
        if(sys.argv[i]=="-n"):
            CSname = sys.argv[i+1]
        if(sys.argv[i]=="-p"):
            CSport = eval(sys.argv[i+1])
        i=i+1

def UDP_Client(msgFromClient):
    global UDPClientSocket
    bytesToSend         = str.encode(msgFromClient)
    serverAddressPort   = (socket.gethostbyname(CSname), CSport)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode()
    print(msgFromServer)
    UDPClientSocket.close()

def UDP_Server():
    global UDP_Server
    UDP_Server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_Server.bind(('', BSPort))
    while True:

        message, address = UDP_Server.recvfrom(1024)
        ip, port = address
        message = message.decode().split()
        if message[0] == "LSF":
            userID = message[1]
            dirName = message[2]
            UDP_Server.sendto("LFD".encode(), (ip, port))
        elif message[0] == "LSU":
            addToDict(userCredentials,message[1],message[2])
            UDP_Server.sendto("LUR OK".encode(), (ip,port))

        clientIP  = "Client IP Address:{}".format(ip)

        print(clientIP + " " + str(port))

        # Sending a reply to client


def addToDict(dict, key, value):
    dict[key] = value

def sigInt_handler(signum,frame):
    #global server
    #server.close()
    msgFromClient = "UNR " + socket.gethostbyname(socket.gethostname()) + " " + str(BSport)
    UDP_Client(msgFromClient)
    exit(0)

signal.signal(signal.SIGINT,sigInt_handler)


def printRequirement(istid, address, requestType, directory = ''):
    print("User:" + istid + " Requirement:" + requestType + "\nIP:" + str(address[0]) + " Port:" + str(address[1]))


def TCP_Server(client_socket, adress, userCredentials):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.send("EXI\n".encode())
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

def handle_client_connection(client_socket, istid, address):
    message = client_socket.recv(1024).decode()
    messages = message.split()
    if len(messages) == 0 or messages[0] == "EXI":
        client_socket.send("EXI\n".encode())
        client_socket.close()
        exit(0)
    requirement = messages[0]
    """
    if requirement == "DLU":
        printRequirement(istid, address, "DLU")
        del(userCredentials[istid]) #replace with abstraction func
        client_socket.send(US_CS_DLR_OK.encode())

     elif requirement == "UPL":
    elif requirement == "RSB":  """

    client_socket.close()


msgFromClient = "REG " + socket.gethostbyname(socket.gethostname()) + " " + str(BSport)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPProcess = multiprocessing.Process(target=UDP_Client, args=(msgFromClient,))
UDPProcess.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', BSport))
server.listen(20)

while True:
    client_socket, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    TCPProcess = multiprocessing.Process(target=TCP_Server, args=(client_socket,address, userCredentials))
    TCPProcess.start()