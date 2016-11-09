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
        self.bot_name = bot_name
        self.pseudo = pseudo
        self.send_sock = send_sock
        self.recv_sock = None
        self.couleur = couleur
        self.users = None
        self.started = False

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def send_message(self, message):
        if self.pseudo is not None:
            self.send_message(message, self.pseudo, self.send_sock)
        else:
            send_public_message(message, self.send_sock)

    def run(self):
        self.users, self.recv_sock = utils.create_irc_socket(self.addr, self.bot_name, self.channel, self.port)
        print "[!] Initialisation of tranfert done"
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
                        print res
                    user, user_account, ip, msg_type, message, target = new_parsing(res)
                    if msg_type == "PUBMSG":

                        self.send_message(
                            chr(3) + str(
                                self.couleur) + self.channel + " : " + user + ">" + message,
                        )
                    elif msg_type == "PRIVMSG":
                        self.send_message(
                            chr(3) + str(self.couleur) + "Private message from user " + user + ">" + message)
                    elif msg_type == "JOIN":
                        self.users.append(user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user + " has join channel")
                    elif msg_type == "QUIT":
                        self.users.remove(user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user + " has quit server with msg : " + message)
                    elif msg_type == "PART":
                        self.users.remove(user)
                        self.send_message(
                            chr(3) + str(self.couleur) + "User " + user + " has quit channel with msg : " + message)

            except:
                pass
