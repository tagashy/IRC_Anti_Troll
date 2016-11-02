from socket import *
import thread
import time
import message_parsing
from config import *
from commands import *


def recv_loop(sock):
    try:
        while (1):
            res = sock.recv(1024)
            if "PING" in res.split(" ")[0]:
                sock.send(res.replace("PING", "PONG"))
            elif res.strip() != "":
                if "353" in res:
                    create_list_of_user(res)
                else:
                    pseudo, message, msg_type = message_parsing.parse_msg(res)
                    command_loop(pseudo, message, msg_type, sock)
                    if message != "NONE":
                        print "[" + msg_type + "]", "USER:", pseudo, "send:", message
    except:
        pass


def send_loop(sock, target):
    while (1):
        exp = raw_input("enter python express:")
        if exp.strip() == "new target":
            target = raw_input("enter target:").strip()
        elif exp.strip() == "end":
            break
        else:
            exec ("tmp=" + exp)
            sock.send("PRIVMSG " + target + " :" + tmp + "\r\n")


def init_bot():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("irc.root-me.org", 6667))
    thread.start_new_thread(recv_loop, (sock,))
    sock.send("USER " + bot_name + " Bot Bot Bot\r\n")
    sock.send("NICK " + bot_name + "\r\n")
    print "[!] Authentification send"
    time.sleep(2)
    sock.send("JOIN " + channel + "\r\n")
    print "[!] Join " + channel + " send"
    send_loop(sock, "Tagashy")
    sock.send("QUIT : va faire une revision\r\n")
    time.sleep(1)
    sock.close()
