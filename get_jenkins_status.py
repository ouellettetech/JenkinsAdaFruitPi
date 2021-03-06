#!/usr/bin/python
# Example using a character LCD plate.
import math
import time
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import jenkins
import string
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      address= socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
      )[20:24])
    except:
      address=""
    return address

def Get_Status( BuildName ):
  output= BuildName[:16]
  try:
    lastBuild=J[BuildName].get_last_completed_build()
  except:
    return output
  Status=lastBuild.get_status()
  output+="\n"+Status + " "
  hasResults=lastBuild.has_resultset()
  buildNum=lastBuild.get_number()
  info=j.get_build_info(BuildName,buildNum)
  failures=0
  totalTest=0
  skipTests=0
  if hasResults:
     try:
       print "Has results"
       failures=info['actions'][15]['failCount']
       totalTest=info['actions'][15]['totalCount']
       skipTests=info['actions'][15]['skipCount']
     except:
       print "Error Getting Test Results"
  output+='%d/%d' % (failures,totalTest)
  return output

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

# create some custom characters
lcd.create_char(1, [2, 3, 2, 2, 14, 30, 12, 0])
lcd.create_char(2, [0, 1, 3, 22, 28, 8, 0, 0])
lcd.create_char(3, [0, 14, 21, 23, 17, 14, 0, 0])
lcd.create_char(4, [31, 17, 10, 4, 10, 17, 31, 0])
lcd.create_char(5, [8, 12, 10, 9, 10, 12, 8, 0])
lcd.create_char(6, [2, 6, 10, 18, 10, 6, 2, 0])
lcd.create_char(7, [31, 17, 21, 21, 21, 21, 17, 31])



# Turning on BackLight, and Displaying IP Address
lcd.set_color(1.0, 0.0, 0.0)
lcd.clear()
IP_Address=get_ip_address('eth0')+"\n"+get_ip_address('wlan0')
lcd.message(IP_Address)
time.sleep(3.0)

lcd.clear()
lcd.message('Connecting...')


# Makes list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select'),
            (LCD.LEFT,   'Left'  ),
            (LCD.UP,     'Up'    ),
            (LCD.DOWN,   'Down'  ),
            (LCD.RIGHT,  'Right' ) )

j = jenkins.Jenkins('http://jenkins.mixpo.com:8081/')
J = Jenkins('http://jenkins.mixpo.com:8081/')

MainBuilds = []
for buildName in J.keys():
   if "-Run-" in buildName:
      MainBuilds.append(buildName)
CurrentBuildNum=5
numBuilds=len(MainBuilds)
lcd.clear()
print MainBuilds[CurrentBuildNum]
lcd.message(Get_Status(MainBuilds[CurrentBuildNum]))


print 'Press Ctrl-C to quit.'
while True:
   # Loop through each button and check if it is pressed.
   if lcd.is_pressed(LCD.LEFT):
      CurrentBuildNum=(CurrentBuildNum+numBuilds-1)%numBuilds
      lcd.clear()
      lcd.message(Get_Status(MainBuilds[CurrentBuildNum]))
   if lcd.is_pressed(LCD.RIGHT):
      CurrentBuildNum=(CurrentBuildNum+1)%numBuilds
      lcd.clear()
      lcd.message(Get_Status(MainBuilds[CurrentBuildNum]))
