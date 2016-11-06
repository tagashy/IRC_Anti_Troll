from socket import *
from config import *
from message_parsing import parse_name_list,create_reg_user_list


def create_irc_socket(addr, bot_name, channel, port=6667):
    name_list_reg=create_reg_user_list(bot_name,channel)
    users=[]
    recv_sock = socket(AF_INET, SOCK_STREAM)
    recv_sock.connect((addr, port))
    recv_sock.send("USER " + bot_name + " Bot Bot Bot\r\n")
    recv_sock.send("NICK " + bot_name + "\r\n")
    print "[!] Authentification to "+addr+" send"
    recv_sock.settimeout(5)
    try:
        while 1:
            res = recv_sock.recv(1024)
            if debug:
                print res
            if "[Throttled]" in res:
                print "[W] Unable to register because of throttled connection"
                exit(0)
            elif "[Registration timeout]" in res:
                print "[W] Unable to register because of Registration Timeout"
                exit(0)
            elif "ERROR :Closing link:" in res:
                print "[W] Unable to register because host close the link"
                exit(0)

            if "353" in res:
                print "[!] creation of user list"
                users += parse_name_list(res,name_list_reg)

    except:
        recv_sock.settimeout(None)
        recv_sock.send("JOIN " + channel + "\r\n")
        print "[!] Join " + channel + " send"
    return users,recv_sock
