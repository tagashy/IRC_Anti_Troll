from __future__ import unicode_literals

import Irc_Class
import user_class
from commands import *
from message_parsing import *


class Transferrer(Irc_Class.IRC):
    def __init__(self, server, channel, port, bot_name, send_sock, original_chan, pseudo=None, couleur=2):
        Irc_Class.IRC.__init__(self, server, channel, port, bot_name)
        self.pseudo = pseudo
        self.send_sock = send_sock
        self.couleur = couleur
        self.original_chan = original_chan

    def send_message(self, message):
        if self.pseudo is not None:
            send_private_message(chr(3) + str(self.couleur) + message, self.pseudo, self.send_sock)
        else:
            send_private_message(chr(3) + str(self.couleur) + message, self.original_chan, self.send_sock)

    def main_loop(self):
        invisible_cara = 07  # caracter to escape highlights
        self.sock.settimeout(2)
        while 1:
            if self.stopped():
                self.sock.send("QUIT : s'enfuis\r\n")
                self.sock.close()
                exit(0)
            try:
                res = self.sock.recv(1024).decode('utf-8', errors='replace')
                if "PING" in res.split(" ")[0]:
                    self.sock.send(res.replace("PING", "PONG"))
                elif res.strip() != "":
                    if config.debug:
                        print_message(res)
                    pseudo, user_account, ip, msg_type, message, target = new_parsing(res)
                    if msg_type == "PUBMSG":
                        self.update_user_last_seen(pseudo)
                        send_res = self.channel + " : " + pseudo[0:1] + chr(invisible_cara) + pseudo[1:] + ">" + message
                    elif msg_type == "PRIVMSG":
                        self.update_user_last_seen(pseudo)
                        send_res = "Private message from user " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                                      1:] + ">" + message
                    elif msg_type == "JOIN":
                        self.add_user(pseudo)
                        send_res = "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                 1:] + " has join channel " + self.channel
                    elif msg_type == "QUIT":
                        if pseudo in self.users:
                            self.deactivate_user(pseudo)
                        send_res = "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                 1:] + " has quit server with msg : " + message
                    elif msg_type == "PART":
                        if pseudo in self.users:
                            self.deactivate_user(pseudo)
                        elif "@" + pseudo in self.users:
                            self.deactivate_user("@" + pseudo)
                            send_res = "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                     1:] + " has quit channel with msg : " + message
                    self.send_message(send_res)
                    self.log.write(send_res)
                    if config.debug:
                        self.log.write(res)
            except timeout:
                pass
