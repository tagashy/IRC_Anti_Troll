import time


class Log:
    def __init__(self, log_file="TagaBot.log"):
        self.log = open(log_file, "a")

    def write(self, message):
        self.log.write("{}:{}\n".format(time.strftime("%d/%m/%y %M:%H "), message))
        self.log.flush()
