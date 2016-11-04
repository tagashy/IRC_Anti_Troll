import commands
from config import *
from commands import send_ticket_to_ghozt

class Command:
    def __init__(self, keyword, function, name, helpable=True):
        self.keyword = keyword
        self.function = function
        self.name = name
        self.help = helpable


def commands_init():
    cmds = []
    cmd = Command("!die " + bot_name, commands.DIE, "DIE")
    cmds.append(cmd)
    cmd = Command(["!transfert", "!transfert?"], commands.transfert_message_from_other_place, "Tranfert")
    cmds.append(cmd)
    cmd = Command(["!kill_transfert", "!kill_transfert?"], commands.suppress_transferrer, "Kill_Tranfert")
    cmds.append(cmd)
    cmd = Command(["!rpg", "!rpg?"], commands.start_rpg, "Rpg")
    cmds.append(cmd)
    cmd = Command(["!kill_rpg", "!kill_rpg?"], commands.stop_rpg, "Kill_Rpg")
    cmds.append(cmd)
    return cmds


def command_loop(pseudo, message, msg_type, sock, cmds):
    if "!help" == message:
        help_cmd(cmds,sock)
    elif "help" in message or "aide" in message:
        send_ticket_to_ghozt(pseudo, message, msg_type, sock)
    for cmd in cmds:
        if isinstance(cmd.keyword, str):
            if message == cmd.keyword:
                print "[!] function " + cmd.name + " called by " + pseudo
                cmd.function(pseudo, message, msg_type, sock)
        else:
            for key in cmd.keyword:
                if message.startswith(key + " ") or message == key:
                    print "[!] function " + cmd.name + " called by " + pseudo
                    cmd.function(pseudo, message, msg_type, sock)


def help_cmd(cmds, sock):
    ret = "Command available:"
    for cmd in cmds:
        if cmd.help:
            if isinstance(cmd.keyword, str):
                ret += " " + cmd.keyword
            else:
                for key in cmd.keyword:
                    if not "?" in key:
                        ret += " " + key
    send_public_message(ret, sock)


def send_public_message(message, sock):
    sock.send("PRIVMSG " + channel + " :" + message + "\r\n")
