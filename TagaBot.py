import threading

import commands
import message_parsing
import utils
from command_class import *
from config import config


class Bot(threading.Thread):
    def __init__(self, server, bot_name, channel, port):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.cmds = commands_init()
        self.users = None
        self.sock = None
        self.name = bot_name
        self.channel = channel
        self.server = server
        self.port = port
        self.started = False
        self.error = None

    def last_seen(self, username):
        for user in self.users:
            if username == user.username:
                return user.lastSeen, user.digiTime
        return -1, -1

    def update_user_last_seen(self, pseudo):
        for user in self.users:
            if pseudo == user.username:
                user.update_last_seen()
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
        print_message("[!] Initialisation of Bot done")
        self.started = True
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
                    self.sock.send(line.replace("PING", "PONG") + "\r\n")
                elif line.strip() != "":
                    if config.debug:
                        print line
                    pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                    self.update_user_last_seen(pseudo)
                    if not command_loop(pseudo, content, msg_type, self.sock, self.cmds,self.channel):
                        print_message("[" + msg_type + "] USER: " + pseudo + " send: " + content)


def commands_init():
    cmds = []
    cmd = Command(["!reload", "!reload?"], commands.reload_bot, "RELOAD", args=[("module/all", "require")])
    cmds.append(cmd)
    cmd = Command("!die", commands.die, "die")
    cmds.append(cmd)
    cmd = Command(["!transfert", "!transfert?"], commands.transfert_message_from_other_place, "Tranfert",
                  args=[("server", "require"), ("#channel", "require"), ("public/publique", "optional")])
    cmds.append(cmd)
    cmd = Command("!list_transfert", commands.list_transferer, "List Tranfert")
    cmds.append(cmd)
    cmd = Command(["!kill_transfert", "!kill_transfert?"], commands.suppress_transferrer, "Kill Tranfert",
                  args=[("server", "require"), ("#channel", "require")])
    cmds.append(cmd)
    cmd = Command(["!rpg", "!rpg?"], commands.start_rpg, "Rpg", args=[("server", "optional"), ("channel", "optional")])
    cmds.append(cmd)
    cmd = Command(["!list_rpg", "!list_rpg?"], commands.list_rpg, "List Rpg")
    cmds.append(cmd)
    cmd = Command(["!kill_rpg", "!kill_rpg?"], commands.stop_rpg, "Kill Rpg",
                  args=[("server", "require"), ("channel", "require")])
    cmds.append(cmd)
    cmd = Command([" help ", " aide "], commands.send_ticket_to_ghozt, "TICKET TO GHOZT", match=True, helpable=False)
    cmds.append(cmd)
    cmd = Command(["!rop", "!rop?"], commands.rop_start, "ROP",
                  args=[("file=...", "require"), ("--args ...", "optional"), ("--user=...", "optional"),
                        ("--password=...", "optional(never use it on public channel!!!)")])
    cmds.append(cmd)
    cmd = Command(["!last_seen", "!last_seen?"], commands.last_time_seen, "LAST SEEN",
                  args=[("pseudo", "require/repteable")])
    cmds.append(cmd)
    cmd = Command(["!new_unit", "!new_unit?"], commands.start_bot, "NEW UNIT",
                  args=[("server", "require"), ("#channel", "require"), ("name", "require")])
    cmds.append(cmd)
    return cmds
