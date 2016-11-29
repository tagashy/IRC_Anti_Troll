from user_class import User


class user_lists:
    def __init__(self):
        self.__users = []

    def user_exist(self, pseudo):
        for u in self.__users:
            if pseudo == u.username:
                return 1
        return 0

    def add_users(self, user, server="UNKNOWN", channel="UNKNOWN"):
        if isinstance(user, User):
            if not self.user_exist(user.username):
                self.__users.append(user)
                return 1
            else:
                return 0
        elif isinstance(user, str) or isinstance(user, unicode):
            if not self.user_exist(user):
                self.__users.append(User(user, channel, server))
                return 1
            else:
                return 0
        else:
            return -1

    def remove_user(self, user):
        if isinstance(user, User):
            if self.user_exist(user.username):
                for u in self.__users:
                    if user.username == u.username:
                        self.__users.remove(u)
                        return 1
                return -1
            else:
                return 0
        elif isinstance(user, str) or isinstance(user, unicode):
            if self.user_exist(user):
                for u in self.__users:
                    if user == u.username:
                        self.__users.remove(u)
                        return 1
                return -1
            else:
                return 0
        else:
            return -1

    def update_user(self, user, alcolemie=False):
        if isinstance(user, User):
            if self.user_exist(user.username):
                for u in self.__users:
                    if user.username == u.username:
                        u.update_last_seen()
                        if alcolemie:
                            u.alcolemie += 1
                        return 1
                return -1
            else:
                return 0
        elif isinstance(user, str) or isinstance(user, unicode):
            if self.user_exist(user):
                for u in self.__users:
                    if user == u.username:
                        u.update_last_seen()
                        if alcolemie:
                            u.alcolemie += 1
        else:
            return -1