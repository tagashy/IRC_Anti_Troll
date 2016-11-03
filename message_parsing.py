import re
from config import *

name_reg = re.compile("(?<=:)[^!]*(?=!)")
msg_type_reg = re.compile("(?<= PRIVMSG )[^:]*(?= :)")
pub_content_reg = re.compile("(?<= PRIVMSG " + channel + " :).*")
priv_content_reg = re.compile("(?<= PRIVMSG " + bot_name + " :).*")
name_list_reg = re.compile("(?<= 353 " + bot_name + " = " + channel + " :).*")


def get_content_public_msg(msg, public_content_reg=pub_content_reg):
    public_content_res = public_content_reg.search(msg)
    if public_content_res:
        public_content = public_content_res.group(0)
        return public_content
    else:
        print "[W] ERROR IN PARSING OF PUBLIC MESSAGE"


def get_content_private_msg(msg, private_content_reg=priv_content_reg):
    private_content_res = private_content_reg.search(msg)
    if private_content_res:
        private_content = private_content_res.group(0)
        return private_content
    else:
        print "[W] ERROR IN PARSING OF PRIVATE MESSAGE"


def parse_msg(msg):
    reg_res = name_reg.search(msg)
    msg_type_res = msg_type_reg.search(msg)
    if reg_res:
        name = reg_res.group(0)
    else:
        name = "NONE"
        if debug:
            print "[W] ERROR IN NAME"

    # parsing Public Private
    if msg_type_res:
        target = msg_type_res.group(0)
        if target == bot_name:
            msg_type = "Private_Message"
        elif target == channel:
            msg_type = "Public_Message"
        else:
            msg_type = "UNDEFINED"
    else:
        msg_type = "NONE"
    # parsing content
    if msg_type == "Private_Message":
        msg_content = get_content_private_msg(msg)
    elif msg_type == "Public_Message":
        msg_content = get_content_public_msg(msg)
    else:
        msg_content = "NONE"
        if debug:
            print "[W] ERROR IN MSG TYPE"

    return name, msg_content, msg_type


def parse_name_list(msg):
    name_list_res = name_list_reg.search(msg)
    if name_list_res:
        name_list = name_list_res.group(0)
        names = name_list.split()
        return names


def init_parsing_external_channel(external_bot_name, external_channel):
    public_content_reg = re.compile("(?<= PRIVMSG " + external_channel + " :).*")
    private_content_reg = re.compile("(?<= PRIVMSG " + external_bot_name + " :).*")
    if debug:
        print "(?<= PRIVMSG " + external_channel + " :).*"
        print "(?<= PRIVMSG " + external_bot_name + " :).*"
    return public_content_reg, private_content_reg


def parse_msg_external_chan(msg, private_content_reg, public_content_reg,external_bot_name,external_channel):
    reg_res = name_reg.search(msg)
    msg_type_res = msg_type_reg.search(msg)
    if reg_res:
        name = reg_res.group(0)
    else:
        name = "NONE"
        if debug:
            print "[W] ERROR IN NAME"

    # parsing Public Private
    if msg_type_res:
        target = msg_type_res.group(0)
        if target == external_bot_name:
            msg_type = "Private_Message"
        elif target == external_channel:
            msg_type = "Public_Message"
        else:
            msg_type = "UNDEFINED"
    else:
        msg_type = "NONE"
    # parsing content
    if msg_type == "Private_Message":
        msg_content = get_content_private_msg(msg, private_content_reg)
    elif msg_type == "Public_Message":
        msg_content = get_content_public_msg(msg, public_content_reg)
    else:
        msg_content = "NONE"
        if debug:
            print "[W] ERROR IN MSG TYPE"

    return name, msg_content, msg_type
