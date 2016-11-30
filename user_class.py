from __future__ import unicode_literals

import time


class User:
    def __init__(self, username, channel="UNKNOWN", server="UNKNOWN", admin=False):
        self.username = username
        self.server = server
        self.channel = channel
        self.admin = admin
        self.connection = [(self.channel, self.server)]
        self.actif = False
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()
        self.alcolemie = 0

    def update_last_seen(self, server="UNKNOWN", channel="UNKNOWN", admin=False):
        self.lastSeen = time.strftime("%d/%m/%y %H:%M:%S")
        self.digiTime = time.time()
        self.server = server
        self.channel = channel
        self.admin = admin

    def __str__(self):
        ret = "user {} has been previously seen on {} and is on channels : ".format(self.username, self.lastSeen)
        for co in self.connection:
            ret += "{}=>{}, ".format(co[1], co[0])
        return ret
