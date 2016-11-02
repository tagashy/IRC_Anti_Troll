from config import *
from message_parsing import *


def command_loop(pseudo, message, msg_type, sock):
    message = message.replace("\n", "").replace("\r", "")
    if "help" in message or "aide" in message:
        send_ticket_to_ghozt(pseudo, message, msg_type, sock)
    if message == "!die " + pseudo:
        DIE(pseudo, sock)


def create_list_of_user(message):
    global users
    print "[!] creation of user list"
    users = parse_name_list(message)


def send_ticket_to_ghozt(pseudo, message, msg_type, sock):
    if msg_type == "Public_Message":
        send_public_message("\x01ACTION pointe ghozt\x01", sock)
        send_public_message("il poura t'aider " + pseudo + " pour (" + message + ")", sock)
        # sock.send("PRIVMSG " + channel + " :" + "\x01ACTION pointe ghozt\x01" + "\r\n")
        # sock.send("PRIVMSG " + channel + " :" + "il poura t'aider " + pseudo + " pour (" + message + ")" + "\r\n")


def send_public_message(message, sock):
    sock.send("PRIVMSG " + channel + " :" + message + "\r\n")


def send_private_message(message, pseudo, sock):
    sock.send("PRIVMSG " + pseudo + " :" + message + "\r\n")


def DIE(pseudo, sock):
    if pseudo != "Tagashy":
        send_public_message("I don't think so " + pseudo, sock)
    else:
        send_public_message("Ok master")
        sock.send("QUIT : suis les ordre\r\n", sock)
        sock.close()
