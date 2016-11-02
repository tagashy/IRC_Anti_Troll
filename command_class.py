import commands
from config import *


class command:
    def __init__(self, keyword, function,name,helpable=True):
        self.keyword = keyword
        self.function = function
        self.name=name
        self.help=helpable

def commands_init():
    cmds = []
    cmd = command("!die " + bot_name, commands.DIE,"DIE")
    cmds.append(cmd)
    cmd = command(["!transfert"],commands.transfert_message_from_other_place,"Tranfert")
    cmds.append(cmd)
    return cmds

