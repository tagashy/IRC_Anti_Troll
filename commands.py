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
rpg_list=[]

def command_loop(pseudo, message, msg_type, sock, cmds):
    #message = message.replace("\n", "").replace("\r", "")
    if "!help" == message:
        ret = "command available:"
        for cmd in cmds:
            if cmd.helpable:
                if isinstance(cmd.keyword, str):
                        ret += " " + cmd.keyword
                else:
                    for key in cmd.keyword:
                        if not "?" in key:
                                ret += " " + key
        send_public_message(ret, sock)
    elif "help" in message or "aide" in message:
        send_ticket_to_ghozt(pseudo, message, msg_type, sock)

    for cmd in cmds:
        if isinstance(cmd.keyword, str):
            if message == cmd.keyword:
                print "[!] function " + cmd.name + " called by " + pseudo
                cmd.function(pseudo, message, msg_type, sock)
        else:
            for key in cmd.keyword:
                if message.startswith(key+" ")or message == key:
                    print "[!] function " + cmd.name + " called by " + pseudo
                    cmd.function(pseudo, message, msg_type, sock)





def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "Public_Message":
        send_public_message("\x01ACTION pointe ghozt\x01", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")", sock)


def send_public_message(message, sock):
    sock.send("PRIVMSG " + channel + " :" + message + "\r\n")


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
    global color, transferrer_list
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!transfert server channel (Private/Publique)", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!transfert server channel (Private/Publique)", sock)
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
            external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
            print "[!] name of transferer user:" + external_bot_name
            transfer = Transferrer(addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
            transfer.start()
            color += 1
            print "[!] Transferring data from " + addr + channel + " started"
            transferrer_list.append(transfer)

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
            send_type = param[3]
            external_bot_name = "user_" + str(num_genrator.randint(1000, 1000 * 1000))
            print "[!] name of transferer user:" + external_bot_name
            if send_type.lower() == "publique" or send_type.lower() == "public":
                transfer = Transferrer(addr, channel, port, external_bot_name, sock, couleur=color)
            else:
                transfer = Transferrer(addr, channel, port, external_bot_name, sock, pseudo, couleur=color)
            transfer.start()
            color += 1
            print "[!] Transferring data from " + addr + channel + " started"
            transferrer_list.append(transfer)


def suppress_transferrer(pseudo, message, msg_type, sock):
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!kill_transfert server channel ", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!kill_transfert server channel ", sock)
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
            if not tr_stopped:
                send_public_message("no transferrer like this one",sock)


def start_rpg(pseudo, message, msg_type, sock):
    param = message.split()
    rpg_game=None
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!rpg (server) (channel) ", sock)
        else:
            rpg_channel = "#RPG_" + str(num_genrator.randint(1000, 1000 * 1000))
            send_public_message("Starting RPG Game in channel : "+rpg_channel,sock)
            rpg_game=rpg.Rpg(main_server,"RPG_MASTER",rpg_channel,main_port)
            rpg_game.start()
    elif len(param) == 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!rpg server (channel) ", sock)
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
            rpg_game = rpg.Rpg(server_addr, "RPG_MASTER", rpg_channel, port)
            rpg_game.start()
            send_public_message("Starting RPG Game on server"+addr+" in channel : " + rpg_channel,sock)
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
        rpg_game = rpg.Rpg(server_addr, "RPG_MASTER", param[2], port)
        rpg_game.start()
        send_public_message("Starting RPG Game on server" + addr + " in channel : " + param[2],sock)
    if rpg_game is not None:
        rpg_list.append(rpg_game)

def stop_rpg(pseudo, message, msg_type, sock):
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!kill_rpg server channel ", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!kill_rpg server channel ", sock)
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
                send_public_message("no RPG like this one",sock)

from transfert_class import Transferrer
