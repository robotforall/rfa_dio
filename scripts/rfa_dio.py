#!/usr/bin/env python

import roslib; roslib.load_manifest('kobuki_testsuite');
import rospy

from std_msgs.msg import String
from kobuki_msgs.msg import DigitalInputEvent, Led, ButtonEvent, BumperEvent, DigitalOutput

digital_in = [True, True, True, True]
button = 0
button_state = 0
bumper = 0
bumper_state = 0

class MainLoop:
  def __init__(self):
    rospy.on_shutdown(self.cleanup)

    # Subscribe to the /mobile_base/events/digital_input topic to receive digital input
    rospy.Subscriber('/mobile_base/events/digital_input', DigitalInputEvent, self.DigitalInputEventCallback)

    # Subscribe to the /mobile_base/events/button topic to receive built-in button input
    rospy.Subscriber('/mobile_base/events/button', ButtonEvent, self.ButtonEventCallback)

    # Subscribe to the /mobile_base/events/bumper topic to receive bumper input
    rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.BumperEventCallback) 

    # publish Led messages to /mobile_base/commands/led1 & /mobile_base/commands/led2 topics to give Led signal
    self.pub1 = rospy.Publisher('/mobile_base/commands/led1', Led)
    self.pub2 = rospy.Publisher('/mobile_base/commands/led2', Led)
    self.led1 = Led()
    self.led2 = Led()

    # publish Led messages to /mobile_base/commands/digital_output to give digital signal
    self.pub3 = rospy.Publisher('/mobile_base/commands/digital_output', DigitalOutput)
    self.digital_out = DigitalOutput()

    # while loop
    while not rospy.is_shutdown():

      if digital_in[1]==True:
	rospy.loginfo("button 1 pressed !!!")

      elif digital_in[2]==True:
	rospy.loginfo("button 2 pressed !!!")

      elif digital_in[3]==True:
	rospy.loginfo("button 3 pressed !!!")



      if bumper == 0:
	if bumper_state == 1:
	  self.led1.value = 1

      elif bumper == 1:
	if bumper_state == 1:
	  self.led1.value = 2

      elif bumper == 2:
	if bumper_state == 1:
	  self.led1.value = 3



      if button == 0:
	if button_state == 1:
	  self.led1.value = 1
          self.digital_out.values = [False, False, False, False]
          self.digital_out.mask = [True, True, True, True]

      elif button == 1:
	if button_state == 1:
	  self.led1.value = 2
          self.digital_out.values = [True, True, True, True]
          self.digital_out.mask = [True, True, True, True]

      elif button == 2:
	if button_state == 1:
	  self.led1.value = 3


      self.pub1.publish(self.led1)
      self.pub2.publish(self.led2)
      self.pub3.publish(self.digital_out)
      rospy.Rate(4).sleep()

  def cleanup(self):
    rospy.loginfo("Stopping digital IO checking...")

  def DigitalInputEventCallback(self,data):
    global digital_in
    digital_in = data.values

  def ButtonEventCallback(self,data1):
    global button
    global button_state
    button = data1.button
    button_state = data1.state

  def BumperEventCallback(self,data2):
    global bumper
    global bumper_state
    bumper = data2.bumper
    bumper_state = data2.state

if __name__ == '__main__':
  rospy.init_node('digital_IO')
  try:
	MainLoop()
  except rospy.ROSInterruptException:
  	pass

