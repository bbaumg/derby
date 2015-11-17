#!/bin/bash

echo "setting permissions and user on main.py"
chown pi:pi /home/pi/derby/main.py
chmod 755 /home/pi/derby/main.py
echo "Installing init.d file"
cp -f /home/pi/derby/init/derby /etc/init.d/derby
chmod 777 /etc/init.d/derby 
chown root:root /etc/init.d/derby
echo "set start on boot and being first time"
update-rc.d derby defaults
service derby restart
echo "init script has been installed"
