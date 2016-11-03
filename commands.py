from config import *
from message_parsing import *
import thread
import random
from socket import *

num_genrator = random.Random()
color = 2
transferrer_list = []


def command_loop(pseudo, message, msg_type, sock, cmds):
    message = message.replace("\n", "").replace("\r", "")
    if "!help" == message:
        ret = "command available:"
        for cmd in cmds:
            if cmd.help:
                if isinstance(cmd.keyword, str):
                    ret += " " + cmd.keyword
                else:
                    for key in cmd.keyword:
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
                if key in message:
                    print "[!] function " + cmd.name + " called by " + pseudo
                    cmd.function(pseudo, message, msg_type, sock)


def create_list_of_user(message):
    global users
    print "[!] creation of user list"
    users = parse_name_list(message)


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
                if tr.port==port and tr.addr==server_addr and tr.channel==channel:
                    tr.stop()
                    tr_stopped=True
                    print "[!] transferrer "+tr.channel+" stopped"
            if not tr_stopped:
                send_public_message("no transferrer like this one")



from transfert_class import Transferrer
