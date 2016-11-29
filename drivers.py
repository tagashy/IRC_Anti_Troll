from __future__ import unicode_literals
import random
import shutil
from ftplib import FTP

import paramiko
import requests
from scp import SCPClient

from command_class import Command


def init_protocol_handler():
    handlers = []
    handler = Command("http", get_http_file, "HTTP")
    handlers.append(handler)
    handler = Command("local", get_local_file, "LOCAL")
    handlers.append(handler)
    handler = Command("ftp", get_ftp_file, "FTP")
    handlers.append(handler)
    handler = Command("scp", get_scp_file, "SCP")
    handlers.append(handler)
    return handlers


def get_file(path, user, password):
    fichier = str(name_gen.randint(0, 1000 * 1000)) + ".bin"
    get_type = path.split(":")[0]
    for handle in handlers:
        if handle.keyword == get_type:
            if handle.function(path, fichier, user, password):
                return fichier
            else:
                return -2
    return -1


def get_scp_file(path, fichier, user=None, password=None):
    try:
        path = path.replace("scp:", "")
        server = path.split(":")[0].split("/")[0]
        try:
            port = path.split(":")[1].split("/")[0]
            port = int(port)
        except IndexError:
            port = 22
        data = path.split("/")
        path = ""
        for i in range(1, len(data) - 1):
            path += data[i] + "/"
        path += data[len(data) - 1]

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        scp = SCPClient(client.get_transport())
        scp.get(path, fichier)
        return 1
    except Exception as e:
        print ("[!] CANNOT GRAB FILE")
        print ("[!] " + str(e))
        return -1


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
            print (ftp.login(user, password))
        else:
            print (ftp.login())

        for i in range(1, len(data) - 1):
            print (ftp.cwd(data[i]))
        print (ftp.retrlines('LIST'))
        print (data[len(data) - 1])
        print (ftp.retrbinary('RETR ' + data[len(data) - 1], open(fichier, 'wb').write))
        return 1
    except:
        return -1


name_gen = random.Random()
name_gen.seed()
handlers = init_protocol_handler()

