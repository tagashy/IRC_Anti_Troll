from utils import print_message


class Command:
    def __init__(self, keyword, function, name, helpable=True, match=False, args=None):
        self.keyword = keyword
        self.function = function
        self.name = name
        self.help = helpable
        self.match = match
        self.args = args


def command_loop(pseudo, message, msg_type, sock, cmds, channel):
    if "!help" == message:
        help_cmds(cmds, msg_type, pseudo, sock, channel)
        print_message("[!] help called by " + pseudo)
        return 1
    for cmd in cmds:
        if isinstance(cmd.keyword, str):
            if message == cmd.keyword or message+"?" == key:

                if "?" in message:
                    help_cmd(cmd, msg_type, pseudo, sock, channel)
                else:
                    print_message("[!] function " + cmd.name + " called by " + pseudo)
                    cmd.function(pseudo, message, msg_type, sock, channel)
                return 1
        else:
            for key in cmd.keyword:
                if message.startswith(key + " ") or message == key or message+"?" == key:
                    if "?" in message:
                        help_cmd(cmd, msg_type, pseudo, sock, channel)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + pseudo)
                        cmd.function(pseudo, message, msg_type, sock, channel)
                    return 1
                elif cmd.match and key in message:
                    if "?" in message:
                        help_cmd(cmd, msg_type, pseudo, sock, channel)
                    else:
                        print_message("[!] function " + cmd.name + " called by " + pseudo)
                        cmd.function(pseudo, message, msg_type, sock, channel)
                    return 1


def help_cmd(cmd, msg_type, pseudo, sock, channel):
    if isinstance(cmd.keyword, str):
        ret = cmd.keyword
    else:
        ret = cmd.keyword[0]
    if cmd.args is not None:
        for arg in cmd.args:
            ret += " <{}|{}>".format(arg[0], arg[1])
    print_message(ret, msg_type, sock, pseudo, channel)


def help_cmds(cmds, msg_type, pseudo, sock, channel):
    ret = "Command available:"
    for cmd in cmds:
        if cmd.help:
            if isinstance(cmd.keyword, str):
                ret += " " + cmd.keyword
            else:
                for key in cmd.keyword:
                    if "?" not in key:
                        ret += " " + key
    print_message(ret, msg_type, sock, pseudo, channel)
