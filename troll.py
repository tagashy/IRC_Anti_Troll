from __future__ import unicode_literals
import Queue

import requests

import mythread
import utils
import time

class troll(mythread.Thread):
    def __init__(self, Target, sock,channel):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.sock = sock
        self.target = Target
        self.channel=channel

    def init(self):
        utils.print_message("I can help you {} :)".format(self.target), "PRIVMSG", self.sock, self.target)

    def main(self):
        pseudo, msg = self.queue.get()
        if pseudo == self.target:
            res=self.get_citation()
            utils.print_message("{}=>{}".format(self.target,msg).encode(errors="replace"), "PUBMSG", self.sock, channel=self.channel)
            utils.print_message("{}<={}".format(self.target,res).encode(errors="replace"), "PUBMSG", self.sock,channel=self.channel)
            time.sleep(0.1*len(res))
            utils.print_message(res.encode(errors="replace"), "PRIVMSG", self.sock, self.target)

    @staticmethod
    def get_citation():
        r = requests.get("http://www.quotationspage.com/random.php3")
        return utils.parse_html_balise("a", utils.parse_html_balise("dt", r.text))
