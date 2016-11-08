import re

from config import *
from utils import print_message

message_regex = re.compile(
    r"^:([\w\[\]\\`_\^\{\|\}][\w\d\[\]\\`_\^\{\|\}\-]{1,})!([^\r\n@ ]+)@([\w\d\-\./]+)\s([\w]*)\s:?([&\#][^\s,\x07]{2,200})\s?:?(.*)$",
    re.VERBOSE)


def new_parsing(msg):
    msg = msg.replace("\r", "").replace("\n", "").replace("\b", "")
    pseudo = user_account = ip = msg_type = content = target = ""
    msg_parsed = message_regex.search(msg)
    if msg_parsed:
        data = msg_parsed.groups()
        if len(data) >= 6:
            pseudo = data[0]
            user_account = data[1]
            ip = data[2]
            msg_type = data[3]
            target = data[4]
            content = data[5]
        if target.startswith("#") and msg_type == "PRIVMSG":
            msg_type = "PUBMSG"
        if debug:
            print_message(
                "[D] pseudo: '{}' user acount: '{}' ip: '{}' msg type: '{}' content: '{}' target: '{}'".format(
                    pseudo, user_account, ip, msg_type, content, target))
    return pseudo, user_account, ip, msg_type, content, target
