import re
from config import *

name_reg = re.compile("(?<=:)[^!]*(?=!)")
msg_type_reg = re.compile("(?<= PRIVMSG )[^:]*(?= :)")
join_reg = re.compile("(?<= JOIN :).*")
quit_reg = re.compile("(?<= QUIT :).*")
part_reg = re.compile("(?<= PART ).*")


# pub_content_reg = re.compile("(?<= PRIVMSG " + channel + " :).*")
# priv_content_reg = re.compile("(?<= PRIVMSG " + bot_name + " :).*")
# name_list_reg = re.compile("(?<= 353 " + bot_name + " = " + channel + " :).*")


def get_content_public_msg(msg, public_content_reg):  # =pub_content_reg):
    public_content_res = public_content_reg.search(msg)
    if public_content_res:
        public_content = public_content_res.group(0)
        return public_content
    else:
        print "[W] ERROR IN PARSING OF PUBLIC MESSAGE"


def get_content_private_msg(msg, private_content_reg):  # =priv_content_reg):
    private_content_res = private_content_reg.search(msg)
    if private_content_res:
        private_content = private_content_res.group(0)
        return private_content
    else:
        print "[W] ERROR IN PARSING OF PRIVATE MESSAGE"


def parse_name_list(msg, name_list_reg):
    name_list_res = name_list_reg.search(msg)
    if name_list_res:
        name_list = name_list_res.group(0)
        names = name_list.split()
        return names


def create_reg_user_list(bot_name, channel):
    name_list_reg = re.compile("(?<= 353 " + bot_name + " = " + channel + " :).*")
    if debug:
        print "(?<= 353 " + bot_name + " = " + channel + " :).*"
    return name_list_reg


def init_parsing_channel(bot_name, channel):
    public_content_reg = re.compile("(?<= PRIVMSG " + channel + " :).*")
    private_content_reg = re.compile("(?<= PRIVMSG " + bot_name + " :).*")
    if debug:
        print "(?<= PRIVMSG " + channel + " :).*"
        print "(?<= PRIVMSG " + bot_name + " :).*"
    return public_content_reg, private_content_reg


def parse_msg(msg, public_content_reg, private_content_reg, external_bot_name, external_channel):
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
        join_res=join_reg.search(msg)
        quit_res=quit_reg.search(msg)
        part_res=part_reg.search(msg)
        if join_res:
            msg_type = "JOIN"
        elif quit_res:
            msg_type = "QUIT"
        elif part_res:
            msg_type = "PART"
        else:
            msg_type = "UNDEFINED"
    # parsing content
    if msg_type == "Private_Message":
        msg_content = get_content_private_msg(msg, private_content_reg)
    elif msg_type == "Public_Message":
        msg_content = get_content_public_msg(msg, public_content_reg)
    elif msg_type == "JOIN":
        msg_content = join_res.group(0)
    elif msg_type == "QUIT":
        msg_content = quit_res.group(0)
    elif msg_type == "PART":
        msg_content = part_res.group(0)
    elif msg_type == "UNDEFINED":
        msg_content = "NONE"
        if debug:
            print "[W] ERROR IN MSG TYPE"
    msg_content = msg_content.replace("\r", "").replace("\n", "").replace("\b", "")
    return name, msg_content, msg_type
