import random
import time

import rop
import rpg
from utils import *

num_genrator = random.Random()
num_genrator.seed()
color = 2
transferrer_list = []
rpg_list = []


def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "PUBMSG":
        send_public_message("\x01ACTION pointe ghozt\x01", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")", sock)


def DIE(pseudo, message, msg_type, sock):
    if pseudo != "Tagashy":
        print_message("I don't think so " + pseudo, msg_type, sock, pseudo)
    else:
        print "[!] Master say I'm DEAD"
        print_message("Ok master", msg_type, sock, pseudo)
        sock.send("QUIT :suis les ordres\r\n")
        sock.close()
        end_other_thread()
        exit(0)


def end_other_thread():
    for tr in transferrer_list:
        tr.stop()
        print_message("[!] Transferer {} stopped".format(tr.name))
    for rpg in rpg_list:
        rpg.stop()
        print_message("[!] RPG {} stopped".format(tr.name))


def transfert_message_from_other_place(pseudo, message, msg_type, sock):
    global color
    param = message.split()
    usage = "!transfert <server|require> <#channel|require> <private/public|optional>"
    if len(param) == 1:
        if "?" in param[0]:
            print_message(usage, msg_type, sock, pseudo)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            print_message(usage, msg_type, sock, pseudo)
        elif len(param) == 3:
            addr = param[1]
            server_addr = addr.split(":")
            if len(server_addr) == 1:
                server_addr = addr
                port = 6667
            elif len(server_addr) == 2:
                port = int(server_addr[1])
                server_addr = server_addr[0]
            else:
                print_message("too much :", msg_type, sock, pseudo)
                return
            channel = param[2]
            if check_valid_sever(server_addr, channel, port):
                print_message("sorry you choose this channel, I can't agree it will create a loophole!!!", msg_type,
                              sock, pseudo)
            elif check_not_already_use_transferer(server_addr, channel, port, pseudo):
                print_message("Transferer already exist", msg_type, sock, pseudo)
            else:
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print_message("[!] name of transferer user:" + external_bot_name)
                transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                sock.settimeout(0.5)
                timeout_start = time.time() + 10
                while not transfer.started:
                    try:
                        res = sock.recv(1024)
                        for line in res.split("\r\n"):
                            if "PING" in line:
                                sock.send(line.replace("PING", "PONG") + "\r\n")
                    except timeout:
                        if time.time() > timeout_start:
                            transfer.stop()
                            print_message("Transfert cannot be start in 10 seconds aborting!", msg_type, sock, pseudo)
                            sock.settimeout(None)
                            return
                        elif transfer.error is not None:
                            transfer.stop()
                            print_message("Transfert cannot be start because of error: " + transfer.error, msg_type,
                                          sock, pseudo)
                            sock.settimeout(None)
                            return
                sock.settimeout(None)
                color += 1
                if color > 15:
                    color = 2
                print_message("[!] Transferring data from " + addr + channel + " started")
                transferrer_list.append(transfer)
                print_message("Transfert start", msg_type, sock, pseudo)

        elif len(param) == 4:
            addr = param[1]
            server_addr = addr.split(":")
            if len(server_addr) == 1:
                server_addr = addr
                port = 6667
            elif len(server_addr) == 2:
                port = int(server_addr[1])
                server_addr = server_addr[0]
            else:
                print_message("too much :", msg_type, sock, pseudo)
                return
            channel = param[2]
            if check_valid_sever(server_addr, channel, port):
                print_message("sorry you choose this channel, I can't agree it will create a loophole!!!", msg_type,
                              sock, pseudo)
            elif check_not_already_use_transferer(server_addr, channel, port, None):
                print_message("Transferer already exist", msg_type, sock, pseudo)
            else:
                send_type = param[3]
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print_message("[!] name of transferer user:" + external_bot_name)
                if send_type.lower() == "publique" or send_type.lower() == "public":
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, couleur=color)
                else:
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                sock.settimeout(0.5)
                timeout_start = time.time() + 10
                while not transfer.started:
                    try:
                        res = sock.recv(1024)
                        for line in res.split("\r\n"):
                            if "PING" in line:
                                sock.send(line.replace("PING", "PONG") + "\r\n")
                    except timeout:
                        if time.time() > timeout_start:
                            transfer.stop()
                            print_message("Transfert cannot be start in 10 seconds aborting!", msg_type, sock, pseudo)
                            sock.settimeout(None)
                            return
                        elif transfer.error is not None:
                            transfer.stop()
                            print_message("Transfert cannot be start because of error: " + transfer.error, msg_type,
                                          sock, pseudo)
                            sock.settimeout(None)
                            return
                sock.settimeout(None)
                color += 1
                if color > 15:
                    color = 2
                print_message("[!] Transferring data from " + addr + channel + " started")
                transferrer_list.append(transfer)
                print_message("Transfert start", msg_type, sock, pseudo)


def check_not_already_use_transferer(server_addr, channel, external_port, target=None):
    for tr in transferrer_list:
        if config.debug:
            print_message("[D]", server_addr, channel, external_port, tr.addr, tr.channel, tr.port, tr.pseudo, target)
            print_message("[D]", tr.pseudo == target)
        if check_valid_sever(server_addr, channel, external_port, tr.addr, tr.channel, tr.port) and tr.pseudo == target:
            return 1


