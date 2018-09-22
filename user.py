#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket

CSname = socket.gethostname()
CSport = 58037

user=""
passwd=""

def input_command():
    if len(sys.argv)==3:
        if get_field(sys.argv,1)=="-n":
            flagCSname = get_field(sys.argv,1)
            CSname = get_field(sys.argv,2)
        elif get_field(sys.argv,1)=="-p":
            flagCSport = get_field(sys.argv,1)
            CSport = eval(get_field(sys.argv,2))

    elif len(sys.argv)==5:
        flagCSname = get_field(sys.argv,1)
        CSname = get_field(sys.argv,2)
        flagCSport = get_field(sys.argv,3)
        CSport = eval(get_field(sys.argv,4))

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
    if get_field(response_list,0)=="ERR":
        err_messages(get_field(response_list,1))

def read_command():
    command = ""
    while command != "exit":
        command = input()
        commands = command.split()

        if get_field(commands,0)=="login":
            if len(commands)!=3:
                err_messages("AUT")
            else:
                connect_TCP()
                send_message("AUT "+get_field(commands,1)+" "+get_field(commands,2)+"\n")
                receive_message()

        elif get_field(commands,0)=="deluser":
            send_message("DLU\n")
            receive_message()

input_command()
read_command()
exit()
