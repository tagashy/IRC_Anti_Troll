#!/usr/bin/python
from __future__ import unicode_literals

import threading

import readline

import commands
from command_class import *
from config import config


class StdInput(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.sock = sock

    def end(self):
        print_message("[!] ABORTING")
        exit(0)

    def run(self):
        cmds = []
        cmd = Command(["!migrate", "!migrate?"], commands.migration, "Migrate",
                      args=[("channel", "require"), ("server", "optional")])
        cmds.append(cmd)
        cmd = Command("!die", commands.die, "die")
        cmds.append(cmd)
        cmd = Command("!list", commands.user_list, "list")
        cmds.append(cmd)
        del cmd
        while 1:
            if self.stopped():
                self.end()
            data = raw_input()
            if command_loop("STDIN", data, "STDIN", self.sock, cmds, "STDIN"):
                print_message("[S] COMMAND SUCESS")
            else:
                try:
                    self.sock.send(data + "\n")
                    print ("[S] SEND SUCCES")
                except:
                    print ("[F] COMMAND/EXEC/SEND FAIL")

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


if __name__ == '__main__':
    readline.parse_and_bind("tab: complete")
    readline.set_completer()
    TAGABOT = commands.start_bot("STDIN", "!start_bot {}:{} {} {}".format(config.main_server, config.main_port,
                                                                          config.main_channel,
                                                                          config.bot_name), "STDIN", None, "STDIN")
    if TAGABOT > 0:
        # TagaBot = bot(config.main_server, config.bot_name, config.main_channel, config.main_port)
        # TagaBot.daemon = True
        # TagaBot.start()
        input_obj = StdInput(commands.bot_list[0].sock)
        input_obj.daemon = True
        input_obj.start()
        # TagaBot.join()
        # input_obj.stop()
        # commands.end_other_thread()
        # TagaBot.stop()
