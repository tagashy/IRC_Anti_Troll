import json
import os
import random
import threading
from subprocess import *

from command_class import *
from drivers import *
from utils import print_message

name_gen = random.Random()
name_gen.seed()


class RopThread(threading.Thread):
    def __init__(self, pseudo, message, msg_type, sock):
        threading.Thread.__init__(self)
        self.handlers = init_protocol_handler()
        self.pseudo = pseudo
        self.msg_type = msg_type
        self.sock = sock
        self.message = message

    def run(self):
        fichier, params, user, password = parse(self.message)
        if fichier is not None:
            fichier = self.get_file(fichier,user,password)
            if params != []:
                res = rop(params, fichier)
            else:
                res = rop(path=fichier)
            if res > 0:
                self.send_result(res, fichier)
            elif res == -1:
                print_message("No driver for this type of file", self.msg_type, self.sock, self.pseudo)
            elif res == -2:
                print_message(
                    "ERROR during recuperation of file (you may need to provide credential depending of the protocol)",
                    self.msg_type, self.sock, self.pseudo)

    def send_result(self, contents, fichier):
        content = ""
        rop_start = False
        for line in contents.split("\n"):
            if rop_start:
                content += line + "\n"
            elif "ROP chain generation" in line:
                content += line
                rop_start = True
        print_message(content)
        if content != "":
            url = "http://hastebin.com/"
            r = requests.post(url + "documents", data=content)
            print_message(r.text)
            data = json.loads(r.text)
            if "key" in data:
                print_message("url of ROP: " + url + data["key"], self.msg_type, self.sock, self.pseudo)
            else:
                print_message("ERROR AFTER POST", self.msg_type, self.sock, self.pseudo)
        else:
            print_message("content is None")
        os.remove(fichier)

    def get_file(self, path,user,password):
        fichier = str(name_gen.randint(0, 1000 * 1000)) + ".bin"
        get_type = path.split(":")[0]
        print_message(get_type)
        for handle in self.handlers:
            if handle.keyword == get_type:
                if handle.function(path, fichier,user,password):
                    return fichier
                else:
                    return -2
        return -1


def rop(params="--ropchain", path="/root/root-me/app-sys/ch32"):
    if isinstance(params, str):
        params = [params]
    elif not isinstance(params, list):
        return -1
    program_name = "ROPgadget"
    args = [program_name]
    for arg in params:
        args.append(arg)
    args.append("--binary")
    args.append(path)
    proc = Popen(args, stdout=PIPE)
    outs = ""
    while proc.poll() is None:
        out, err = proc.communicate()
        outs += out
    for line in outs.split("\n"):
        print_message(line)
    return outs


def parse(message):
    user = None
    password = None
    params = message.split(" ")
    args = []
    extra_arg = False
    fichier = None

    for param in params:
        splitted =param.split("=")[0]
        if  splitted == "--user" and len(splitted)>1:
            user=splitted[1]
        elif  splitted == "--password" and len(splitted)>1:
            password=splitted[1]
        elif extra_arg:
            args.append(param)
        elif "--args" == param:
            extra_arg = True
        elif splitted == "file" and len(splitted)>1:
            fichier = param[5:]

    return fichier, args, user, password


def init_protocol_handler():
    handlers = []
    handler = Command("http", get_http_file, "HTTP")
    handlers.append(handler)
    handler = Command("local", get_local_file, "LOCAL")
    handlers.append(handler)
    return handlers


if __name__ == '__main__':
    r = RopThread(None, "!rop file=http://challenge01.root-me.org/cracking/ch15/ch15.exe", "STDIN", None)
    r.start()
# parse("!rop file=/root/root-me/app-sys/ch32")
