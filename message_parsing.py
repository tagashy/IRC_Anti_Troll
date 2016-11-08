import re
from config import *
from utils import print_message

name_reg = re.compile("(?<=:)[^!]*(?=!)")
msg_type_reg = re.compile("(?<= PRIVMSG )[^:]*(?= :)")
join_reg = re.compile("(?<= JOIN :).*")
quit_reg = re.compile("(?<= QUIT :).*")
part_reg = re.compile("(?<= PART ).*")
message_regex = re.compile(
    r"^:([\w\[\]\\`_\^\{\|\}][\w\d\[\]\\`_\^\{\|\}\-]{1,})!([^\r\n@ ]+)@([\w\d\-\./]+)\s([\w]*)\s:?([&\#][^\s,\x07]{2,200})\s?:?(.*)$",
    re.VERBOSE)


# pub_content_reg = re.compile("(?<= PRIVMSG " + channel + " :).*")
# priv_content_reg = re.compile("(?<= PRIVMSG " + bot_name + " :).*")
# name_list_reg = re.compile("(?<= 353 " + bot_name + " = " + channel + " :).*")


def get_content_public_msg(msg, public_content_reg):  # =pub_content_reg):
    public_content_res = public_content_reg.search(msg)
    if public_content_res:
        public_content = public_content_res.group(0)
        return public_content
    else:
        print_message("[W] ERROR IN PARSING OF PUBLIC MESSAGE")


def get_content_private_msg(msg, private_content_reg):  # =priv_content_reg):
    private_content_res = private_content_reg.search(msg)
    if private_content_res:
        private_content = private_content_res.group(0)
        return private_content
    else:
        print_message("[W] ERROR IN PARSING OF PRIVATE MESSAGE")


def init_parsing_channel(bot_name, channel):
    public_content_reg = re.compile("(?<= PRIVMSG " + channel + " :).*")
    private_content_reg = re.compile("(?<= PRIVMSG " + bot_name + " :).*")
    if debug:
        print_message("(?<= PRIVMSG " + channel + " :).*")
        print_message("(?<= PRIVMSG " + bot_name + " :).*")
    return public_content_reg, private_content_reg


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
            # if content.startswith(" JOIN :"):
            #   full_username = msg_type[1:]
            #  msg_type = "JOIN"
            # pseudo = full_username.split("!")[0]
            # user_account = cut_at_cara(full_username, "!").split("@")[0]
            # ip = cut_at_cara(full_username, "@")
            # target = content.split(" JOIN :")[1]
        # content = cut_at_cara(content, ":")
        if target.startswith("#") and msg_type == "PRIVMSG":
            msg_type = "PUBMSG"
        if debug:
            print_message(
                "[D] pseudo: '{}' user acount: '{}' ip: '{}' msg type: '{}' content: '{}' target: '{}'".format(
                    # full_username, pseudo, user_account, ip, msg_type, content, target))
                    pseudo, user_account, ip, msg_type, content, target))
    return pseudo, user_account, ip, msg_type, content, target


def cut_at_cara(string, c):
    index = string.find(c)
    if index != -1:
        return string[index + 1:]
    else:
        return string


def parse_msg(msg, public_content_reg, private_content_reg, external_bot_name, external_channel):
    reg_res = name_reg.search(msg)
    msg_type_res = msg_type_reg.search(msg)
    if reg_res:
        name = reg_res.group(0)
    else:
        name = "NONE"
    if debug:
        print_message("[W] ERROR IN NAME")

        # parsing Public Private
    if msg_type_res:
        target = msg_type_res.group(0)
        if target == external_bot_name:
            msg_type = "PRIVMSG"
        elif target == external_channel:
            msg_type = "PUBMSG"
    else:
        join_res = join_reg.search(msg)
        quit_res = quit_reg.search(msg)
        part_res = part_reg.search(msg)
        if join_res:
            msg_type = "JOIN"
        elif quit_res:
            msg_type = "QUIT"
        elif part_res:
            msg_type = "PART"
        else:
            msg_type = "UNDEFINED"
            # parsing content
    if msg_type == "PRIVMSG":
        msg_content = get_content_private_msg(msg, private_content_reg)
    elif msg_type == "PUBMSG":
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
            print_message("[W] ERROR IN MSG TYPE")
    msg_content = msg_content.replace("\r", "").replace("\n", "").replace("\b", "")
    return name, msg_content, msg_type
