#!/bin/bash
if [ "$EUID" -ne 0 ]
	then echo "Must be root"
	exit
fi

if [[ $# -ne 2 ]]
	then echo "Usage: sudo $0 apPassword mysqlRootPassword"
	exit
fi

APSSID="rPi3"
APPASS=$1

MYSQLPASSWD=$2

echo "<?php \$con = mysqli_connect('localhost', 'root', '$MYSQLPASSWD', 'MusicManager'); ?>" >> ./html/database.php

echo "You have chones the following for you access point: "
echo "Network Name: $APSSID"
echo "Network Pass: $APPASS"

echo "Updateing apt-get..."
sudo apt-get update

echo "Installing nginx, php5, mysql, and mysql python"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $MYSQLPASSWD"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $MYSQLPASSWD"
sudo apt-get install nginx php5-fpm mysql-server php5-mysql python-mysqldb hostapd dnsmasq -y

echo "Moving nginx configs"
sudo mv default /etc/nginx/sites-enabled/default
sudo mv nginx.conf /etc/nginx/nginx.conf

echo "Moving php.ini"
sudo mv php.ini /etc/php5/fpm/php.ini

echo "Configureing wireless AP"
cat > /etc/dnsmasq.conf <<EOF
interface=wlan0
dhcp-range=10.0.0.2,10.0.0.5,255.255.255.0,12h
EOF

cat > /etc/hostapd/hostapd.conf <<EOF
interface=wlan0
hw_mode=g
channel=10
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=$APPASS
ssid=$APSSID
EOF

sed -i -- 's/exit 0/ /g' /etc/rc.local

cat >> /etc/rc.local <<EOF
ifconfig wlan0 down
ifconfig wlan0 10.0.0.1 netmask 255.255.255.0 up
iwconfig wlan0 power off
service hostapd start
service dnsmasq restart
hostapd -B /etc/hostapd/hostapd.conf & > /dev/null 2>&1
exit 0
EOF

echo "Installing database tables"
mysql -h "localhost" -u root -p"$MYSQLPASSWD" < "createDatabase.sql"

echo "Setting up webpage"
sudo chown pi -R /var/www/html
cp -R html/* /var/www/html/

echo "Setting up python script"

mv musicManager.py /home/pi/musicManager.py
chmod u+x /home/pi/musicManager.py

sed -i -- 's/exit 0/ /g' /etc/rc.local

cat >> /etc/rc.local <<EOF
/home/pi/musicManager.py &
exit 0
EOF

echo "All done!"
