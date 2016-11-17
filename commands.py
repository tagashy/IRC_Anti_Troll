import random
import time

import TagaBot
import rop
import rpg
from utils import *

num_genrator = random.Random()
num_genrator.seed()
color = 2
transferrer_list = []
rpg_list = []
bot_list = []


def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "PUBMSG":
        send_public_message("\x01ACTION pointe ghozt\x01", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")", sock)


def die(pseudo, message, msg_type, sock, channel):
    if pseudo == config.admin or msg_type == "STDIN":
        print_message("[!] Master say I'm DEAD")
        print_message("Ok master", msg_type, sock, pseudo, channel)
        sock.send("QUIT :suis les ordres\r\n")
        sock.close()
        end_other_thread()
        exit(0)
    else:
        print_message("I don't think so " + pseudo, msg_type, sock, pseudo, channel)


def end_other_thread():
    for tr in transferrer_list:
        tr.stop()
        print_message("[!] Transferer {} stopped".format(tr.name))
    for rpg in rpg_list:
        rpg.stop()
        print_message("[!] RPG {} stopped".format(rpg.name))


def transfert_message_from_other_place(pseudo, message, msg_type, sock, channel):
    global color
    param = message.split()
    if len(param) >= 3:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", msg_type, sock, pseudo, channel)
            return
        if check_valid_server(server_addr, param[2], port):
            print_message("sorry you can't choose this channel, I can't agree it will create a loophole!!!", msg_type,
                          sock, pseudo, channel)
            return
        elif len(param) == 3 or (len(param) == 4 and param[3].lower() != "publique" and param[3].lower() != "public"):
            if check_not_already_use_transferer(server_addr, param[2], port, pseudo):
                print_message("Transferer already exist", msg_type, sock, pseudo, channel)
                return
        else:
            if check_not_already_use_transferer(server_addr, param[2], port, None):
                print_message("Transferer already exist", msg_type, sock, pseudo, channel)
                return
        external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
        print_message("[!] name of transferer user:" + external_bot_name)
        if len(param) == 3 or (len(param) == 4 and param[3].lower() != "publique" and param[3].lower() != "public"):
            transfer = Transferrer(server_addr, param[2], port, external_bot_name, sock,channel, pseudo, couleur=color)
        else:
            transfer = Transferrer(server_addr, param[2], port, external_bot_name, sock,channel, couleur=color)
        transfer.start()
        timeout_start = time.time() + 10
        while not transfer.started:
            if time.time() > timeout_start:
                transfer.stop()
                print_message("Transfert cannot be start in 10 seconds aborting!", msg_type, sock, pseudo, channel)
                return
            elif transfer.error is not None:
                transfer.stop()
                print_message("Transfert cannot be start because of error: " + transfer.error, msg_type,
                              sock, pseudo, channel)
                return
        color += 1
        if color > 15:
            color = 2
        print_message("[!] Transferring data from " + addr + param[2] + " started")
        transferrer_list.append(transfer)
        print_message("Transfert start", msg_type, sock, pseudo, channel)


def check_not_already_use_transferer(server_addr, channel, external_port, target=None):
    for tr in transferrer_list:
        if config.debug:
            print_message(
                "[D] {} {} {} {} {} {} {} {}".format(server_addr, channel, external_port, tr.addr, tr.channel, tr.port,
                                                     tr.pseudo, target))
            print_message("[D] {}".format(tr.pseudo == target))
        if check_valid_server(server_addr, channel, external_port, tr.addr, tr.channel,
                              tr.port) and tr.pseudo == target:
            return 1


def check_valid_server(server_addr, channel, external_port, comp_serv=config.main_server,
                       comp_channel=config.main_channel,
                       comp_port=config.main_port):
    server_addr = server_addr.lower()
    if server_addr[-1:] == ".":
        server_addr = server_addr[:-1]
    channel = channel.lower()
    try:
        external_addrs = getaddrinfo(server_addr, external_port)
        addrs = getaddrinfo(comp_serv, comp_port)
    except:
        print_message("[W] Invalid Address")
        return 1
    if config.debug:
        print_message("[D] ip address of server {}".format(addrs))
    for data in addrs:
        if len(data) >= 5:
            adresse = data[4][0]
        else:
            adresse = ""
        if config.debug:
            print_message(
                "[D] adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(adresse, server_addr,
                                                                                                 adresse == server_addr))
            print_message("[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel,
                                                                                                           channel,
                                                                                                           comp_channel == channel))
        if adresse == server_addr and channel == comp_channel:
            return 1
        for external_data in external_addrs:
            if len(data) >= 5:
                external_adresse = data[4][0]
            else:
                external_adresse = ""
            if config.debug:
                print_message(
                    "[D] ip adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(adresse,
                                                                                                        server_addr,
                                                                                                        adresse == external_adresse))
                print_message(
                    "[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel,
                                                                                                     channel,
                                                                                                     comp_channel == channel))
            if adresse == external_adresse and channel == comp_channel:
                return 1
    if config.debug:
        print_message(
            "[D] adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(comp_serv, server_addr,
                                                                                             comp_serv == server_addr))
        print_message(
            "[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel, channel,
                                                                                             comp_channel == channel))
    if channel == comp_channel and server_addr == comp_serv:
        return 1


def list_transferer(pseudo, message, msg_type, sock, channel):
    print_message("List of transferer:", msg_type, sock, pseudo, channel)
    for tr in transferrer_list:
        print_message("{} on {} in channel {}".format(tr.name, tr.addr, tr.channel), msg_type, sock, pseudo, channel)


