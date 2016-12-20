#!/usr/bin/python

import sys
from sys import argv as arguments
import subprocess

operation = arguments[1]
mac = arguments[2]
ip = arguments[3]

try:
    hostname = arguments[4]
except IndexError:
    hostname = "Unknown"

posture="Healthy"
domain="global"
role="DHCP-Allocated"
user=hostname

if operation == "add":
    subprocess.call([sys.executable, '/var/tmp/User-Logon.py', '-o','logon','-a',ip,'-d',domain,'-r',role,'-u',user,'-p',posture])

if operation == "del":
    subprocess.call([sys.executable, '/var/tmp/User-Logon.py', '-o','logoff','-a',ip,'-u',user])
