from socket import *
import thread
import time
import message_parsing
from config import *
from commands import *
from command_class import *
import utils

cmds = commands_init()


def recv_loop(sock, bot_name, channel):
    public_content_reg, private_content_reg = init_parsing_channel(bot_name, channel)
    while (1):
        res = sock.recv(1024)
        if "PING" in res.split(" ")[0]:
            sock.send(res.replace("PING", "PONG"))
        elif res.strip() != "":
            pseudo, message, msg_type = message_parsing.parse_msg(res, public_content_reg,
                                                                  private_content_reg, bot_name, channel)
            command_loop(pseudo, message, msg_type, sock, cmds)
            if message != "NONE":
                print "[" + msg_type + "]", "USER:", pseudo, "send:", message


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
    users, sock = utils.create_irc_socket(main_server, bot_name, channel, main_port)
    thread.start_new_thread(recv_loop, (sock, bot_name, channel))
    send_loop(sock, "Tagashy")
    sock.send("QUIT : va faire une revision\r\n")
    sock.close()


init_bot()
