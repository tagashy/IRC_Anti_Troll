from __future__ import unicode_literals

from time import sleep

from requests import get

import Irc_Class
from utils import convert_html_to_uni, parse_html_balise, print_message


class Apero(Irc_Class.IRC):
    def __init__(self, addr, channel, port, bot_name, sock, users):
        Irc_Class.IRC.__init__(self, addr, channel, port, bot_name, sock, users)
        self.apero = ""
        self.conseil = ""

    def main_loop(self):
        while not self.stopped():
            apero, conseil = self.check_apero()
            if apero != "":
                print_message(apero, "PUBMSG", self.sock, channel=self.channel)
                self.apero = apero
            if conseil != "":
                print_message(conseil, "PUBMSG", self.sock, channel=self.channel)
                self.conseil = conseil
            sleep(60)

    def check_apero(self):
        conseil = ""
        r = get(u"http://estcequecestbientotlapero.fr/")
        msg = parse_html_balise(u"h2", r.text)
        apero = convert_html_to_uni(parse_html_balise(u"<font size=5>", msg))
        if apero == self.apero:
            apero = ""
        if "font size=3" in msg:
            conseil = convert_html_to_uni(parse_html_balise(u"<font size=3", msg))
            if conseil == self.conseil:
                conseil = ""
        return apero, conseil
