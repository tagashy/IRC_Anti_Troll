from socket import *
from config import *
from message_parsing import parse_name_list


def create_irc_socket(addr, bot_name, channel, port=6667):
    users=""
    recv_sock = socket(AF_INET, SOCK_STREAM)
    recv_sock.connect((addr, port))
    recv_sock.send("USER " + bot_name + " Bot Bot Bot\r\n")
    recv_sock.send("NICK " + bot_name + "\r\n")
    print "[!] Authentification send"
    recv_sock.settimeout(5)
    try:
        while 1:
            res = recv_sock.recv(1024)
            if "353" in res:
                print "[!] creation of user list"
                users = parse_name_list(res)
            if debug:
                print res
    except:
        recv_sock.settimeout(None)
        recv_sock.send("JOIN " + channel + "\r\n")
        print "[!] Join " + channel + " send"
    return users,recv_sock
