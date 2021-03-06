#!/usr/bin/python


import paramiko
from time import sleep

username = input("Username: ")
password = input("Password: ")
hostname = input("Hostname: ")


session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
session.connect(hostname, port=22, username= username, password=password)

stdin, stdout, stderr = session.exec_command("show ip interface brief")

output = stdout.readlines()
sleep(0.25)
for line in output:
    print(line.rstrip('\n'))

