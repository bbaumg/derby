#!/bin/bash

#Variables
log="build.log"
v_gitEmail='bbaumg@gmail.com'
v_gitUser='Barrett'

# OK, let's install all of the basic stuff and do the basline configurations
sudo raspi-config
echo -en "\n-------------------------------------------------------\napt-get dist-upgrade\n\n" | tee -a $log
sudo apt-get dist-upgrade -y
echo -en "\n-------------------------------------------------------\napt-get update\n\n" | tee -a $log
sudo apt-get update -y
echo -en "\n-------------------------------------------------------\napt-get install\n\n" | tee -a $log
sudo apt-get install -y python-pip python-dev python-smbus python-imaging i2c-tools vim git-core locate build-essential scons swig htop
echo -en "\n-------------------------------------------------------\napt-get dist-config\n\n" | tee -a $log
sudo apt-get dist-upgrade -y
echo -en "\n-------------------------------------------------------\napt-get update\n\n" | tee -a $log
sudo apt-get update -y

echo -en "\n-------------------------------------------------------\nAdding to .bashrc\n\n" | tee -a $log
cd /home/pi
sed -i --follow-symlinks '/stuff/d' .bashrc
sed -i --follow-symlinks '/alias ll/d' .bashrc
sed -i --follow-symlinks '/export EDITOR/d' .bashrc
echo -en "\n# Some stuff I added\n"\
"alias ll='ls -alh'\n"\
"export EDITOR=vim\n" >> .bashrc

echo -en "\n-------------------------------------------------------\nSettup MOTD\n\n" | tee -a $log
cd /home/pi
curl "https://raw.githubusercontent.com/bbaumg/scripts/master/kickstart/banner" | sudo tee /etc/banner
curl "https://raw.githubusercontent.com/bbaumg/scripts/master/kickstart/motd.sh" | sudo tee /etc/motd.sh
sed -i --follow-symlinks '/motd.sh/d' .bashrc
echo '[ -n "$PS1" ] && bash /etc/motd.sh' >> .bashrc

echo -en "\n-------------------------------------------------------\nGet Derby App\n\n" | tee -a $log
cd /home/pi
git clone https://github.com/bbaumg/derby.git
#sudo bash derby/install.sh































