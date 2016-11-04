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
    cmd = command(["!transfert","!transfert?"],commands.transfert_message_from_other_place,"Tranfert")
    cmds.append(cmd)
    cmd = command(["!kill_transfert", "!kill_transfert?"], commands.suppress_transferrer, "Kill_Tranfert")
    cmds.append(cmd)
    cmd = command(["!rpg", "!rpg?"], commands.start_rpg, "Rpg")
    cmds.append(cmd)
    cmd = command(["!kill_rpg", "!kill_rpg?"], commands.start_rpg, "Kill_Rpg")
    cmds.append(cmd)
    return cmds

