#!/usr/bin/python

import datetime
import xml.etree.ElementTree as ET
import requests
from requests.auth import HTTPBasicAuth
import argparse


timestamp =  str(datetime.datetime.now().isoformat())

#Define arguments to construct XML 
parser = argparse.ArgumentParser()
parser.add_argument('-o','--operation', choices=['logon','logoff'], help='Operation type (Logon or Logoff)',required=True)
parser.add_argument('-a','--address', help='IPv4 or IPv6 Address',required=False)
parser.add_argument('-d','--domain', help='Domain name',required=False)
parser.add_argument('-u','--user', help='Users name',required=False)
parser.add_argument('-r','--role', help='list of roles this user belongs to. Maximum of 200 roles',nargs='+', type=str, required=False)
parser.add_argument('-p','--posture', help='Current security posture of the user/ip. Options of Healthy, Checkup, Transition, Quarantine, Infected or Unknown',required=False)
parser.add_argument('--hostname', help='Name of the machine/device)',required=False)
parser.add_argument('-t','--category', help='High level category of device(ie Desktop, Laptop, Tablet, Phone etc)',required=False)
parser.add_argument('--vendor', help='Vendor/Manufacturer name',required=False)
parser.add_argument('--type', help='Type of device (ie iPad, iPhone, Chromebook etc)',required=False)
parser.add_argument('--os', help='Operating System name (ie Win10, OSX, Android)',required=False)
parser.add_argument('--version', help='Operating System version number',required=False)

args = parser.parse_args()

def logon():
    #Generate XML file for upload
    source = ET.Element("source")
    source.text = "Aruba ClearPass"
    user.insert(0,source)
    time = ET.Element("timestamp")
    time.text = timestamp + "z"
    user.insert(1,time)
    operation = ET.Element("operation")
    operation.text = args.operation
    user.insert(2,operation)
    address = ET.Element("IP")
    address.text = args.address
    user.insert(3,address)
    domain = ET.Element("domain")
    domain.text = args.domain
    user.insert(4,domain)
    name = ET.Element("user")
    name.text = args.user
    user.insert(5,name)
    posture = ET.Element("posture")
    posture.text = args.posture
    user.insert(6,posture)
    #Add Device attributes into XML
    hostname = ET.Element("value")
    hostname.text = args.hostname
    device.insert(0,hostname)
    #Add role assignments into XML
    for role in args.role: 
        ET.SubElement(roles, "role").text = role     
    type = ET.Element("device-category")
    type.text = args.category
    attributes.insert(0,type)
    vendor = ET.Element("device-vendor")
    vendor.text = args.vendor
    attributes.insert(1,vendor)
    model = ET.Element("device-model")
    model.text = args.type
    attributes.insert(2,model)
    os = ET.Element("device-os")
    os.text = args.os
    attributes.insert(3,os)
    version = ET.Element("device-os-version")
    version.text = args.version
    attributes.insert(4,version)
    return;

def logoff():
    #Generate XML file for upload
    source = ET.Element("source")
    source.text = "Aruba ClearPass"
    user.insert(0,source)
    time = ET.Element("timestamp")
    time.text = timestamp + "z"
    user.insert(1,time)
    operation = ET.Element("operation")
    operation.text = args.operation
    user.insert(2,operation)
    address = ET.Element("IP")
    address.text = args.address
    user.insert(3,address)
    domain = ET.Element("domain")
    domain.text = args.domain
    user.insert(4,domain)
    name = ET.Element("user")
    name.text = args.user
    user.insert(5,name)
    return;

def generatexml():
    tree = ET.ElementTree(root)
    xml = "<?xml version=\"1.0\"?>" + ET.tostring(root)
    print xml
    headers = {'Content-Type': 'application/xml'}
    url = 'http://192.168.0.2:8080/api/userfw/v1/post-entry'
    print requests.post(url, auth=HTTPBasicAuth('user1','password123'), data=xml, headers=headers).text


#Define XML File to upload to SRX 
#Make this a routine for operations going through a "logon" phase
root = ET.Element("userfw-entries")
user = ET.SubElement(root, "userfw-entry")
roles = ET.SubElement(user, "role-list")
attributes = ET.SubElement(user, "end-user-attribute")
device = ET.SubElement(attributes, "device-identity")

if args.operation == "logon":	
    logon()
    generatexml()

if args.operation == "logoff": 	
    logoff()
    generatexml()






