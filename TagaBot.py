from __future__ import unicode_literals

import IRC_Apero
import Irc_Class
import commands
import message_parsing
from command_class import *
from config import config


class Bot(Irc_Class.IRC):
    def __init__(self, server, bot_name, channel, port):
        if channel == "#root-me":
            self.error="BANNED CHANNEL"
            exit(0)
        Irc_Class.IRC.__init__(self, server, channel, port, bot_name)
        self.cmds = commands_init()
        self.apero=None


    def end(self):
        self.sock.send("QUIT : va faire une revision\r\n")
        self.sock.close()
        exit(0)

    def main_loop(self):
        self.apero = IRC_Apero.Apero(self.server, self.channel, self.port, self.name, self.sock, self.users)
        self.apero.start()
        while (1):
            if self.stopped():
                self.end()
            res = self.sock.recv(1024)
            for line in res.split("\r\n"):
                if "PING" in line:
                    self.sock.send(line.replace("PING", "PONG") + "\r\n")
                elif line.strip() != "":
                    if config.debug:
                        print (line)
                    pseudo, user_account, ip, msg_type, content, target = message_parsing.new_parsing(line)
                    self.update_user_last_seen(pseudo)
                    if not command_loop(pseudo, content, msg_type, self.sock, self.cmds, target):
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
    cmd = Command(["!apero", "!apero?"], commands.apero_status, "APERO")
    cmds.append(cmd)
    return cmds
