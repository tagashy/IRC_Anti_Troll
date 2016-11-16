import shutil
from ftplib import FTP

import requests


def get_local_file(path, fichier, user=None, password=None):
    try:
        path = path.replace("local:", "")
        shutil.copy2(path, fichier)
        return 1
    except:
        return -1


def get_http_file(path, fichier, user=None, password=None):
    try:
        if user is not None and password is not None:
            r = requests.get(path, stream=True, auth=(user, password))
        else:
            r = requests.get(path, stream=True)
        if r.status_code == 200:
            with open(fichier, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                return 1
        else:
            print ("Not Able To Download")
            return -1
    except:
        return -1


def get_ftp_file(path, fichier, user=None, password=None):
    try:
        path = path.replace("ftp:", "")
        data = path.split("/")
        addr = data[0]
        ftp = FTP(addr)
        if user is not None and password is not None:
            print ftp.login(user, password)
        else:
            print ftp.login()

        for i in xrange(1, len(data) - 1):
            print ftp.cwd(data[i])
        print ftp.retrlines('LIST')
        print data[len(data) - 1]
        print ftp.retrbinary('RETR ' + data[len(data) - 1], open(fichier, 'wb').write)
        return 1
    except:
        return -1


print get_http_file("ftp:51.254.128.177/test", "test.titi", "tagashy", "2ZsXdR(TgB")
