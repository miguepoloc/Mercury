# -*- coding: utf-8 -*-
#Librería de tiempo
import time
#Librería de los GPIO
import RPi.GPIO as GPIO

#Variable que controla el ciclo infinito de la vizualización de la tira led
tira_led = True
#Ponemos los pines en modo Board
GPIO.setmode(GPIO.BCM)
red = 25
green = 10
blue = 9
colores = ("000", "011", "001", "101", "100", "110", "010")
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)


def color(R, G, B):
	"""Color"""
	GPIO.output(red, R)
	GPIO.output(green, G)
	GPIO.output(blue, B)


print("  R    G    B\n--------------")
# Main loop
try:
	while tira_led:
		for todo in colores:
			print ((todo[0], todo[1], todo[2]))
			color(int(todo[0]), int(todo[1]), int(todo[2]))
			time.sleep(2)
except KeyboardInterrupt:
	tira_led = False
	print ("Fin")
finally:
	GPIO.cleanup()