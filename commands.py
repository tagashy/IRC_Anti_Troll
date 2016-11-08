from config import *
from message_parsing import *
import thread
import random
import rpg
from socket import *

num_genrator = random.Random()
num_genrator.seed()
color = 2
transferrer_list = []
rpg_list = []


def print_message(message, msg_type="STDIN", sock=None, pseudo=None):
    if msg_type == "PRIVMSG":
        send_private_message(message, pseudo, sock)
    elif msg_type == "PUBMSG":
        send_public_message(message, sock)
    elif msg_type == "STDIN":
        print message


def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "PUBMSG":
        send_public_message("\x01ACTION pointe ghozt\x01", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")", sock)


def send_public_message(message, sock):
    sock.send("PRIVMSG " + main_channel + " :" + message + "\r\n")


def send_private_message(message, pseudo, sock):
    sock.send("PRIVMSG " + pseudo + " :" + message + "\r\n")


def DIE(pseudo, message, msg_type, sock):
    if pseudo != "Tagashy":
        send_public_message("I don't think so " + pseudo, sock)
    else:
        print "[!] Master say I'm DEAD"
        send_public_message("Ok master", sock)
        sock.send("QUIT :suis les ordres\r\n")
        sock.close()
        exit(0)


def transfert_message_from_other_place(pseudo, message, msg_type, sock):
    param = message.split()
    if msg_type == "PUBMSG":
        transferrer_public(pseudo, param, sock)
    elif msg_type == "PRIVMSG":
        transferrer_private(pseudo, param, sock)


def transferrer_public(pseudo, param, sock):
    global color
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!transfert <server|require> <#channel|require> <private/public|optional>", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!transfert <server|require> <#channel|require> <private/public|optional>", sock)
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
                send_public_message("too much :", sock)
                return
            channel = param[2]
            if check_valid_sever(server_addr, channel, port):
                send_public_message("sorry you choose this channel, I can't agree it will create a loophole!!!", sock)
            elif check_not_already_use_transferer(server_addr, channel, port, pseudo):
                send_public_message("Transferer already exist", sock)
            else:
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print "[!] name of transferer user:" + external_bot_name
                transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                color += 1
                if color > 15:
                    color = 2
                print "[!] Transferring data from " + addr + channel + " started"
                transferrer_list.append(transfer)
                send_public_message("Transfert start", sock)

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
                send_public_message("too much :", sock)
                return
            channel = param[2]
            if check_valid_sever(server_addr, channel, port):
                send_public_message("sorry you choose this channel, I can't agree it will create a loophole!!!", sock)
            elif check_not_already_use_transferer(server_addr, channel, port, None):
                send_public_message("Transferer already exist", sock)
            else:
                send_type = param[3]
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print "[!] name of transferer user:" + external_bot_name
                if send_type.lower() == "publique" or send_type.lower() == "public":
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, couleur=color)
                else:
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                color += 1
                if color > 15:
                    color = 2
                print "[!] Transferring data from " + addr + channel + " started"
                transferrer_list.append(transfer)
                send_public_message("Transfert start", sock)


def transferrer_private(pseudo, param, sock):
    global color
    if len(param) == 1:
        if "?" in param[0]:
            send_private_message("!transfert <server|require> <#channel|require> <private/public|optional>", pseudo,
                                 sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_private_message("!transfert <server|require> <#channel|require> <private/public|optional>", pseudo,
                                 sock)
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
                send_private_message("too much :", pseudo, sock)
                return
            channel = param[2]
            if channel[:1] != "#":
                send_private_message("Not a valid channel", pseudo, sock)
            elif check_valid_sever(server_addr, channel, port):
                send_private_message("sorry you choose this channel, I can't agree it will create a loophole!!!",
                                     pseudo, sock)
            elif check_not_already_use_transferer(server_addr, channel, port, pseudo):
                send_private_message("Transferer already exist", sock)
            else:
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print "[!] name of transferer user:" + external_bot_name
                transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                color += 1
                if color > 15:
                    color = 2
                print "[!] Transferring data from " + addr + channel + " started"
                transferrer_list.append(transfer)
                send_private_message("Transfert start", pseudo, sock)

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
                send_private_message("too much :", sock)
                return
            channel = param[2]
            if channel[:1] != "#":
                send_private_message("Not a valid channel", pseudo, sock)
            elif check_valid_sever(server_addr, channel, port):
                send_private_message("sorry I can't agree it will create a loophole!!!",
                                     pseudo, sock)
            elif check_not_already_use_transferer(server_addr, channel, port, None):
                send_private_message("Transferer already exist", pseudo, sock)
            else:
                send_type = param[3]
                external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
                print "[!] name of transferer user:" + external_bot_name
                if send_type.lower() == "publique" or send_type.lower() == "public":
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, couleur=color)
                else:
                    transfer = Transferrer(server_addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
                transfer.start()
                color += 1
                if color > 15:
                    color = 2
                print "[!] Transferring data from " + addr + channel + " started"
                transferrer_list.append(transfer)
                send_private_message("Transfert start", pseudo, sock)


def check_not_already_use_transferer(server_addr, channel, external_port, target=None):
    for tr in transferrer_list:
        if debug:
            print "[D]", server_addr, channel, external_port, tr.addr, tr.channel, tr.port, tr.pseudo, target
            print "[D]", tr.pseudo == target
        if check_valid_sever(server_addr, channel, external_port, tr.addr, tr.channel, tr.port) and tr.pseudo == target:
            return 1


def check_valid_sever(server_addr, channel, external_port, comp_serv=main_server, comp_channel=main_channel,
                      comp_port=main_port):
    server_addr = server_addr.lower()
    if server_addr[-1:] == ".":
        server_addr = server_addr[:-1]
    channel = channel.lower()
    try:
        external_addrs = getaddrinfo(server_addr, external_port)
        addrs = getaddrinfo(comp_serv, comp_port)
    except:
        print "[W] Invalid Address"
        return 1
    if debug:
        print "[D] ip address of server {}".format(addrs)
    for data in addrs:
        if len(data) >= 5:
            adresse = data[4][0]
        else:
            adresse = ""
        if debug:
            print "[D] adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(adresse, server_addr,
                                                                                                   adresse == server_addr)
            print "[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel,
                                                                                                   channel,
                                                                                                   comp_channel == channel)
        if adresse == server_addr and channel == comp_channel:
            return 1
        for external_data in external_addrs:
            if len(data) >= 5:
                external_adresse = data[4][0]
            else:
                external_adresse = ""
            if debug:
                print "[D] ip adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(adresse,
                                                                                                          server_addr,
                                                                                                          adresse == external_adresse)
                print "[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel,
                                                                                                       channel,
                                                                                                       comp_channel == channel)
            if adresse == external_adresse and channel == comp_channel:
                return 1
    if debug:
        print "[D] adresse of main serv '{}', adresse of external serv '{}', equal :{}".format(comp_serv, server_addr,
                                                                                               comp_serv == server_addr)
        print "[D] channel of main serv '{}', channel of external serv '{}', equal :{}".format(comp_channel, channel,
                                                                                               comp_channel == channel)
    if channel == comp_channel and server_addr == comp_serv:
        return 1


