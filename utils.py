import re
from socket import *

from config import config
from user import User

if config.log:
    import Bot_log

    log = Bot_log.Log()


def create_irc_socket(addr, bot_name, channel, port=6667):
    name_list_reg = re.compile("(?<= 353 " + bot_name + " = " + channel + " :).*")
    if config.debug:
        print_message("(?<= 353 " + bot_name + " = " + channel + " :).*")
    users = []
    recv_sock = socket(AF_INET, SOCK_STREAM)
    recv_sock.connect((addr, port))
    recv_sock.send("USER " + bot_name + " Bot Bot Bot\r\n")
    recv_sock.send("NICK " + bot_name + "\r\n")
    res = ""
    print_message("[!] Authentification to " + addr + " send")
    recv_sock.settimeout(2)
    try:
        while 1:
            res = recv_sock.recv(1024)
            if config.debug:
                print_message(res)
            if "[Throttled]" in res:
                print_message("[W] Unable to register because of throttled connection")
                return -1, -1
            elif "[Registration timeout]" in res:
                print_message("[W] Unable to register because of Registration Timeout")
                return -1, -2
            elif "ERROR :Closing link:" in res:
                print_message("[W] Unable to register because host close the link")
                return -1, -3


    except timeout:
        recv_sock.send("JOIN " + channel + "\r\n")
        recv_sock.settimeout(None)
        print_message("[!] Join " + channel + " send")

    while " 366 " not in res:
        res = recv_sock.recv(1024)
        if config.debug:
            print_message(res)
        if " 353 " in res:
            print_message("[!] creation of user list")
            users += parse_name_list(res, name_list_reg,channel,addr)
            if config.debug:
                print_message("[D] users of channel {}:{}".format(channel, users))
    return users, recv_sock


def print_message(message, msg_type="STDIN", sock=None, pseudo=None, channel=None):
    if msg_type == "PRIVMSG":
        send_private_message(message, pseudo, sock)
    elif msg_type == "PUBMSG":
        send_private_message(message, channel, sock)
    elif msg_type == "STDIN":
        print message
    if config.log:
        log.write(message)


def send_public_message(message, sock):
    sock.send("PRIVMSG " + config.main_channel + " :" + message + "\r\n")


def send_private_message(message, pseudo, sock):
    sock.send("PRIVMSG " + pseudo + " :" + message + "\r\n")


def parse_name_list(msg, name_list_reg,channel="UNKNOWN",server="UNKNOWN"):
    name_list_res = name_list_reg.search(msg)
    if name_list_res:
        name_list = name_list_res.group(0)
        names = name_list.split()
        users = []
        for name in names:
            users.append(User(name,channel,server))
        return users


def cut_at_cara(string, c):
    index = string.find(c)
    if index != -1:
        return string[index + 1:]
    else:
        return string