def suppress_transferrer(pseudo, message, msg_type, sock, channel):
    param = message.split()
    if len(param) >= 3:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", msg_type, sock, pseudo, channel)
            return
        tr_stopped = False
        for tr in transferrer_list:
            if tr.port == port and tr.server == server_addr and tr.channel == param[2]:
                tr.stop()
                tr_stopped = True
                print_message("[!] transferrer " + tr.channel + " stopped")
                transferrer_list.remove(tr)
                print_message("transferrer " + tr.channel + " stopped", msg_type, sock, pseudo, channel)
        if not tr_stopped:
            print_message("no transferrer like this one", msg_type, sock, pseudo, channel)


def start_rpg(pseudo, message, msg_type, sock, channel):
    param = message.split()
    usage = "!rpg <server|optional> <channel|optional> "
    if len(param) == 1:
        rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
        print_message("Starting RPG Game in channel : " + rpg_channel, msg_type, sock, pseudo, channel)
        rpg_game = rpg.Rpg(config.main_server, "RPG_MASTER" + str(num_genrator.randint(1000, 1000 * 1000)),
                           rpg_channel,
                           config.main_port)
        rpg_game.start()
    else:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", msg_type, sock, pseudo, channel)
            return
        if len(param) == 2:
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(1000, 1000 * 1000)), rpg_channel,
                               port)
            rpg_game.start()
            print_message("Starting RPG Game on server" + addr + " in channel : " + rpg_channel, msg_type, sock, pseudo,
                          channel)

        else:
            rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(0, 1000 * 1000)), param[2], port)
            rpg_game.start()
            print_message("Starting RPG Game on server" + addr + " in channel : " + param[2], msg_type, sock, pseudo,
                          channel)
    if rpg_game is not None:
        rpg_list.append(rpg_game)


def list_rpg(pseudo, message, msg_type, sock, channel):
    print_message("List of RPG:", msg_type, sock, pseudo, channel)
    for rpg in rpg_list:
        print_message("{} on {} in channel {}".format(rpg.name, rpg.addr, rpg.channel), msg_type, sock, pseudo, channel)


def stop_rpg(pseudo, message, msg_type, sock, channel):
    usage = "!kill_rpg <server|require> <channel|require>"
    param = message.split()
    if len(param) == 3:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", msg_type, sock, pseudo, channel)
            return
        tr_stopped = False
        for rpg_game in rpg_list:
            if rpg_game.port == port and rpg_game.addr == server_addr and rpg_game.channel == param[2]:
                rpg_game.stop()
                tr_stopped = True
                print_message("[!] RPG " + rpg_game.channel + " stopped")
        if not tr_stopped:
            print_message("no RPG like this one", msg_type, sock, pseudo, channel)


def rop_start(pseudo, message, msg_type, sock, channel):
    rop.RopThread(pseudo, message, msg_type, sock, channel).start()


def migration(pseudo, message, msg_type, sock, channel):
    param = message.split()
    if len(param) == 2:
        sock.send("JOIN " + param[1] + "\r\n")
        sock.send("PART " + config.main_channel + "\r\n")
        config.main_channel = param[1]
        print_message("Migration done", msg_type, sock, pseudo, channel)


def reload_bot(pseudo, message, msg_type, sock, channel):
    param = message.split()
    if len(param) == 2:
        if param[1] == "all":
            print_message("starting the reload", msg_type, sock, pseudo, channel)
            reload(rop)
            reload(rpg)
            reload(TagaBot)
            print_message("reload finished", msg_type, sock, pseudo, channel)


def start_bot(pseudo, message, msg_type, sock, channel):
    param = message.split()
    if len(param) >= 4:
        addr = param[1]
        server_addr = addr.split(":")
        if len(server_addr) == 1:
            server_addr = addr
            port = 6667
        elif len(server_addr) == 2:
            port = int(server_addr[1])
            server_addr = server_addr[0]
        else:
            print_message("too much :", msg_type, sock, pseudo, channel)
            return
        for bot in bot_list:
            if check_valid_server(server_addr, param[2], port, bot.server, bot.channel, bot.port):
                print_message("sorry you can't choose this channel, There is already one Unit of myself present in it",
                              msg_type,
                              sock, pseudo, channel)
                return
        bot_name = param[3]
        bot = TagaBot.Bot(bot_name=bot_name, server=server_addr, channel=param[2], port=port)
        bot.start()
        timeout_start = time.time() + 10
        while not bot.started:
            if time.time() > timeout_start:
                bot.stop()
                print_message("Bot cannot be start in 10 seconds aborting!", msg_type, sock, pseudo, channel)
                return -1
            elif bot.error is not None:
                bot.stop()
                print_message("Bot cannot be start because of error: " + bot.error, msg_type,
                              sock, pseudo, channel)
                return -2
        bot_list.append(bot)
        print_message("Bot started", msg_type, sock, pseudo, channel)
        return 1


def last_time_seen(pseudo, message, msg_type, sock, channel):
    param = message.split()
    if len(param) > 1:
        for i in xrange(1, len(param)):
            username = param[i]
            if username != "":
                found = False
                last_seen = ""
                digi_time = 0
                for tr in transferrer_list:
                    last, num_time = tr.last_seen(username)
                    if last != -1:
                        found = True
                        if digi_time < num_time:
                            last_seen = last
                            digi_time = num_time
                            channel_user = tr.channel
                            server = tr.server
                for bot in bot_list:
                    last, num_time = bot.last_seen(username)
                    if last != -1:
                        found = True
                        if digi_time < num_time:
                            last_seen = last
                            digi_time = num_time
                            channel_user = bot.channel
                            server = bot.server
                if found:
                    print last_seen
                    ret = "{} has been seen the last time on server {} in channel {} at: {}".format(username, server,
                                                                                                    channel_user,
                                                                                                    last_seen)
                else:
                    ret = "{} has never been seen".format(username)
                print_message(ret, msg_type, sock, pseudo, channel)


from transfert_class import Transferrer