def suppress_transferrer(pseudo, message, msg_type, sock):
    param = message.split()
    if msg_type == "PUBMSG":
        suppress_transferrer_public(param, sock)
    elif msg_type == "PRIVMSG":
        suppress_transferrer_public(pseudo, param, sock)


def suppress_transferrer_public(param, sock):
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!kill_transfert <server|require> <#channel|require>  ", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!kill_transfert <server|require> <#channel|require> ", sock)
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
                send_public_message("too much :", sock)
                return
            channel = param[2]
            tr_stopped = False
            for tr in transferrer_list:
                if tr.port == port and tr.addr == server_addr and tr.channel == channel:
                    tr.stop()
                    tr_stopped = True
                    print "[!] transferrer " + tr.channel + " stopped"
                    transferrer_list.remove(tr)
                    send_public_message("transferrer " + tr.channel + " stopped", sock)
            if not tr_stopped:
                send_public_message("no transferrer like this one", sock)


def suppress_transferrer_private(pseudo, param, sock):
    if len(param) == 1:
        if "?" in param[0]:
            send_private_message("!kill_transfert <server|require> <#channel|require>  ", pseudo, sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_private_message("!kill_transfert <server|require> <#channel|require> ", pseudo, sock)
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
                send_private_message("too much :", pseudo, sock)
                return
            channel = param[2]
            tr_stopped = False
            for tr in transferrer_list:
                if tr.port == port and tr.addr == server_addr and tr.channel == channel:
                    tr.stop()
                    tr_stopped = True
                    print "[!] transferrer " + tr.channel + " stopped"
                    transferrer_list.remove(tr)
                    send_private_message("transferrer " + tr.channel + " stopped", pseudo, sock)

            if not tr_stopped:
                send_private_message("no transferrer like this one", pseudo, sock)


def start_rpg(pseudo, message, msg_type, sock):
    param = message.split()
    rpg_game = None
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!rpg <server|optional> <channel|optional> ", sock)
        else:
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            send_public_message("Starting RPG Game in channel : " + rpg_channel, sock)
            rpg_game = rpg.Rpg(main_server, "RPG_MASTER", rpg_channel, main_port)
            rpg_game.start()
    elif len(param) == 2:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!rpg <server|optional> <channel|optional> ", sock)
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
                send_public_message("too much :", sock)
                return
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(1000, 1000 * 1000)), rpg_channel,
                               port)
            rpg_game.start()
            send_public_message("Starting RPG Game on server" + addr + " in channel : " + rpg_channel, sock)
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
            send_public_message("too much :", sock)
            return
        rpg_game = rpg.Rpg(server_addr, "RPG_MASTER" + str(num_genrator.randint(0, 1000 * 1000)), param[2], port)
        rpg_game.start()
        send_public_message("Starting RPG Game on server" + addr + " in channel : " + param[2], sock)
    if rpg_game is not None:
        rpg_list.append(rpg_game)


def stop_rpg(pseudo, message, msg_type, sock):
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!kill_rpg <server|require> <channel|require>", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!kill_rpg <server|require> <channel|require>", sock)
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
                send_public_message("too much :", sock)
                return
            channel = param[2]
            tr_stopped = False
            for rpg_game in rpg_list:
                if rpg_game.port == port and rpg_game.addr == server_addr and rpg_game.channel == channel:
                    rpg_game.stop()
                    tr_stopped = True
                    print "[!] RPG " + rpg_game.channel + " stopped"
            if not tr_stopped:
                send_public_message("no RPG like this one", sock)


def migration(pseudo, message, msg_type, sock, entry="IRC"):
    global channel
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            if entry == "IRC":
                send_private_message("!migrate channel (server)", pseudo, sock)
            elif entry == "STDIN":
                print "!migrate channel (server)"
    elif len(param) == 2:
        sock.send("JOIN " + param[2])
        sock.send("PART " + channel)
        channel = param[2]


from transfert_class import Transferrer
