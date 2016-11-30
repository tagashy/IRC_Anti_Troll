from __future__ import unicode_literals

from user_class import User


class user_lists:
    def __init__(self):
        self.__users = []

    def user_exist(self, pseudo):
        for u in self.__users:
            if pseudo == u.username:
                return 1
        return 0

    def add_user(self, user, server="UNKNOWN", channel="UNKNOWN"):
        admin = False
        if isinstance(user, User):
            if user.username[0:1] == "@":
                user.username = user.username[1:]
                user.admin = True
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            if user[0:1] == "@":
                user = user[1:]
                admin = True
            u = self.get_user(user)
        else:
            return -1
        if u == -1:
            if isinstance(user, User):
                self.__users.append(user)
            elif isinstance(user, str) or isinstance(user, unicode):
                self.__users.append(User(user, channel, server, admin))
            return 1
        else:
            for co in u.connection:
                if co[0] == channel and co[1] == server:
                    return 0
            u.connection.append((channel, server))
            return 1

    def deactivate_user(self, user):
        if isinstance(user, User):
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            u.actif = False
            return 1
        else:
            return 0

    def remove_user(self, user):
        if isinstance(user, User):
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            self.__users.remove(u)
            return 1
        else:
            return 0

    def update_user(self, user, server="UNKNOWN", channel="UNKNOWN", alcolemie=False):
        if isinstance(user, User):
            if user.username[:1] == "@":
                user = user[1:]
                admin = True
            else:
                admin = False
            u = self.get_user(user.username)
        elif isinstance(user, str) or isinstance(user, unicode):
            if user[:1] == "@":
                user = user[1:]
                admin = True
            else:
                admin = False
            u = self.get_user(user)
        else:
            return -1
        if u != -1:
            u.update_last_seen(server, channel, admin)
            if alcolemie:
                u.alcolemie += 1
            return 1
        else:
            return 0

    def get_user(self, user):
        if self.user_exist(user):
            for u in self.__users:
                if user == u.username:
                    return u
        else:
            return -1

    def __str__(self):
        ret = "USERLIST:"
        for user in self.__users:
            ret = "{}\r\n{}".format(ret, user)
        return ret


USERLIST = user_lists()