def check_valid_sever(server_addr, channel, external_port, comp_serv=config.main_server,
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


def list_transferer(pseudo, message, msg_type, sock):
    print_message("List of transferer:", msg_type, sock, pseudo)
    for tr in transferrer_list:
        print_message("{} on {} in channel {}".format(tr.name, tr.addr, tr.channel), msg_type, sock, pseudo)


def suppress_transferrer(pseudo, message, msg_type, sock):
    param = message.split()
    usage = "!kill_transfert <server|require> <#channel|require>"
    if len(param) == 1:
        if "?" in param[0]:
            print_message(usage, msg_type, sock, pseudo)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            print_message(usage, msg_type, sock, pseudo)
        elif len(param) >= 3:
            addr = param[1]
            server_addr = addr.split(":")
            if len(server_addr) == 1:
                server_addr = addr
                port = 6667
            elif len(server_addr) == 2:
                port = int(server_addr[1])
                server_addr = server_addr[0]
            else:
                print_message("too much :", msg_type, sock, pseudo)
                return
            channel = param[2]
            tr_stopped = False
            for tr in transferrer_list:
                if tr.port == port and tr.addr == server_addr and tr.channel == channel:
                    tr.stop()
                    tr_stopped = True
                    print_message("[!] transferrer " + tr.channel + " stopped")
                    transferrer_list.remove(tr)
                    print_message("transferrer " + tr.channel + " stopped", msg_type, sock, pseudo)
            if not tr_stopped:
                print_message("no transferrer like this one", msg_type, sock, pseudo)


def start_rpg(pseudo, message, msg_type, sock):
    param = message.split()
    rpg_game = None
    usage = "!rpg <server|optional> <channel|optional> "
    if len(param) == 1:
        if "?" in param[0]:
            print_message(usage, msg_type, sock, pseudo)
        else:
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            print_message("Starting RPG Game in channel : " + rpg_channel, msg_type, sock, pseudo)
            rpg_game = rpg.Rpg(config.main_server, "RPG_MASTER" + str(num_genrator.randint(1000, 1000 * 1000)),
                               rpg_channel,
                               config.main_port)
            rpg_game.start()
    elif len(param) == 2:
        if "?" in param[0] or "?" in param[1]:
            print_message(usage, msg_type, sock, pseudo)
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
                print_message("too much :", msg_type, sock, pseudo)
                return
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(1000, 1000 * 1000)), rpg_channel,
                               port)
            rpg_game.start()
            print_message("Starting RPG Game on server" + addr + " in channel : " + rpg_channel, msg_type, sock, pseudo)

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
            print_message("too much :", msg_type, sock, pseudo)
            return
        rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(0, 1000 * 1000)), param[2], port)
        rpg_game.start()
        print_message("Starting RPG Game on server" + addr + " in channel : " + param[2], msg_type, sock, pseudo)
    if rpg_game is not None:
        rpg_list.append(rpg_game)


def list_rpg(pseudo, message, msg_type, sock):
    print_message("List of RPG:", msg_type, sock, pseudo)
    for rpg in rpg_list:
        print_message("{} on {} in channel {}".format(rpg.name, rpg.addr, rpg.channel), msg_type, sock, pseudo)


def stop_rpg(pseudo, message, msg_type, sock):
    usage = "!kill_rpg <server|require> <channel|require>"
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            print_message(usage, msg_type, sock, pseudo)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            print_message(usage, msg_type, sock, pseudo)
        elif len(param) == 3:
            addr = param[1]
            server_addr = addr.split(":")
            if len(server_addr) == 1:
                server_addr = addr
                port = 6667
            elif len(server_addr) == 2:
                port = int(server_addr[1])
                server_addr = server_addr[0]
            else:
                print_message("too much :", msg_type, sock, pseudo)
                return
            channel = param[2]
            tr_stopped = False
            for rpg_game in rpg_list:
                if rpg_game.port == port and rpg_game.addr == server_addr and rpg_game.channel == channel:
                    rpg_game.stop()
                    tr_stopped = True
                    print_message("[!] RPG " + rpg_game.channel + " stopped")
            if not tr_stopped:
                print_message("no RPG like this one", msg_type, sock, pseudo)


def rop_start(pseudo, message, msg_type, sock):
    rop.RopThread(pseudo, message, msg_type, sock).start()


def migration(pseudo, message, msg_type, sock):
    usage = "!migrate <channel|require> <server|optional>"
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            print_message(usage, msg_type, sock, pseudo)
    elif len(param) == 2:
        sock.send("JOIN " + param[1] + "\r\n")
        sock.send("PART " + config.main_channel + "\r\n")
        config.main_channel = param[1]
        print_message("Migration done", msg_type, sock, pseudo)


def reload_bot(pseudo, message, msg_type, sock):
    param = message.split(" ")
    if len(param) == 2:
        if param[1] == "all":
            print_message("starting the reload", msg_type, sock, pseudo)
            reload(rop)
            reload(rpg)
            print_message("reload finished", msg_type, sock, pseudo)


from transfert_class import Transferrer
