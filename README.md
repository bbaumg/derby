# Pinewood Derby Timer
This pinewood derby timer is designed to work with a basic 4 lane wood track.  It is a simple python based application that with some Adafruit hardware.

The install is fairily well packaged, and as of writing this (11/15/2015) the install works with the "2015-09-24-raspbian-jessie" build of Raspbian.

To install...
```bash
curl "https://raw.githubusercontent.com/bbaumg/derby/master/build.sh" > build.sh
bash build.sh  #don't use sudo!!!
```
  1  raspi-config... will open
  2  Expand Filesystem
  3  Set international options for your local.
  4  Enable I2C under Advanced
  5  Don't Reboot - we will do that later.
  6  It will install all updates, upgrades, needed software, 
     and then run back through the updates and upgrades to make sure everything is current and tidy.
4  sudo bash derby/install.sh

At this point you should have a fully functioning pinewood derby timer that will start up on boot.
