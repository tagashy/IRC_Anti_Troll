import Queue

import requests

import mythread
import utils


class troll(mythread.Thread):
    def __init__(self, Target, sock):
        mythread.Thread.__init__(self)
        self.queue = Queue.Queue()
        self.sock = sock
        self.target = Target

    def init(self):
        utils.print_message("I can help you {} :)".format(self.target), "PRIVMSG", self.sock, self.target)

    def main(self):
        pseudo, msg = self.queue.get()
        if pseudo == self.target:
            utils.print_message(self.get_citation(), "PRIVMSG", self.sock, self.target)
            utils.print_message(self.get_citation(), "STDIN", self.sock, self.target)

    @staticmethod
    def get_citation():
        r = requests.get("http://www.quotationspage.com/random.php3")
        return utils.parse_html_balise("a", utils.parse_html_balise("dt", r.text))
