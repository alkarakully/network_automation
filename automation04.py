#!/usr/bin/python3

import paramiko
import getpass
from time import sleep
import logging
import datetime

cred = '\033[91m'
cgrn = '\033[92m'
cend = '\033[0m'

today = datetime.date.today()

logging.basicConfig(filename=str(today), level=logging.DEBUG)
logger = logging.getLogger("paramiko")


username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
hostname = input("Hostname: ")

commands = ['term len 0\n', 'show ip int bri\n', 'show ip route bgp\n']
try:
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(hostname, port=22, username=username, password=password)
    connection = session.invoke_shell()

    outputs = []

    while connection.recv_ready():
        connection.recv(1024)

    for cmd in commands:
        connection.send(cmd)
        sleep(0.5)
        outputs.append(connection.recv(2048).decode('utf-8').replace(cmd.rstrip('\n'), ''))
        with open(str(today), 'a') as logFile:
           logFile.write(str(datetime.datetime.now()) + ' : ' + username + ' : ' + cmd + ' \n')

    session.close()

    i = 1
    while i < len(commands):
        outputFile = open(str(hostname) + '.txt', 'a')
        print(cred + '\n======================= {0} : {1} =======================\n'.format(datetime.datetime.now(), commands[i].rstrip('\n')) + cend)
        outputFile.write('\n======================= {0} : {1} =======================\n'.format(datetime.datetime.now(), commands[i].rstrip('\n')))
        out = outputs[i].split('\n')
        for line in out:
            if '#' in line:
                continue
            else:
                print(cgrn + line.rstrip('\n') + cend)
                outputFile.write(line + '\n')
        i +=1
        outputFile.close()
except:
    print(cred + "\n*********** Please, check your username and password" + cend)
