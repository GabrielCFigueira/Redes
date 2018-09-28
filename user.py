#!/usr/bin/env python3
from abstraction_util import *
from datetime import datetime

import sys
import socket
import os

CSname = socket.gethostname()
CSport = DEFAULT_PORT_CS
user=""
passwd=""
flag_AUT=0
backup_path=""

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
    global user, passwd, flag_AUT, backup_path

    response = client.recv(4096).decode()
    err_messages(response)
    responses = response.split()

    print(response)

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
        print("Logged out")
        client.close()
    elif responses[0]=="BKR":
        BSName = responses[1]
        BSPort = responses[2]
        N_files = responses[3]
        client.close()

        BSClient=creatClient()
        BSClient.connect((BSName, BSPort))

        send_message("UPL " + backup_path + " " + N_files, BSClient)

        BSresponse = client.recv(4096).decode()

        i=4
        files_to_print=""
        while i+4 <= len(responses):
            filename = os.path.join(directory, responses[i])
            file_size = os.path.getsize(filename)
            file_datetime = os.path.getmtime(filename)
            string = filename
            string+= " " + datetime.fromtimestamp(file_datetime).strftime('%d.%m.%Y %H:%M:%S')
            string+= " " + str(file_size)
            files_to_print += " " + filename

            file = open(backup_path+"\\"+filname, "r") 
            string+=file.read().encode()
            file.close()

            i=i+4
            send_message(string.encode(), BSClient)

        response = client.recv(4096).decode()
        if response=="UPR OK":
            print("completed - " + backup_path + files_to_print)
        
        backup_path=""
        BSClient.close()
        
        elif response=='DDR OK\n':
            print("Deleted")
            reset_flag_AUT()
            client.close()
            
        elif response=='DDR NOK\n':
            print("Not Deleted")
            reset_flag_AUT()
            client.close()


#---------------------------------------------------------------
def read_command():
    global user, passwd, flag_AUT, backup_path
    while True:
        command = input("> ")
        commands = command.split()

        if get_field(commands,0)=="exit":
            break
        
        #***** LOGIN *****
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

        #***** DELUSER *****
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

        #***** LOGOUT *****
        elif get_field(commands,0)=="logout":
            if user == "" and passwd == "":
                err_messages("ERR AUT\n")
            else:
                user=""
                passwd=""
                reset_flag_AUT()
        
        #***** BACKUP *****
        elif get_field(commands,0)=="backup":
            if flag_AUT==0:
                client=creatClient()
                connect_TCP(client)
                send_message("AUT "+user+" "+passwd+"\n", client)
                receive_message(client)

            directory = get_field(commands,1)
            n_files = len(os.listdir(directory))

            string = US_CS_BCK + " " + directory + " " + str(n_files)
            if os.path.isdir(directory):
                for file in os.listdir(directory):
                    filename = os.path.join(directory, file)
                    file_size = os.path.getsize(filename)
                    file_datetime = os.path.getmtime(filename)
                    string+= " " + file
                    string+= " " + datetime.fromtimestamp(file_datetime).strftime('%d.%m.%Y %H:%M:%S')
                    string+= " " + str(file_size)
            
            print(string)
            send_message( string + "\n", client)
            backup_path=directory
            receive_message(client)
            reset_flag_AUT()

        #***** RESTORE *****
        elif get_field(commands,0)=="restore":
            if flag_AUT==0:
                client=creatClient()
                connect_TCP(client)
                send_message("AUT "+user+" "+passwd+"\n", client)
                receive_message(client)
            send_message(US_CS_RST + " " + get_field(commands,1) + "\n", client)
            receive_message(client)
            reset_flag_AUT()

        #***** DIRLIST *****
        elif get_field(commands,0)=="dirlist":
            if flag_AUT==0:
                client=creatClient()
                connect_TCP(client)
                send_message("AUT "+user+" "+passwd+"\n", client)
                receive_message(client)
            send_message(US_CS_LSD, client)
            receive_message(client)
            reset_flag_AUT()

        #***** FILELIST *****
        elif get_field(commands,0)=="filelist":
            if flag_AUT==0:
                client=creatClient()
                connect_TCP(client)
                send_message("AUT "+user+" "+passwd+"\n", client)
                receive_message(client)
            send_message(US_CS_LSF + " " + get_field(commands,1) + "\n", client)
            receive_message(client)
            reset_flag_AUT()

        #***** DELETE *****
        elif get_field(commands,0)=="delete":
            if flag_AUT==0:
                client=creatClient()
                connect_TCP(client)
                send_message("AUT "+user+" "+passwd+"\n", client)
                receive_message(client)
            send_message(US_CS_DEL + " " + get_field(commands,1) + "\n", client)
            receive_message(client)
            reset_flag_AUT()



input_command()
read_command()
exit()
