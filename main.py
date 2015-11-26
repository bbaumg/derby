#!/usr/bin/env python

####################################################################
#  Pinewood derby timer and winner display software.
#  Written by:  Barrett Baumgartner
#  Purpose:  Keep track of a 4 lane Pinewood Derby track. Report 
#            rankings and completion time.  Built for pack 900
#
#  Hardware needed:
####################################################################

import RPi.GPIO as GPIO
import sys
import time
import math
import signal
import logging
from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment
#from neopixel import *

# Setup logging
logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
#logLevel = logging.INFO
#logLevel = logging.DEBUG
cstlogFile = '/var/controller/main.log'

logging.basicConfig(
  level=logLevel, 
  #format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  format='%(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  #filename = cstlogFile)
  )
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 22(PIN 15) Start
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 23(PIN 16) Lane 1
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 24(PIN 18) Lane 2
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 25(PIN 22) Lane 3
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  4(PIN  7) Lane 4
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 27(PIN 13) Reset Switch
dictDisplays = {1:0x70, 2:0x71, 3:0x72, 4:0x73}   # Display addresses
flipflop = False                                  # Used for display rotation
raceReady = False                                 # Safety to start switch
dictPin2Lane = {23:1, 24:2, 25:3, 4:4}            # GPIO# to PIN#
dictLaneTime = {1:0, 2:0, 3:0, 4:0}               # Holds time for each lane
dictLaneRank = {1:0, 2:0, 3:0, 4:0}               # Holse rank for each lane
listPlacement = []                                # List holds placement


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def signal_handler(signal, frame):
    logger.info('You pressed Ctrl+C!')
    sys.exit(0)

def resetTrack(channel):
  global raceReady
  outResetDisp()
  raceReady = True
  logger.info('Track is reset and ready for race')

def raceStart(channel):
  global raceReady
  global dt_RaceStart
  if raceReady == True:
    dt_RaceStart = datetime.now()
    logger.critical("Start of race = " + str(dt_RaceStart))
    for i in range(1,5,1):
      dictLaneTime[i] = 0
      dictLaneRank[i] = 0
    del listPlacement[:]
    outZeroDisp()
    raceReady = False
    logger.info('All values reset')
  else:
    logger.info('Race not reset first!')
    
def laneFinish(channel):
  lane = dictPin2Lane[channel]
  logger.info('Care in lane ' + str(lane) + ' on PIN ' + str(channel) + ' Finished')
  if listPlacement.count(lane) == 0:
    listPlacement.append(lane)
    timer = (datetime.now() - dt_RaceStart)
    timer = float(str(timer.seconds) + "." + str(timer.microseconds / 1000))
    dictLaneTime[lane] = timer
    outTimeDisp(lane)
    dictLaneRank[lane] = listPlacement.index(lane)+1
    logger.critical('Lane ' + str(lane) + ' finished # ' + str(dictLaneRank[lane]) \
                    + ' with time ' + str(dictLaneTime[lane]))
  else:
    logger.critical('PROBLEM: Lane ' + str(lane) + ' already finished! ' \
                    + ' Reset and run again!')
  
def outZeroDisp():
  for i in dictDisplays:
    try:
      objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
      objDisp_i.begin()
      for ii in range(0,4,1):
        objDisp_i.set_digit_raw(ii, 0x3f)
      objDisp_i.write_display()
    except IOError as e:
      logger.error("The display caused an error for lane " + str(i))
    except:
      logger.info("There was an error writing to display " + str(lane))
      logger.exception(str(sys.exc_info()[0]))

def outResetDisp():  
  for i in dictDisplays:
    try:
      objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
      objDisp_i.begin()
      for ii in range(0,4,1):
        objDisp_i.set_digit_raw(ii, 0x40)
      objDisp_i.write_display()
    except IOError as e:
      logger.error("The display caused an error for lane " + str(i))
    except:
      logger.info("There was an error writing to display " + str(lane))
      logger.exception(str(sys.exc_info()[0]))

def outTimeDisp(lane):
  global dictDisplays
  global dictLaneTime
  i = lane
  try:
    objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
    objDisp_i.begin()
    objDisp_i.print_float(dictLaneTime[i])
    objDisp_i.write_display()
  except IOError as e:
    logger.error("The display caused an error for lane " + str(i))
  except:
    logger.error("There was an error writing to display " + str(lane))
    logger.exception(str(sys.exc_info()[0]))
    
def outRankDisp(lane):
  global dictDisplays
  global dictLaneRank
  i = lane
  try:
    objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
    objDisp_i.begin()
    objDisp_i.print_number_str(str(dictLaneRank[i])+ " ")
    objDisp_i.write_display()
  except IOError as e:
    logger.error("The display caused an error for lane " + str(i))
  except:
    logger.error("There was an error writing to display " + str(lane))
    logger.exception(str(sys.exc_info()[0]))

def outDispSetup():
  logger.info("Quick test to make sure the displays work")
  testDispSetup = (
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
    0x3f, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x3f)
  for y in range(len(testDispSetup)):
    for i in dictDisplays:
      try:
        objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
        objDisp_i.begin()
        for ii in range(0,4,1):
          objDisp_i.set_digit_raw(ii, testDispSetup[y])
        objDisp_i.write_display()
      except IOError as e:
        logger.error("The display caused an error for lane " + str(i))
      except:
        logger.exception("An unknown error happened" + str(sys.exc_info()[0]))
    time.sleep(.02)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END FUNCTIONS - BEGIN PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.critical("**************************************************")
logger.critical("*")
logger.critical("* Starting Program")
logger.critical("*")
logger.critical("**************************************************")
logger.critical("Log Level = " + str(logLevel))

GPIO.add_event_detect(22, GPIO.RISING, callback=raceStart, bouncetime=2000)
GPIO.add_event_detect(23, GPIO.RISING, callback=laneFinish, bouncetime=2000)
GPIO.add_event_detect(24, GPIO.RISING, callback=laneFinish, bouncetime=2000)
GPIO.add_event_detect(25, GPIO.RISING, callback=laneFinish, bouncetime=2000)
GPIO.add_event_detect(4, GPIO.RISING, callback=laneFinish, bouncetime=2000)
GPIO.add_event_detect(27, GPIO.RISING, callback=resetTrack, bouncetime=2000)
outDispSetup()

#strip = Adafruit_NeoPixel(cstLEDCount, cstLEDPin, cstLEDFreqHZ, cstLEDDMA, cstLEDInvert)
#strip.begin()


signal.signal(signal.SIGINT, signal_handler)
logger.critical('Press Ctrl+C')


while True:
  if len(listPlacement) != 0 and raceReady == False:
    if flipflop == False:
      for lane in dictLaneTime:
        outTimeDisp(lane)
      flipflop = True
    else:
      for lane in dictLaneRank:
        outRankDisp(lane)
      flipflop = False
  time.sleep(2)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
