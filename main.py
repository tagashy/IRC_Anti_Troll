import threading

import commands
import message_parsing
import utils
from command_class import *


class bot(threading.Thread):
    def __init__(self, server, bot_name, channel, port):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.cmds = commands_init()
        self.users, self.sock = utils.create_irc_socket(server, bot_name, channel, port)
        if self.sock == -1:
            exit(-1)
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
                    self.sock.send(line.replace("PING", "PONG") + "\r\n")
                elif line.strip() != "":
                    if config.debug:
                        print line
                    pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                    if not command_loop(pseudo, content, msg_type, self.sock, self.cmds):
                        print_message("[" + msg_type + "] USER: "+ pseudo+ " send: "+ content)


def commands_init():
    cmds = []
    cmd = Command("!die", commands.DIE, "DIE")
    cmds.append(cmd)
    cmd = Command(["!transfert", "!transfert?"], commands.transfert_message_from_other_place, "Tranfert")
    cmds.append(cmd)
    cmd = Command("!list_transfert", commands.list_transferer, "List Tranfert")
    cmds.append(cmd)
    cmd = Command(["!kill_transfert", "!kill_transfert?"], commands.suppress_transferrer, "Kill Tranfert")
    cmds.append(cmd)
    cmd = Command(["!rpg", "!rpg?"], commands.start_rpg, "Rpg")
    cmds.append(cmd)
    cmd = Command(["!list_rpg", "!list_rpg?"], commands.list_rpg, "List Rpg")
    cmds.append(cmd)
    cmd = Command(["!kill_rpg", "!kill_rpg?"], commands.stop_rpg, "Kill Rpg")
    cmds.append(cmd)
    cmd = Command([" help ", " aide "], commands.send_ticket_to_ghozt, "TICKET TO GHOZT", match=True, helpable=False)
    cmds.append(cmd)
    return cmds


class STD_INPUT(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.cmds = commands_init()
        self.sock = sock

    def run(self):
        cmds = []
        cmd = Command(["!migrate", "!migrate?"], commands.migration, "Migrate")
        cmds.append(cmd)

        while 1:
            if self.stopped():
                self.end()
            data = raw_input()
            if command_loop("STDIN", data, "STDIN", self.sock, cmds):
                print "[!] EXECUTED VIA STDIN"
            else:
                try:
                    exec data
                except:
                    self.sock.send(data)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


TagaBot = bot(config.main_server, config.bot_name, config.main_channel, config.main_port)
TagaBot.start()
input_obj = STD_INPUT(TagaBot.sock)
input_obj.daemon = True
input_obj.start()
TagaBot.join()
input_obj.stop()
commands.end_other_thread()
# TagaBot.stop()
print "[!] End"
