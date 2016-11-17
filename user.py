import time


class User:
    def __init__(self, username):
        self.username = username
        self.lastSeen = time.strftime("%d/%m/%y %M:%H")

    def update_last_seen(self):
        self.lastSeen = time.strftime("%d/%m/%y %M:%H")
