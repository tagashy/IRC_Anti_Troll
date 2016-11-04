from commands import *
from message_parsing import *
import threading
import utils
class Transferrer(threading.Thread):
    def __init__(self, addr, channel, port, bot_name, send_sock, pseudo=None,couleur=2):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.addr = addr
        self.channel = channel
        self.port = port
        self.bot_name = bot_name
        self.pseudo = pseudo
        self.send_sock=send_sock
        self.recv_sock = None
        self.couleur=couleur
        self.users=None
    def stop(self):
        self._stop.set()


    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.users,self.recv_sock=utils.create_irc_socket(self.addr,self.bot_name,self.channel,self.port)
        pub_reg, priv_reg = init_parsing_channel(self.bot_name, self.channel)
        print "[!] Initialisation of tranfert done"
        self.recv_sock.settimeout(2)
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
                        if debug:
                            print res
                        user, message, msg_type = parse_msg(res, pub_reg, priv_reg, self.bot_name,
                                                            self.channel)
                        if self.pseudo is not None:
                            if msg_type == "Public_Message":
                                send_private_message(
                                    chr(3) + str(self.couleur) + "Message from channel " + self.channel + " : " + user + ">" + message,
                                    self.pseudo, self.send_sock)
                            else:
                                send_private_message(chr(3) + str(self.couleur) + "Message from user " + user + ">" + message, self.pseudo,
                                                     self.send_sock)
                        else:
                            if debug:
                                print res
                            if msg_type == "Public_Message":
                                send_public_message(
                                    chr(3) + str(self.couleur) + "Message from channel " + self.channel + " : " + user + ">" + message,
                                    self.send_sock)
                            else:
                                send_public_message(chr(3) + str(self.couleur) + "Message from user " + user + ">" + message, self.send_sock)
            except:
                pass