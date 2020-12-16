#!/usr/bin/python3

import paramiko
import getpass
from time import sleep


username = input("Username: ")
password = getpass.getpass(prompt="Password: ", stream=None)
hostname = input("Hostname: ")

commands = ['term len 0\n', 'show ip int bri\n', 'show ip route bgp\n']

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


session.close()


i = 1

while i < len(commands):
    print('======================= {0} =======================\n'.format(commands[i].rstrip('\n')))
    out = outputs[i].split('\n')
    for line in out:
        if '#' in line:
            continue
        else:
            print(line.rstrip('\n'))
    i +=1
