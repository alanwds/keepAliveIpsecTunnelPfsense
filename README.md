# Description

Script to parser config.xml from pfsense and send a spoofed package from pfsense to ip setted on automatically ping.  There are two work modes:

1 - Spoofed IP using scapy - Send a spoofed package from pfsense to ip setted on automatically ping. If no IP is setted, the script will send the package to remote network with a random port
2 - Nmap scan - Run a nmap scan using nmap -e {interface} -S source_ip dest_ip -sS from pfsense to remote network. To use this, you should set nmapMode = True on script variables section. 

## Dependencies

- Cron service on PfSense
- Nmap

## How it works

- 1 - Create a list with dicts with tunnel description, source network, destination network and ip to send package. If no ip was setted, we use the remote network as destination. The IP can have a port too.  To use that, you have to add ip:port on automatically ping host.
- 2 - Interact with each dict and send the package from source network

### Installation

- You have to put keepAliveNatedIpsecPfsense.py on pfsense filesystem. (/usr/local/bin/ in this example)
- Set the correct variables on variables section (interface, timeout and - if you like - nmap mode)
- Install cron service at pfsense packages manager
- Configure job as bellow
```
minute:  */5      (if you want to run every 5 minutes)
hours:    *
mday:    *
month:   *
wday:     *
(who):   root
command:   /usr/local/bin/python2.7 /usr/local/bin/keepAliveNatedIpsecPfsense.py
```

# To do

- Add some kind of log function

# Notes
 PR are always welcome
