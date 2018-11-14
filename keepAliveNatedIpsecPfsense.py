# -*- coding: utf-8 -*-
#Script to parser config.xml from pfsense and send a spoofed package from pfsense to ip setted on automatically ping (or remote network, if no ip is setted)
#How it works:
#1 - Create a list with dict (i.e. tunnel) with tunnel description, source network and ip to send package. If no ip was setted, we use the remote network as destination. The IP can have a port too.  To use that, you have to add ip:port on automatically ping host.
#2 - Interact with each dict and send the package from source network

import socket
import sys 
from random import randint
import xml.etree.cElementTree as ET

#Get XML conf
PFSENSE_CONF = './config.xml'
tree = ET.parse(PFSENSE_CONF)
root = tree.getroot()

try:
	from scapy.all import *
except:
	print "You need install scapy module first" 
	print "Do the follow steps:\npython2.7 -m ensurepip\npython2.7 -m pip install scapy"
	sys.exit(1)

#Get DST  port
def getDstPort(dst_ip):
	#Check if we have a port
	if ":" in dst_ip:
		#create a temp list with values separated ':'
		tmp = dst_ip.split(":")
		#Return port
		return str(tmp[1])
	else:
		#calculate  a random port
		return  int(randint(1024, 65000))

def sendPackage(source_ip,dst_ip):

	src_port = int(randint(1024, 65000))

	#calculate dst_port
	dst_port = int(getDstPort(dst_ip))

	#Split dst_ip to get only IP
	if ":" in dst_ip:
		tmp = dst_ip.split(":")
		dst_ip = tmp[0]

	payload = 'keepalive'
	spoofed_packet = IP(src=source_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port) / payload

	print "Sending spoofed TCP package from %s to %s on port %s" % (source_ip,dst_ip,dst_port)

	try:
		send(spoofed_packet)
	except:
		print "Error to send package to ",dst_ip


#Function to get tunnels info
def getTunnelsInfo():

	#Create an empty list to store the tunnels
	tunnelList = []

	print "Start config.xml parser"

	#Define search
        search = "./ipsec/phase2"

        for tunnel in root.findall(search):
		#Create tunnelDict
		tunnelDict = {}

                tunnelDict['name'] = tunnel.find('descr').text
                tunnelDict['pinghost'] = tunnel.find('pinghost').text
                tunnelDict['remoteNetwork'] = tunnel.find('remoteid/address').text
		tunnelDict['localNetwork'] = tunnel.find('localid/address').text
		tunnelList.append(tunnelDict)

	return tunnelList

#Main
if __name__ == '__main__':

        print "Staring script"
        print "Get list with description tunnels, source networks and ips to send packages"
        tunnels = getTunnelsInfo()

        for tunnel in tunnels:
		if tunnel['pinghost'] is not None:
               		print "Working on tunnel %s - network %s - ip to send package %s" % (tunnel['name'],tunnel['localNetwork'],tunnel['pinghost'])
			sendPackage(tunnel['localNetwork'],tunnel['pinghost'])
		else:
			print "No automatically ping ip was founded. Let's use remote network"
                	print "Working on tunnel %s - network %s - ip to send package %s" % (tunnel['name'],tunnel['localNetwork'],tunnel['remoteNetwork'])
			sendPackage(tunnel['localNetwork'],tunnel['remoteNetwork'])
			
