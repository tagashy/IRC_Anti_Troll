import threading

import Bot_log
import user_class
import utils


class IRC(threading.Thread):
    def __init__(self, addr, channel, port, bot_name):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.server = addr
        self.channel = channel
        self.port = port
        self.name = bot_name
        self.users = None
        logname = utils.clean("{}_{}.log".format(self.server, self.channel))
        self.log = Bot_log.Log(logname)
        self.started = False
        self.error = None
        self.sock = None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def last_seen(self, username):
        for user in self.users:
            if username == user.username:
                return user.lastSeen, user.digiTime, user.actif
        return -1, -1, -1

    def update_user_last_seen(self, pseudo):
        found = False
        for user in self.users:
            if pseudo == user.username:
                user.update_last_seen()
                user.actif = True
                found = True
                break
        if not found:
            self.users.append(user_class.User(pseudo))

    def add_user(self, pseudo):
        for user in self.users:
            if user.username == pseudo:
                user.actif = True
                return
        self.users.append(user_class.User(pseudo, self.channel, self.server))
        return

    def deactivate_user(self, pseudo):
        for user in self.users:
            if pseudo == user.username:
                user.actif = False
                break

    def run(self):
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
        print "[!] Starting {} on server {}:{} in channel {}".format(self.name, self.server, self.port, self.channel)
        self.main_loop()

    def main_loop(self):
        pass
