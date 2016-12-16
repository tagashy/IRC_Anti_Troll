from __future__ import unicode_literals

from socket import timeout

import Bot_log
import message_parsing
import mythread
import utils
from Users_List import USERLIST
from config import config


class IRC(mythread.Thread):
    def __init__(self, addr, channel, port, bot_name, sock=None):
        mythread.Thread.__init__(self)
        self.server = addr
        self.channel = channel
        self.port = port
        self.name = bot_name
        self.pseudo = None
        logname = utils.clean("{}_{}.log".format(self.server, self.channel))
        self.log = Bot_log.Log(logname)
        self.sock = sock

    def last_seen(self, username):
        for user in self.users:
            if username == user.username:
                return user.lastSeen, user.digiTime, user.actif
        return -1, -1, -1

    def update_user_last_seen(self, pseudo):
        if USERLIST.update_user(pseudo, "{}:{}".format(self.server, self.port), self.channel) < 1:
            USERLIST.add_user(pseudo, "{}:{}".format(self.server, self.port), self.channel)

    def add_user(self, pseudo):
        USERLIST.add_user(pseudo, "{}:{}".format(self.server, self.port), self.channel)
        return

    def deactivate_user(self, pseudo):
        USERLIST.deactivate_user(pseudo)

    def end(self):
        self.sock.send("QUIT : \r\n")
        self.sock.close()
        exit(0)

    def init(self):
        if self.sock is None:
            self.users, self.sock = utils.create_irc_socket(self.server, self.name, self.channel, self.port)
            if self.sock == -1:
                self.error = "Throttled"
                exit(-1)
            elif self.sock == -2:
                self.error = "Registration timeout"
                exit(-2)
            elif self.sock == -3:
                self.error = "Link closed"
                exit(-3)
            utils.print_message("[!] Initialisation of Bot done")
        self.started = True
        self.IRC_init()
        print ("[!] Starting {} on server {}:{} in channel {}".format(self.name, self.server, self.port, self.channel))

    def IRC_init(self):
        pass

    def main(self):
        self.sock.settimeout(2)
        while (1):
            if self.stopped():
                self.end()
            try:
                res = self.sock.recv(1024).decode('utf-8', errors='replace')
                for line in res.split("\r\n"):
                    if "PING" in line:
                        self.sock.send(line.replace("PING", "PONG") + "\r\n")
                    elif line.strip() != "":
                        if config.debug:
                            print (line)
                            self.log.write(res)
                        pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                        self.update_user_last_seen(pseudo)
                        if msg_type == "PART":
                            self.deactivate_user(pseudo)
                            self.user_part(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "QUIT":
                            self.deactivate_user(pseudo)
                            self.user_quit(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "JOIN":
                            self.add_user(pseudo)
                            self.user_join(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "PRIVMSG":
                            self.update_user_last_seen(pseudo)
                            self.user_privmsg(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "PUBMSG":
                            self.update_user_last_seen(pseudo)
                            self.user_pubmsg(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "KICK":
                            self.deactivate_user(pseudo)
                            self.user_kick(pseudo, user_account, ip, msg_type, content, target)
                        elif msg_type == "BAN":
                            self.deactivate_user(pseudo)
                            self.user_ban(pseudo, user_account, ip, msg_type, content, target)

            except timeout:
                pass

    def user_join(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_privmsg(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_pubmsg(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_quit(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_part(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_ban(self, pseudo, user_account, ip, msg_type, content, target):
        pass

    def user_kick(self, pseudo, user_account, ip, msg_type, content, target):
        pass
