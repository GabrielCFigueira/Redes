DEFAULT_PORT_CS = 58041
DEFAULT_PORT_BS = 59000

US_CS_AUR_OK = 'AUR OK\n'
US_CS_AUR_NOK = 'AUR NOK\n'
US_CS_AUR_NEW = 'AUR NEW\n'

US_CS_DLU = 'DLU\n'

US_CS_DLR_OK = 'DLR OK\n'
US_CS_DLR_NOK = 'DLR NOK\n'

US_CS_BCK = 'BCK'

US_CS_RST = 'RST'

US_CS_LSD = 'LSD\n'

US_CS_LSF = 'LSF'

US_CS_DEL = 'DEL'

def get_field(list, pos):
    return list[pos]

def addToDict(dict, key, value):
    dict[key] = value

def removeFromDict(dict, key):
    del(dict[key])


def receive_string(client):
  string = ""
  char = ""
  while char != "\n":
     char = client.recv(1).decode()
     string += char
  string += "\n"
  return string


def err_messages(flag):
    if flag=="ERR AUT\n":
        print("Para se autenticar tem que executar: login user pass")
    elif flag=="ERR_login":
        print("Já efectuou um login")
    elif flag=="AUR NOK\n":
        print("Erro na pass tente novamente com: login user pass")
