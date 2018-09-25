#!/usr/bin/env python3
from abstraction_util import *

import sys
import socket

CSname = socket.gethostname()
CSport = DEFAULT_PORT_CS
user=""
passwd=""
flag_AUT=0

#---------------------------------------------------------------
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
#---------------------------------------------------------------
def creatClient():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def connect_TCP(client):
    client.connect((CSname, CSport))

def send_message(message, client):
    client.send(message.encode())

def receive_message(client):
    global user, passwd, flag_AUT

    response = client.recv(4096).decode()
    err_messages(response)

    if response==US_CS_AUR_OK:
        if flag_AUT==2:
            print("Logged in")
        flag_AUT=1
    elif response==US_CS_AUR_NOK:
        user = ""
        passwd = ""
        reset_flag_AUT()
        client.close()
    elif response==US_CS_AUR_NEW:
        print("User \"" + user + "\" created")
        reset_flag_AUT()
        client.close()
    elif response==US_CS_DLR_OK:
        print("User deleted")
        reset_flag_AUT()
        client.close()
    elif response=="EXI\n":
        client.close()

#---------------------------------------------------------------
def read_command():
    global user, passwd, flag_AUT
    while True:
        command = input("> ")
        commands = command.split()

        if get_field(commands,0)=="exit":
            break

        elif get_field(commands,0)=="login":
            if user == "" and passwd == "":
                if len(commands)!=3:
                    err_messages("AUT")
                else:
                    flag_AUT=2
                    client=creatClient()
                    connect_TCP(client)
                    user=get_field(commands,1)
                    passwd=get_field(commands,2)
                    send_message("AUT "+user+" "+passwd+"\n", client)
                    receive_message(client)
            else:
                err_messages("ERR_login")

        elif get_field(commands,0)=="deluser":
            if user == "" and passwd == "":
                err_messages("ERR AUT\n")
            else:
                if flag_AUT==0:
                    client=creatClient()
                    connect_TCP(client)
                    send_message("AUT "+user+" "+passwd+"\n", client)
                    receive_message(client)
                send_message(US_CS_DLU, client)
                receive_message(client)
                user=""
                passwd=""
                reset_flag_AUT()

        elif get_field(commands,0)=="logout":
            if user == "" and passwd == "":
                err_messages("ERR AUT\n")
            else:
                if flag_AUT==0:
                    client=creatClient()
                    connect_TCP(client)
                    send_message("AUT "+user+" "+passwd+"\n", client)
                send_message("EXI\n", client)
                receive_message(client)
                user=""
                passwd=""
                reset_flag_AUT()



input_command()
read_command()
exit()
