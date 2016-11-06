import threading
from socket import *
from config import *
import utils
from message_parsing import *
import random
from command_class import Command

num_genrator = random.Random()
num_genrator.seed()


class Rpg(threading.Thread):
    def __init__(self, addr, bot_name, channel, port=6667):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.players = []
        self.addr = addr
        self.bot_name = bot_name
        self.channel = channel
        self.port = port
        self.sock = None
        self.cmds = []
        self.pub_reg = None
        self.priv_reg = None

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.comands_init()
        users, self.sock = utils.create_irc_socket(self.addr, self.bot_name, self.channel, self.port)
        self.pub_reg, self.priv_reg = init_parsing_channel(self.bot_name, self.channel)
        self.send_public_message("RPG Game about to start please register by !join")
        start = False
        while not start:
            if self.stopped():
                self.sock.send("QUIT : End of game\r\n")
                self.sock.close()
                exit(0)
            try:
                res = self.sock.recv(1024)
                if "PING" in res.split(" ")[0]:
                    self.sock.send(res.replace("PING", "PONG"))
                elif res.strip() != "":
                    if debug:
                        print res
                    user, message, msg_type = parse_msg(res, self.pub_reg, self.priv_reg, self.bot_name,
                                                        self.channel)
                    if message.startswith("!join"):
                        param = message.split(" ")
                        if len(param) == 1:
                            self.players.append(Player(user, 100, 100))
                    if message.startswith("!start"):
                        start = True
            except:
                pass
        self.send_public_message("Game has start !!!")
        for player in self.players:
            self.send_public_message(
                "INFO: " + player.pseudo + " has " + str(player.hp) + " HP and " + str(player.mana) + " mana")
        self.main_loop()

    def main_loop(self):
        while 1:
            for player in self.players:
                if player.hp <= 0:
                    self.send_public_message("Player " + player.pseudo + " is dead")
                    self.players.remove(player)
            if len(self.players) == 1:
                self.send_public_message("WIN for " + self.players[0].pseudo)
                self.stop()
            if self.stopped():
                self.sock.send("QUIT : End of game\r\n")
                self.sock.close()
                exit(0)
            try:
                res = self.sock.recv(1024)
                if "PING" in res.split(" ")[0]:
                    self.sock.send(res.replace("PING", "PONG"))
                elif res.strip() != "":
                    if debug:
                        print res
                    user, message, msg_type = parse_msg(res, self.pub_reg, self.priv_reg, self.bot_name,
                                                        self.channel)
                    self.command_choice(message,user)

            except:
                pass

    def command_choice(self, message, user):
        param = message.split(" ")
        for cmd in self.cmds:
            if isinstance(cmd.keyword, str):
                if message == cmd.keyword:
                    if debug:
                        print "[!] function " + cmd.name + " called by " + user
                    cmd.function(param, user)
            else:
                for key in cmd.keyword:
                    if message.startswith(key + " ") or message == key:
                        if debug:
                            print "[!] function " + cmd.name + " called by " + user
                        cmd.function(param, user)

    def fireball(self, param, user):
        if len(param) == 1:
            self.send_public_message(
                "USAGE: !fireball player (deal 5-30(+magic power) dmg to player)")
        elif len(param) > 1:
            for player in self.players:
                if player.pseudo == user:
                    minimum_dmg = 5 + player.magic_upgrade
                    maximum_dmg = 30 + player.magic_upgrade
                    cost = 25 - player.cost_reduction
                    if cost <= 0:
                        cost = 1
                    if player.mana >= cost:
                        player.mana -= cost
                        self.send_public_message(
                            "INFO: " + player.pseudo + " has now " + str(player.mana) + " mana")
                        for player in self.players:
                            if player.pseudo == param[1]:
                                player.hp -= num_genrator.randint(minimum_dmg, maximum_dmg)
                                self.send_public_message(
                                    "INFO: " + player.pseudo + " has now " + str(player.hp) + " HP")
                                break
                        break
                    else:
                        self.send_public_message(
                            "INFO: " + player.pseudo + " has not enough mana: " + str(
                                player.mana) + " mana/25")
                        break

    def reload(self, param, user):

        if "?" in param[0]:
            self.send_public_message("USAGE: !reload (restore mana 0-75(+magic power) mana)")
            return
        for player in self.players:
            if player.pseudo == user:
                minimum_dmg = 0 + player.magic_upgrade
                maximum_dmg = 75 + player.magic_upgrade
                player.mana += num_genrator.randint(minimum_dmg, maximum_dmg)
                self.send_public_message(
                    "INFO: " + player.pseudo + " has now " + str(player.mana) + " mana")
                break

    def heal(self, param, user, cost_reduction, magic_upgrade):

        if len(param) <= 1:
            if "?" in param[0]:
                self.send_public_message(
                    "USAGE: !heal (player) (give 0-25(+magic power) hp to player)")
                return
            target = user
        else:
            target = param[1]

        for player in self.players:
            if player.pseudo == user:
                minimum_dmg = 0 + player.magic_upgrade
                maximum_dmg = 25 + player.magic_upgrade
                cost = 10 - player.cost_reduction
                if cost <= 0:
                    cost = 1
                if player.mana >= cost:
                    player.mana -= cost
                    self.send_public_message(
                        "INFO: " + player.pseudo + " has now " + str(player.mana) + " mana")
                    for player in self.players:
                        if player.pseudo == target:
                            player.hp += num_genrator.randint(minimum_dmg, maximum_dmg)
                            self.send_public_message(
                                "INFO: " + player.pseudo + " has now " + str(player.hp) + " HP")
                            break
                    break
                else:
                    self.send_public_message(
                        "INFO: " + player.pseudo + " has not enough mana: " + str(
                            player.mana) + " mana/10")
                    break

    def help(self):
        ret = "Command available:"
        for cmd in self.cmds:
            if cmd.helpable:
                if isinstance(cmd.keyword, str):
                    ret += " " + cmd.keyword
                else:
                    for key in cmd.keyword:
                        if not "?" in key:
                            ret += " " + key

    def comands_init(self):
        cmds = []
        cmd = Command(["!fireball", "!fireball?"], self.fireball, "Fireball")
        cmds.append(cmd)
        cmd = Command(["!heal", "!heal?"], self.heal, "Heal")
        cmds.append(cmd)
        cmd = Command(["!reload", "!reload?"], self.reload, "Heal")
        cmds.append(cmd)
        self.cmds = cmds

    def send_public_message(self, message):
        self.sock.send("PRIVMSG " + self.channel + " :" + message + "\r\n")

    def send_private_message(self, message, pseudo):
        self.sock.send("PRIVMSG " + pseudo + " :" + message + "\r\n")


# rpg = Rpg("irc.root-me.org", "RPG_master", "#test")
# rpg.start()


class Player:
    def __init__(self, pseudo, hp, mana):
        self.pseudo = pseudo
        self.hp = hp
        self.mana = mana
        self.cost_reduction = 0
        self.magic_upgrade = 0
