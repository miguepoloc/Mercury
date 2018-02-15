#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)
mini = 0
medi = 0.0005
maxi = 0.0009
freq = 1000
periodo = 0.001
t_tick = periodo / 4096
t_mini = mini / t_tick
t_medi = medi / t_tick
t_maxi = maxi / t_tick
servoMin = int(t_mini)  # Min pulse length out of 4096
print (servoMin)
servoMed = int(t_medi)
print (servoMed)
servoMax = int(t_maxi)  # Max pulse length out of 4096
print (servoMax)


pwm.setPWMFreq(freq)                        # Set frequency to 60 Hz
while (True):
	# Change speed of continuous servo on channel O
	pwm.setPWM(3, 0, servoMin)
	time.sleep(1)
	pwm.setPWM(3, 0, servoMed)
	time.sleep(1)
	pwm.setPWM(3, 0, 4095)
	time.sleep(1)