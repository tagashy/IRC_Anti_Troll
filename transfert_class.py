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
        self.error=None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def send_message(self, message):
        if self.pseudo is not None:
            send_private_message(message, self.pseudo, self.send_sock)
        else:
            send_public_message(message, self.send_sock)

    def run(self):
        invisible_cara=31#caracter to escape highlights
        self.users, self.recv_sock = utils.create_irc_socket(self.addr, self.name, self.channel, self.port)
        if self.recv_sock == -1:
            self.error="Throttled"
            exit(-1)
        elif self.recv_sock == -2:
            self.error = "Registration timeout"
            exit(-2)
        elif self.recv_sock == -3:
            self.error = "Link closed"
            exit(-3)
        print_message( "[!] Initialisation of tranfert done")
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
                        print_message( res)
                    user, user_account, ip, msg_type, message, target = new_parsing(res)
                    if msg_type == "PUBMSG":

                        self.send_message(
                            chr(3) + str(
                                self.couleur) + self.channel + " : " + user + ">" + message,
                        )
                    elif msg_type == "PRIVMSG":
                        self.send_message(
                            chr(3) + str(self.couleur) + "Private message from user " + user[0:1] + chr(invisible_cara) + user[
                                                                                                                1:] + ">" + message)
                    elif msg_type == "JOIN":
                        self.users.append(user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user[0:1] + chr(invisible_cara) + user[
                                                                                           1:] + " has join channel")
                    elif msg_type == "QUIT":
                        self.users.remove(user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user[0:1] + chr(invisible_cara) + user[
                                                                                           1:] + " has quit server with msg : " + message)
                    elif msg_type == "PART":
                        if user in self.users:
                            self.users.remove(user)
                        elif "@"+user in self.users:
                            self.users.remove("@"+user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user[0:1] + chr(invisible_cara) + user[
                                                                                           1:] + " has quit channel with msg : " + message)

            except timeout:
                pass
