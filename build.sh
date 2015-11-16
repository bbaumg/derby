#!/bin/bash

# Instructions:
# Run the two below commands on the pi for the pinewood derby app.
# curl "https://raw.githubusercontent.com/bbaumg/derby/master/build.sh" > build.sh
# sudo bash build.sh

#Variables
log="/var/log/pibuild.log"
v_repo='https://raw.githubusercontent.com/bbaumg/derby/master'
v_defaultapps="python-pip python-dev python-smbus i2c-tools vim git-core locate build-essential scons swig htop"
v_gitEmail='bbaumg@gmail.com'
v_gitUser='Barrett'

# OK, let's install all of the basic stuff and do the basline configurations
sudo raspi-config
echo -en "\n-------------------------------------------------------\napt-get update\n\n" | tee -a $log
sudo apt-get dist-upgrade -y
echo -en "\n-------------------------------------------------------\napt-get install\n\n" | tee -a $log
sudo apt-get update -y
echo -en "\n-------------------------------------------------------\napt-get dist-upgrade\n\n" | tee -a $log
sudo apt-get install -y $v_defaultapps
echo -en "\n-------------------------------------------------------\npip3.2 install\n\n" | tee -a $log
sudo pip install pyephem pymysql configparser


echo -en "\n-------------------------------------------------------\nAdding to .bashrc\n\n" | tee -a $log
sed -i --follow-symlinks '/stuff/d' .bashrc
sed -i --follow-symlinks '/alias ll/d' .bashrc
sed -i --follow-symlinks '/export EDITOR/d' .bashrc
echo -en "\n# Some stuff I added\n"\
"alias ll='ls -alh'\n"\
"export EDITOR=vim\n" >> .bashrc

echo -en "\n-------------------------------------------------------\nSettup MOTD\n\n" | tee -a $log
curl "$v_repo/kickstart/banner" > /etc/banner
curl "$v_repo/kickstart/motd.sh" > /etc/motd.sh
sed -i --follow-symlinks '/motd.sh/d' .bashrc
echo '[ -n "$PS1" ] && bash /etc/motd.sh' >> .bashrc

echo -en "\n-------------------------------------------------------\nSetting up git\n\n" | tee -a $log
cd $HOME
git config --global user.email "$v_gitEmail"
git config --global user.name "$v_gitUser"

echo -en "\n-------------------------------------------------------\nInstall Dependencies\n\n" | tee -a $log
cd $HOME
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install

echo -en "\n-------------------------------------------------------\nInstall Automation\n\n" | tee -a $log
cd $HOME
git clone https://github.com/bbaumg/derby.git
#sudo bash automation/install.sh

echo -en "\n-------------------------------------------------------\nRemove Install File\n\n" | tee -a $log
cd $HOME
sudo rm -f build.sh

echo -en "\n-------------------------------------------------------\nBuild Complete\n\n" | tee -a $log
