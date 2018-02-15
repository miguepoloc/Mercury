# -*- coding: utf-8 -*-
#MAGBÓTICO

"""----------------IMPORTACIÓN DE TODAS LAS LIBRERÍAS NECESARIAS----------------------"""
#Importamos la libreria del Webiopi, será la encargada de controlar los GPIO
#Además de ser el servidor
import webiopi
#Importamos la librería de tiempo
import time
#Importamos los GPIO como xGPIO, con el fin de controlarlos externos al webiopi
import RPi.GPIO as GPIO
#Importamos la libreria que permite activar nuevos procesos
import subprocess
#Importamos la librería que nos permite manejar varios hilos
import threading
#Importamos la libreria del sistema
import sys
#Añadimos la ruta del proyecto donde están los scripts que importaremos
sys.path.append('/home/pi/mercury/libreria')
#Importamos la librería de PWM para la shield del servo
from Adafruit_PWM_Servo_Driver import PWM

"""----------------------------CONTROL DE LOS PINES GPIO------------------------------"""
GPIO.setmode(GPIO.BCM)


"""------------LOS PINES PARA EL CONTROL DE LOS MOTORES TODOS SON GPIO BCM------------"""
#Definimos el pin 27 GPIO BCM donde se encontrara el motord in1
motord_in1 = 4
#Colocamos el pin del motord in1 como salida
GPIO.setup(motord_in1, GPIO.OUT)
#Definimos el pin 22 GPIO BCM donde se encontrara el motord in2
motord_in2 = 17
#Colocamos el pin del motord in2 como salida
GPIO.setup(motord_in2, GPIO.OUT)
#Definimos el pin 24 GPIO BCM donde se encontrara el motori in1
motori_in1 = 18
#Colocamos el pin del motori in1 como salida
GPIO.setup(motori_in1, GPIO.OUT)
#Definimos el pin 25 GPIO BCM donde se encontrara el motori in2
motori_in2 = 27
#Colocamos el pin del motori in2 como salida
GPIO.setup(motori_in2, GPIO.OUT)
##Definimos el pin 4 GPIO BCM donde se encontrara el pwm del motor 1
#motorpwm1 = 22
##Colocamos el pin del pwm1 como pwm
#GPIO.setFunction(motorpwm1, GPIO.PWM)
##Definimos el pin 18 GPIO BCM donde se encontrara el pwm del motor 2
#motorpwm2 = 23
##Colocamos el pin del pwm2 como pwm
#GPIO.setFunction(motorpwm2, GPIO.PWM)


"""-------------------------------SWICHEO DE MOTORES----------------------------------"""


def reversa():
	"""El robot se moverá hacia atras, en reversa"""
	GPIO.output(motord_in1, 1)
	GPIO.output(motord_in2, 0)
	GPIO.output(motori_in1, 0)
	GPIO.output(motori_in2, 1)


def adelante():
	"""El robot se moverá hacia adelante"""
	GPIO.output(motord_in1, 0)
	GPIO.output(motord_in2, 1)
	GPIO.output(motori_in1, 1)
	GPIO.output(motori_in2, 0)


def stop():
	"""El robot se detiene"""
	GPIO.output(motord_in1, 0)
	GPIO.output(motord_in2, 0)
	GPIO.output(motori_in1, 0)
	GPIO.output(motori_in2, 0)
	#Se declara a la variable velocidad como global
	global velocidad
	#Se define como 0 inicialmente
	velocidad = 0


def derecha():
	"""El robot se moverá hacia la derecha"""
	GPIO.output(motord_in1, 0)
	GPIO.output(motord_in2, 1)
	GPIO.output(motori_in1, 0)
	GPIO.output(motori_in2, 1)


def izquierda():
	"""El robot se moverá hacia la izquierda"""
	GPIO.output(motord_in1, 1)
	GPIO.output(motord_in2, 0)
	GPIO.output(motori_in1, 1)
	GPIO.output(motori_in2, 0)


"""--------------------------ACELERACIÓN DE LOS MOTORES-------------------------------"""


