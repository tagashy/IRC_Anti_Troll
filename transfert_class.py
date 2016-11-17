import threading

import utils
from commands import *
from message_parsing import *


class Transferrer(threading.Thread):
    def __init__(self, addr, channel, port, bot_name, send_sock, pseudo=None, couleur=2):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.addr = addr
        self.channel = channel
        self.port = port
        self.name = bot_name
        self.pseudo = pseudo
        self.send_sock = send_sock
        self.recv_sock = None
        self.couleur = couleur
        self.users = None
        self.started = False
        self.error = None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def send_message(self, message):
        if self.pseudo is not None:
            send_private_message(message, self.pseudo, self.send_sock)
        else:
            send_public_message(message, self.send_sock)

    def last_seen(self, username):
        for user in self.users:
            if username == user.username:
                return user.lastSeen,user.digiTime
        return -1,-1

    def update_user_last_seen(self, pseudo):
        for user in self.users:
            if pseudo == user.username:
                user.update_last_seen()
                break

    def run(self):
        invisible_cara = 07  # caracter to escape highlights
        self.users, self.recv_sock = utils.create_irc_socket(self.addr, self.name, self.channel, self.port)
        if self.recv_sock == -1:
            self.error = "Throttled"
            exit(-1)
        elif self.recv_sock == -2:
            self.error = "Registration timeout"
            exit(-2)
        elif self.recv_sock == -3:
            self.error = "Link closed"
            exit(-3)
        print_message("[!] Initialisation of tranfert done")
        self.recv_sock.settimeout(2)
        self.started = True
        while 1:
            if self.stopped():
                self.recv_sock.send("QUIT : s'enfuis\r\n")
                self.recv_sock.close()
                exit(0)
            try:
                res = self.recv_sock.recv(1024)
                if "PING" in res.split(" ")[0]:
                    self.recv_sock.send(res.replace("PING", "PONG"))
                elif res.strip() != "":
                    if config.debug:
                        print_message(res)
                    pseudo, user_account, ip, msg_type, message, target = new_parsing(res)
                    if msg_type == "PUBMSG":
                        self.update_user_last_seen(pseudo)
                        self.send_message(
                            chr(3) + str(
                                self.couleur) + self.channel + " : " + pseudo + ">" + message,
                        )
                    elif msg_type == "PRIVMSG":
                        self.update_user_last_seen(pseudo)
                        self.send_message(
                            chr(3) + str(self.couleur) + "Private message from user " + pseudo[0:1] + chr(
                                invisible_cara) + pseudo[
                                                  1:] + ">" + message)
                    elif msg_type == "JOIN":
                        self.users.append(pseudo)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                                       1:] + " has join channel")
                    elif msg_type == "QUIT":
                        if pseudo in self.users:
                            self.users.remove(pseudo)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                                       1:] + " has quit server with msg : " + message)
                    elif msg_type == "PART":
                        if pseudo in self.users:
                            self.users.remove(pseudo)
                        elif "@" + pseudo in self.users:
                            self.users.remove("@" + pseudo)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + pseudo[0:1] + chr(invisible_cara) + pseudo[
                                                                                                       1:] + " has quit channel with msg : " + message)

            except timeout:
                pass
