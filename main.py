import threading
import message_parsing
import utils
from command_class import *
import commands

class bot(threading.Thread):
    def __init__(self, server, bot_name, channel, port):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.cmds = commands_init()
        self.users, self.sock = utils.create_irc_socket(server, bot_name, channel, port)
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
                    print line
                    pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                    command_loop(pseudo, content, msg_type, self.sock, self.cmds)
                    if content != "NONE":
                        print "[" + msg_type + "]", "USER:", pseudo, "send:", content

def commands_init():
    cmds = []
    cmd = Command("!die", commands.DIE, "DIE")
    cmds.append(cmd)
    cmd = Command(["!transfert", "!transfert?"], commands.transfert_message_from_other_place, "Tranfert")
    cmds.append(cmd)
    cmd = Command(["!kill_transfert", "!kill_transfert?"], commands.suppress_transferrer, "Kill_Tranfert")
    cmds.append(cmd)
    cmd = Command(["!rpg", "!rpg?"], commands.start_rpg, "Rpg")
    cmds.append(cmd)
    cmd = Command(["!kill_rpg", "!kill_rpg?"], commands.stop_rpg, "Kill_Rpg")
    cmds.append(cmd)
    cmd= Command([" help "," aide "],commands.send_ticket_to_ghozt,"TICKET_TO_GHOZT",match=True)
    cmds.append(cmd)
    return cmds


TagaBot = bot(main_server, bot_name, main_channel, main_port)
TagaBot.start()
