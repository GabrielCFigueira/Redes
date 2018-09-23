#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket

CSname = socket.gethostname()
CSport = DEFAULT_PORT_CS
client = ""
user=""
passwd=""
flag_AUT=0

def creatClient():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def input_command():
    global flagCSname, CSname, flagCSport, CSport
    if len(sys.argv)==3:
        if get_field(sys.argv,1)=="-n":
            CSname = get_field(sys.argv,2)
        elif get_field(sys.argv,1)=="-p":
            CSport = eval(get_field(sys.argv,2))

    elif len(sys.argv)==5:
        CSname = get_field(sys.argv,2)
        CSport = eval(get_field(sys.argv,4))

def reset_flag_AUT():
    global flag_AUT
    flag_AUT=0

def printar(arg1, arg2, arg3, arg4):
    if arg1=="-n":
        print(arg2)
    if arg3=="-p":
        print(arg4)

def connect_TCP():
    global client
    client.connect((CSname, CSport))

def send_message(message):
    global client
    client.send(message.encode())

def receive_message():
    global client
    response = client.recv(4096)
    response_list = response.decode().split()
    if len(response_list) > 0:
        if get_field(response_list,0)=="ERR":
            err_messages(get_field(response_list,1))

def read_command():
    global user, passwd, flag_AUT, client
    command = ""
    while command != "exit":
        command = input()
        commands = command.split()

        if get_field(commands,0)=="login":
            if user == "" and passwd == "":
                if len(commands)!=3:
                    err_messages("AUT")
                else:
                    creatClient()
                    connect_TCP()
                    user=get_field(commands,1)
                    passwd=get_field(commands,2)
                    send_message("AUT "+user+" "+passwd+"\n")
                    receive_message()
                    flag_AUT=1
            else:
                err_messages("ERR_login2")

        elif get_field(commands,0)=="deluser":
            if user == "" and passwd == "":
                err_messages("AUT")
            else:
                if flag_AUT==0:
                    send_message("AUT "+user+" "+passwd+"\n")
                    receive_message()
                send_message(US_CS_DLU)
                receive_message()
                client.close()
                user=""
                passwd=""
                reset_flag_AUT()

        elif get_field(commands,0)=="logout":
            if user == "" and passwd == "":
                err_messages("AUT")
            else:
                send_message("EXI\n")
                receive_message()
                client.close()
                user=""
                passwd=""
                reset_flag_AUT()

input_command()
read_command()
exit()
