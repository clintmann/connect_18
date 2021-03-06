
from netmiko import ConnectHandler
import os
import re
from postsparkrm import post_message


""" FOR DEMO PURPOSES ONLY

This is script for Demo #5

SESSION: Network Programmability for the CLI Jockey

DESCRIPTION: This script is part of a series to show how a Network Engineer may start to leverage
network automation and programmability.

This script illustrates how to check for network connectivity of a Cisco device using ping.

It demonstrates how to use the Netmiko library to SSH to the device. We will use familiar cli commands
and collect the output (sometimes referred to as 'screen scrape'). Next we will attempt to add some 
'structure' to this 'unstructured' data in order to more easily search for the information we want. 

We will check if 
 - if Telnet is configured 
 - the HTTP server is disabled (this is commented out for demo purposes)

Lastly we will post findings to a Spark Room.

This script contains an over abundance of comments for demo purposes. 

It is not necessarily meant to be fast or efficient - but rather the purpose is to demonstrate
how a Network Engineer, who is new to programming might determine if Telnet is enabled on a switch and 
post the result to a Spark room. 

Run the run.sh script to populate the variables and execute this code.

"""

# Credentials to log into switch
mgmt_ip = os.environ['IPADDR']
username = os.environ['USR']
password = os.environ['USRPWD']

# Token of user who will post message in spark room
token = os.environ['SPARKTKN']

# Room ID of spark room
room_id = os.environ['SPARKRM']


def connect():

    print "\n"
    print "------ START OF SCRIPT ------\n"

    # Check for connectivity
    response = os.system("ping -c 3 " + mgmt_ip)
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    print "\n"
    print "PING STATUS: %s \n" % pingstatus

    # SSH to device
    print "------------------------\n"
    print "Connecting to device via SSH (using netmiko) ...\n"
    print "------------------------\n"
    net_connect = ConnectHandler(device_type='cisco_ios', ip=mgmt_ip, username=username, password=password)

    return net_connect


def get_name(net_connect):

    net_connect.find_prompt()

    # Get hostname of device
    get_hostname = net_connect.send_command("show run | include hostname")
    hostname = get_hostname.split("hostname ", 1)[1]

    return hostname


def get_vty(net_connect):

    net_connect.find_prompt()

    print "------------------------\n"
    print " (1) GET LINE VTY INFORMATION  "
    print "------------------------\n"

    # Assign output of Cisco show pipe command to a variable
    show_vty = net_connect.send_command("show run | section vty")

    # Print results and type
    print "------------------------\n"
    print " (2) CREATE STRUCTURED DATA TO PARSE "
    print "------------------------\n"

    return show_vty


def parse_regex(running_cfg, hostname):

    alert = []

    modified_lst = running_cfg.split('line')

    print "------------------------\n"
    print " (3) USE REGULAR EXPRESSIONS "
    print "------------------------\n"

    if 'telnet' in modified_lst[1]:
        text = modified_lst[1]
        vty = re.findall(r'(vty.*)', text)

        print "\n"
        print " ANSWER TO OUR QUESTIONS - IS TELNET CONFIGURED - IF SO, WHERE ? "
        print "------------------------\n"
        alert.append("\n** ALERT : DEVICE : %s has TELNET configured on %s \n" % (hostname, vty[0]))
        print "\n** ALERT : DEVICE : %s has TELNET configured on %s \n" % (hostname, vty[0])

    if 'telnet' in modified_lst[2]:
        text = modified_lst[2]
        vty = re.findall(r'(vty.*)', text)

        print "\n"
        print " ANSWER TO OUR QUESTIONS - IS TELNET CONFIGURED - IF SO, WHERE ? "
        print "------------------------\n"
        alert.append("\n** ALERT : DEVICE : %s has TELNET configured on %s \n" % (hostname, vty[0]))
        print "\n** ALERT : DEVICE : %s has TELNET configured on %s \n" % (hostname, vty[0])

    a_join = (", ".join(alert))

    return a_join


def check_http(net_connect):
    net_connect.find_prompt()
    show_http = net_connect.send_command("show run | include http server")

    print "------------------------\n"
    print " (3) LET'S CHECK IF http server IS CONFIGURED ON THE DEVICE"
    print "------------------------\n"

    if 'no' in show_http:
        print "RESULTS OF: show run | include http server \n %s \n" % show_http
        print "http *IS NOT* configured on this device \n"
    else:
        print "RESULTS OF: show run | include http server \n %s \n" % show_http
        print "http *IS* configured on this device \n"


def disconnect(net_connect):
    print "\n .... DISCONNECT FROM SWITCH \n"
    net_connect.disconnect()


if __name__ == '__main__':
    ssh = connect()
    name = get_name(ssh)
    show_run = get_vty(ssh)
    msg = parse_regex(show_run, name)
    # check_http(ssh)
    print "------------------------\n"
    print " (4) USE REST API CALL TO POST MESSAGE TO SPARK ROOM"
    print "------------------------\n"
    result = post_message(token, msg, room_id)
    disconnect(ssh)
