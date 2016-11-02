from config import *
from message_parsing import *


def command_loop(pseudo, message, msg_type, sock):
    if "help" in message or "aide" in message:
        send_ticket_to_ghozt(pseudo, message, msg_type, sock)


def create_list_of_user(message):
    print "[!] creation of user list"
    return parse_name_list(message)


def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "Public_Message":
        send_public_message("\x01ACTION pointe ghozt\x01" + "\r\n", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")" + "\r\n", sock)
        # sock.send("PRIVMSG " + channel + " :" + "\x01ACTION pointe ghozt\x01" + "\r\n")
        # sock.send("PRIVMSG " + channel + " :" + "il poura t'aider " + pseudo + " pour (" + message + ")" + "\r\n")


def send_public_message(message, sock):
    sock.send("PRIVMSG " + channel + " :" + message)


def send_private_message(message, pseudo, sock):
    sock.send("PRIVMSG " + pseudo + " :" + message)
