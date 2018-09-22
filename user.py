#!/usr/bin/env python3

import sys
import socket

CSname = socket.gethostname()
CSport = 58037

if len(sys.argv)==3:
    flagCSname = sys.argv[1]
    CSname = sys.argv[2]
elif len(sys.argv)==5:
    flagCSport = sys.argv[3]
    CSport = eval(sys.argv[4])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def printar(arg1, arg2, arg3, arg4):
    if arg1=="-n":
        print(arg2)
    if arg3=="-p":
        print(arg4)

def connect_TCP():
    client.connect((CSname, CSport))

def send_message(message):
    client.send(message.encode())

def receive_message():
    response = client.recv(4096)
    response_list = response.decode().split()
    if response_list[0]=="ERR":
        err_messages(response_list[1])

def err_messages(flag):
    if flag=="AUT":
        print("Para se autenticar tem que executar: login user pass")

def read_command():
    command = ""
    while command != "exit":
        command = input()
        commands = command.split()

        if commands[0]=="login":
            if len(commands)==3:
                err_messages("AUT")
            else:
                connect_TCP()
                send_message("AUT "+commands[1]+" "+commands[2]+"\n")
                receive_message()


read_command()
exit()
