#!/usr/bin/python

import sys
from sys import argv as arguments
import subprocess
from netaddr import *

operation = arguments[1]
mac = EUI(arguments[2])
oui = mac.oui
vendor = oui.registration().org

ip = arguments[3]

try:
    hostname = arguments[4]
except IndexError:
    hostname = "Unknown"

posture="Healthy"
domain="global"
role="DHCP-Allocated"
user=hostname
type="Unknown"
os="Unknown"
version="Unknown"
model="Unknown"
hostname=user




if operation == "add":
    subprocess.call([sys.executable, '/var/tmp/User-Logon.py', '-o','logon','-a',ip,'-d',domain,'-r',role,'-u',user,'-p',posture,'--vendor',vendor,'-t',type,'--os',os,'--version',version,'--model',model,'--hostname',hostname])

if operation == "del":
    subprocess.call([sys.executable, '/var/tmp/User-Logon.py', '-o','logoff','-a',ip,'-u',user])
