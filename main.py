from socket import *
import thread
import time
import message_parsing
from config import *
from commands import *
from command_class import *
import utils
import threading


class bot(threading.Thread):
    def __init__(self, server, bot_name, channel, port):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.cmds = commands_init()
        self.users, self.sock = utils.create_irc_socket(server, bot_name, channel, port)
        self.public_content_reg, self.private_content_reg = init_parsing_channel(bot_name, channel)
        self.name = bot_name
        self.channel = channel
        self.server = server
        self.port = port

    def run(self):
        print "[!] Starting {} on server {}:{} in channel {}".format(self.name, self.server, self.port, self.channel)
        self.main_loop()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def end(self):
        self.sock.send("QUIT : va faire une revision\r\n")
        self.sock.close()
        exit(0)

    def main_loop(self):
        while (1):
            if self.stopped():
                self.end()
            res = self.sock.recv(1024)
            for line in res.split("\r\n"):
                if "PING" in line:
                    self.sock.send(line.replace("PING", "PONG")+"\r\n")
                elif line.strip() != "":
                    print line
                    # pseudo, message, msg_type = message_parsing.parse_msg(res, self.public_content_reg,self.private_content_reg, self.name,self.channel)
                    #full_username,\
                    pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                    # command_loop(pseudo, message, msg_type, self.sock, self.cmds)
                    command_loop(pseudo, content, msg_type, self.sock, self.cmds)
                    if content != "NONE":
                        print "[" + msg_type + "]", "USER:", pseudo, "send:", content


def recv_loop(sock, bot_name, channel):
    public_content_reg, private_content_reg = init_parsing_channel(bot_name, channel)
    while (1):
        res = sock.recv(1024)
        if "PING" in res.split(" ")[0]:
            sock.send(res.replace("PING", "PONG"))
        elif res.strip() != "":
            #pseudo, message, msg_type = message_parsing.parse_msg(res, public_content_reg, private_content_reg, bot_name, channel)
            full_username, pseudo, user_account, ip, msg_type, message, target = new_parsing(res)
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
    users, sock = utils.create_irc_socket(main_server, bot_name, main_channel, main_port)
    thread.start_new_thread(recv_loop, (sock, bot_name, main_channel))
    send_loop(sock, "Tagashy")
    sock.send("QUIT : va faire une revision\r\n")
    sock.close()


# init_bot()
TagaBot = bot(main_server, bot_name, main_channel, main_port)
TagaBot.start()
