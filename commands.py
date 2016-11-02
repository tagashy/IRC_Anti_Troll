from config import *
from message_parsing import *


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
    param = message.split()
    if len(param) == 1:
        if "?" in param[0]:
            send_public_message("!transfert server channel (Private/Publique)", sock)
    elif len(param) > 1:
        if "?" in param[0] or "?" in param[1]:
            send_public_message("!transfert server channel (Private/Publique)", sock)
        else:
            pass


def transfert_loop(recv_sock, send_sock,channel_name,external_bot_name,pseudo=None):
    pub_reg,priv_reg=init_parsing_external_channel(external_bot_name,channel_name)
    while (1):
        res = recv_sock.recv(1024)
        if "PING" in res.split(" ")[0]:
            recv_sock.send(res.replace("PING", "PONG"))
        elif res.strip() != "":
            if "353" in res:
                create_list_of_user(res)
            else:
                user, message, msg_type = parse_msg_external_chan(res,priv_reg,pub_reg)
                if pseudo is not None:
                    if msg_type=="Public_Message":
                        send_private_message("Message from channel "+channel_name+" :"+user+">"+message,pseudo,send_sock)
                    else:
                        send_private_message("Message from user "+pseudo+">"+message,pseudo,send_sock)
                else:
                    if msg_type=="Public_Message":
                        send_public_message("Message from channel "+channel_name+" :"+user+">"+message,send_sock)
                    else:
                        send_public_message("Message from user "+user+">"+message,send_sock)
