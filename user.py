#!/usr/bin/env python3

import sys
import socket

flagCSname = sys.argv[1]
CSname = sys.argv[2]
flagCSport = sys.argv[3]
CSport = 58000+eval(sys.argv[4])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def printar(arg1, arg2, arg3, arg4):
    if(arg1=="-n"):
        print(arg2)
    if(arg3=="-p"):
        print(arg4)

def connect_TCP():
    client.connect((CSname, CSport))

def send_message(message):
    client.send(message.encode())

def receive_message():
    response = client.recv(4096)
    print(response.decode(), end='')

def read_command():
    command = ""
    while command != "exit":
        command = input()
        commands = command.split()

        if commands[0]=="login":
            connect_TCP()
            send_message(commands[1]+" "+commands[2]+"\n")
            receive_message()


read_command()
exit()
