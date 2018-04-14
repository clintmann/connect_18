#!/usr/bin/env bash

echo
echo "################################################"
echo "Thank you for using the Network Audit Script    "
echo "--"
echo "This script will execute the script audit.py "
echo "--"
echo "It will display results to the screen           "
echo
echo "################################################"
echo

echo "Press Enter to continue..."
read confirm

echo "Please enter Management IP Address of switch to test : "
read ipaddr

echo "Please enter the USERNAME to log into the switch : "
read usr

echo "Please enter the PASSWORD for the switch : "
read -s usrpwd

echo "Please enter your SPARK TOKEN : "
read -s sparktkn

echo "Please enter SPARK ROOM ID : "
read -s sparkrm

export IPADDR=${ipaddr}
export USR=${usr}
export USRPWD=${usrpwd}
export SPARKTKN=${sparktkn}
export SPARKRM=${sparkrm}

python audit_sparkpost.py ${ipaddr}, ${usr}, ${usrpwd} ${sparktkn} ${sparkrm}

