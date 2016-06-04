#!/bin/bash
if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

if [[ $# -ne 2 ]]
	then echo "Usage: sudo $0 staticIP gateway"
	exit
fi

STATICIP=$1
GATEWAY=$2

if ![ -f /etc/dhcpcd.conf.bak ]
	then sudo cp /etc/dhcpcp.conf /etc/dhcpcd.conf.bak
fi

sudo cp /etc/dhcpcd.conf.bak /etc/dhcpcp.conf

cat >> /etc/dhcpcd.conf <<EOF
interface eth0
static ip_address=$STATICIP
static routers=$GATEWAY
static domain_name_servers=$GATEWAY 8.8.8.8
EOF