def acelerar(valor_vel):
	"""Controla la velocidad de los motores"""
	global velocidad
	velocidad = valor_vel
	#value = float(velocidad) / 100
	#GPIO.pulseRatio(motorpwm1, value)
	#GPIO.pulseRatio(motorpwm2, value)


"""--------------------------CONTROL DE LOS SERVOMOTORES------------------------------"""
#Se inicia la fución pwm en la ruta 0 de I2C que sería 0x40
pwm = PWM(0x40)
#Se establece la frecuencia a 50 Hz
freq = 50
#Debido a tener una frecuencia de 50Hz, el periodo es de 20ms
periodo = 0.020
#Colocamos los pulsos del pwm al valor de la frecuencia
pwm.setPWMFreq(freq)


def servo01(tick):
	"""Controla el primer servomotor, este tiene un rango entre 130 y 500 ticks"""
	#Toma el valor recibido del deslizador en la página respecto al servo 1
	#Convierte ese valor de String a entero
	tick = int(tick)
	#Para comodidad, en la página el deslizador va de 13 a 50, por eso se multiplica * 10
	tick = tick * 10
	print ("El valor del servo es: " + str(tick))
	#Colocamos el servo del canal 0, iniciando con alto hasta el valor del tick
	#La función hace lo siguiente |¨¨¨¨¨¨¨|______|¨¨¨¨¨¨¨|______
	#Esta función tiene como parámetro el canal, valor de on y off
	#Es decir, se enciende en 0 y se apaga en el tiempo del tick
	pwm.setPWM(0, 0, tick)


def servo02(tick):
	"""Controla el segundo servomotor, este tiene un rango entre 160 y 450 ticks"""
	#Toma el valor recibido del deslizador en la página respecto al servo 2
	#Convierte ese valor de String a entero
	tick = int(tick)
	#Para comodidad, en la página el deslizador va de 16 a 45, por eso se multiplica * 10
	tick = tick * 10
	print ("El valor del servo es: " + str(tick))
	#Colocamos el servo del canal 1, iniciando con alto hasta el valor del tick
	pwm.setPWM(1, 0, tick)


"""---------------------SWICHEO DE LUZ LED PARA CRUZAR EL TÚNEL-----------------------"""
#Definimos el pin 24 donde se encontrara el led que servirá de linterna
led = 24
#Colocamos el pin del led como salida
GPIO.setup(led, GPIO.OUT)
#Variable que controla el estado de la tira led de la linterna
estadoluz = "apagado"


def linterna():
	"""Controla la tira led que funcionará de linterna en el túnel"""
	#Si el estado de la luz es apagado
	global estadoluz
	if(estadoluz == "apagado"):
		#Enciende la tira led
		GPIO.output(led, 1)
		#Coloca el estado de la luz en encendido
		estadoluz = "encendido"
	#Si el estado de la luz es encendido
	elif(estadoluz == "encendido"):
		#Apaga la tira led
		GPIO.output(led, 0)
		#Coloca el estado de la luz en apagado
		estadoluz = "apagado"


"""-------------------------VERIFICAR CONEXIÓN A INTERNET-----------------------------"""


def internet():
	"""Realiza un ping a google para saber si hay conexión a internet
	Además de controlar la variable tira_led dependiendo de la conexión a internet
	Y si no hay internet ejecuta la función stop"""
	global tira_led
	global infinito
	while infinito:
		w = subprocess.Popen(["ping", "-c 1", "www.google.com"], stdout=subprocess.PIPE)
		w.wait()
		if w.poll():
			tira_led = False
			stop()
			print ("No hay internet")
			linterna()
			time.sleep(1)
		else:
			print ("Si hay internet")
			tira_led = True
			time.sleep(1)


