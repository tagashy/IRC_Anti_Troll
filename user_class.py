from __future__ import unicode_literals
import time


class User:
    def __init__(self, username, channel="UNKNOWN", server="UNKNOWN"):
        self.username = username
        self.server = server
        self.channel = channel
        self.actif = False
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()

    def update_last_seen(self):
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()
