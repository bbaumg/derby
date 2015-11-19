# Pinewood Derby Timer
This pinewood derby timer is designed to work with a basic 4 lane wood track.  It is a simple python based application that with some Adafruit hardware.

Hardware List:
*   1 Raspberry pi with 1A power supply
*   4 Adafruit 0.56" 4-Digit 7-Segment Display w/I2C Backpack
*   1 Adafruit Perma-Proto HAT for Pi Mini Kit - No EEPROM
*   1 1k Ohm resistor
*   4 Phototransistor (I used:  OSRAM 720-SFH314)
*   1 lever switch

The install is fairily well packaged, and as of writing this (11/15/2015) the install works with the "2015-09-24-raspbian-jessie" build of Raspbian.

Start by running the installer

```bash
curl "https://raw.githubusercontent.com/bbaumg/derby/master/build.sh" > build.sh
bash build.sh  #don't use sudo!!!
```
1.  raspi-config... will open
2.  Select Expand Filesystem
3.  Set international options for your local.
4.  Enable I2C under Advanced
5.  Exit *Don't Reboot* - we will do that later.
6.  It will install all updates, upgrades, needed software, 
    and then run back through the updates and upgrades to make sure everything is current and tidy.
7.  now reboot

```bash
sudo bash derby/install.sh
```

At this point you should have a fully functioning pinewood derby timer that will start up on boot.


