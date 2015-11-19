#!/bin/bash

log="install.log"

echo -en "\n-------------------------------------------------------\nConfigure logrotate\n\n" | tee -a $log
# Create the base log file
echo 'Creating initial log file'
logfile='/var/log/derby.log'
touch $logfile
chown root:root $logfile
chmod 777 $logfile

# Setup log rotate
echo 'Configuring logrotate...'
rotatefile='/etc/logrotate.d/derby'
echo -en "$logfile\n$gitlogfile\n"\
"{\n"\
"  rotate 4\n"\
"  weekly\n"\
"  compress\n"\
"  notifempty\n"\
"}\n" > $rotatefile
chown root:root $rotatefile
chmod 755 $rotatefile
echo -en "\n\n"
cat $rotatefile

echo -en "\n-------------------------------------------------------\Install Derby\n\n" | tee -a $log
# Install and start daemon
bash /home/pi/derby/init/update.sh

echo -en "\n-------------------------------------------------------\nInstall Complete\n\n" | tee -a $log
