def get_field(list, pos):
    return list[pos]

def err_messages(flag):
    if flag=="AUT":
        print("Para se autenticar tem que executar: login user pass")
    elif flag=="ERR_login2":
        print("Já efectuou um login")