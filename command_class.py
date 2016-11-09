from config import *
from utils import print_message

class Command:
    def __init__(self, keyword, function, name, helpable=True,match=False):
        self.keyword = keyword
        self.function = function
        self.name = name
        self.help = helpable
        self.match=match

def command_loop(pseudo, message, msg_type, sock, cmds):
    if "!help" == message:
        help_cmd(cmds,msg_type,pseudo,sock)
    for cmd in cmds:
        if isinstance(cmd.keyword, str):
            if message == cmd.keyword:
                print "[!] function " + cmd.name + " called by " + pseudo
                cmd.function(pseudo, message, msg_type, sock)
                return 1
        else:
            for key in cmd.keyword:
                if message.startswith(key + " ") or message == key:
                    print "[!] function " + cmd.name + " called by " + pseudo
                    cmd.function(pseudo, message, msg_type, sock)
                    return 1
                elif cmd.match and key in message:
                    print "[!] function " + cmd.name + " called by " + pseudo
                    cmd.function(pseudo, message, msg_type, sock)
                    return 1


def help_cmd(cmds,msg_type,pseudo,sock):
    ret = "Command available:"
    for cmd in cmds:
        if cmd.help:
            if isinstance(cmd.keyword, str):
                ret += " " + cmd.keyword
            else:
                for key in cmd.keyword:
                    if not "?" in key:
                        ret += " " + key
    print_message(ret,msg_type, sock,pseudo)


def send_public_message(message, sock):
    sock.send("PRIVMSG " + config.main_channel + " :" + message + "\r\n")