"""-------------TIRA LED PARA DECORACIÓN Y SEÑAL DE PÉRDIDA DE INTERNET---------------"""
#Definimos el pin 24 xGPIO board el cual controlará el color rojo de la tira led
tira_rojo = 25
#Colocamos el pin del led rojo como salida
GPIO.setup(tira_rojo, GPIO.OUT)
#Definimos el pin 24 xGPIO board el cual controlrá el color verde de la tira led
tira_verde = 10
#Colocamos el pin del led verde como salida
GPIO.setup(tira_verde, GPIO.OUT)
#Definimos el pin 24 xGPIO board el cual controlará el color azul de la tira led
tira_azul = 9
#Colocamos el pin del led azul como salida
GPIO.setup(tira_azul, GPIO.OUT)
colores = ("000", "011", "001", "101", "100", "110", "010")
#Variable que controla el ciclo infinito de la vizualización de la tira led
tira_led = True


def color(R, G, B):
	"""Color"""
	GPIO.output(tira_rojo, R)
	GPIO.output(tira_verde, G)
	GPIO.output(tira_azul, B)


def whitru():
	"""Ejecuta el ciclo infinito para la visualización de la tira led"""
	print ("Tira Ok")
	global tira_led
	global infinito
	#Mientras que el valor de la tira led sea verdadero
	for todo in colores:
		print ((todo[0], todo[1], todo[2]))
		color(int(todo[0]), int(todo[1]), int(todo[2]))
		time.sleep(2)
		if (tira_led is False):
			break
		if (infinito is False):
			break


def whifalse():
	"""No se"""
	print("Tira NOOOOO")
	GPIO.output(tira_rojo, 0)
	GPIO.output(tira_verde, 1)
	GPIO.output(tira_azul, 1)
	#Espera 0.5 segundos
	time.sleep(1)
	#Apga el color rojo
	GPIO.output(tira_rojo, 1)
	#Espera 0.5 segundos
	time.sleep(1)


def tira():
	"""Control total de la tira led"""
	#Mientras que la variable tira_led sea True
	global tira_led
	global infinito
	while infinito:
		if (tira_led is True):
			whitru()
		if (tira_led is False):
			print("Tira False")
			whifalse()


"""----------------------CONTROL DE LOS HILOS EN EJECUCIÓN----------------------------"""
global infinito
infinito = True
#Inicia el hilo que comprueba si hay internet
hilo_internet = threading.Thread(target=internet)
#Inicia el hilo que hace funcionar la tira led para estética y comprobar el internet
hilo_tira = threading.Thread(target=tira)
#Inicia el hilo de internet
hilo_internet.start()
#Inicia el hilo de la tira led
hilo_tira.start()


"""-----------------CONTROL DE VARIABLES PROVENIENTES DEL SERVIDOR--------------------"""


@webiopi.macro
def Aceleracion(value):
	"""Función que recibe los datos del deslizador de la página web de la aceleración
	y ejecuta la función de acelrar"""
	acelerar(value)


@webiopi.macro
def BotonAdelante():
	"""Función que recibe los datos del botón de adelante de la página web
	y ejecuta la función de adelante"""
	adelante()


@webiopi.macro
def BotonReversa():
	"""Función que recibe los datos del botón de atrás de la página web
	y ejecuta la función de reversa"""
	reversa()


@webiopi.macro
def BotonDerecha():
	"""Función que recibe los datos del botón de derecha de la página web
	y ejecuta la función de derecha"""
	derecha()


@webiopi.macro
def BotonIzquierda():
	"""Función que recibe los datos del botón de izquierda de la página web
	y ejecuta la función de izquierda"""
	izquierda()


@webiopi.macro
def servo1(valor):
	"""Función que recibe los datos del deslizador de la página web del movimiento del servo
	y ejecuta la función servo01"""
	servo01(valor)


@webiopi.macro
def servo2(valor):
	"""Función que recibe los datos del deslizador de la página web del movimiento del servo
	y ejecuta la función servo02"""
	servo02(valor)


@webiopi.macro
def BotonStop():
	"""Función que recibe los datos del botón de parar de la página web
	y ejecuta la función stop"""
	stop()


@webiopi.macro
def luz():
	"""Función que recibe los datos del botón de luz de la página web
	y ejecuta la función linterna"""
	linterna()


"""---------------------------DESTRUYE LAS VARIABLES USADAS---------------------------"""


def destroy():
	"""Destruye todas las variables"""
	global infinito
	GPIO.cleanup()
	infinito = False