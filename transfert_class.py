from __future__ import unicode_literals

import Irc_Class
from commands import *
from message_parsing import *


class Transferrer(Irc_Class.IRC):
    def __init__(self, server, channel, port, bot_name, send_sock, original_chan, pseudo=None, couleur=2):
        Irc_Class.IRC.__init__(self, server, channel, port, bot_name)
        self.pseudo = pseudo
        self.send_sock = send_sock
        self.couleur = couleur
        self.original_chan = original_chan
        self.invisible_cara = u"\u200B"

    def send_message(self, message):
        if self.pseudo is not None:
            send_private_message(chr(3) + str(self.couleur) + message, self.pseudo, self.send_sock)
        else:
            send_private_message(chr(3) + str(self.couleur) + message, self.original_chan, self.send_sock)

    def user_join(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "User " + pseudo[0:1] + self.invisible_cara + pseudo[1:] + " has join channel " + self.channel
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_part(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "User " + pseudo[0:1] + self.invisible_cara + pseudo[1:] + " has quit channel with msg : " + content
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_pubmsg(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = self.channel + " : " + pseudo[0:1] + self.invisible_cara + pseudo[1:] + ">" + content
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_privmsg(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "Private message from user " + pseudo[0:1] + self.invisible_cara + pseudo[1:] + ">" + content
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_quit(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "User " + pseudo[0:1] + self.invisible_cara + pseudo[1:] + " has quit server with msg : " + content
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_kick(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "User " + pseudo[0:1] + self.invisible_cara + pseudo[
                                                                 1:] + " has been kicked from channel " + self.channel
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)

    def user_ban(self, pseudo, user_account, ip, msg_type, content, target):
        self.add_user(pseudo)
        send_res = "User " + pseudo[0:1] + self.invisible_cara + pseudo[
                                                                 1:] + " has has been banned channel " + self.channel
        self.send_message(send_res)
        if config.debug:
            self.log.write(send_res)
