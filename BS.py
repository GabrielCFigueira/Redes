import socket
import sys
import os
import signal

i = 0
BSport = 59000
CSname = socket.gethostname()
CSport = 58037
userCredentials = { "86420" : "12345678" }

def sigInt_handler(signum,frame):
    global server
    server.close()
    exit()

signal.signal(signal.SIGINT,sigInt_handler)

if(len(sys.argv) != 1):
    while(i<len(sys.argv)):
        if(sys.argv[i]=="-b"):
            BSport = sys.argv[i+1]
        if(sys.argv[i]=="-n"):
            CSname = sys.argv[i+1]
        if(sys.argv[i]=="-p"):
            CSport = sys.argv[i+1]
        i=i+1

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', BSport))
server.listen(20)

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
    return False


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request.decode()))
    client_socket.send('ACK!'.encode())
    client_socket.close()
    #exit()

while True:
    #while i<2:
    client_sock, address = server.accept()
    print('Accepted connection from {}:{}'.format(address[0], address[1]))
    #    i=i+1
    #    pid=os.fork()
    #    if pid==0:
    handle_client_connection(client_sock)