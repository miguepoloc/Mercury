#!/usr/bin/python
# -*- coding: utf-8 -*-
#Importamos la librería GPIO
import RPi.GPIO as GPIO
import time
#Ponemos la placa en modo BCM
GPIO.setmode(GPIO.BCM)


def obstaculo():
	"""Función encargada de detectar un obstáculo"""
	#Usamos el pin GPIO 25 como TRIGGER
	TRIGGER = 20
	#Usamos el pin GPIO 7 como ECHO
	ECHO = 21
	#Configuramos Trigger como salida
	GPIO.setup(TRIGGER, GPIO.OUT)
	#Configuramos Echo como entrada
	GPIO.setup(ECHO, GPIO.IN)
	#Ponemos el pin 25 como BAJO
	GPIO.output(TRIGGER, False)
	#Enviamos un pulso de ultrasonidos
	GPIO.output(TRIGGER, True)
	#Una pequeñña pausa
	time.sleep(0.00001)
	#Apagamos el pulso
	GPIO.output(TRIGGER, False)
	#Guarda el tiempo actual mediante time.time()
	start = time.time()
	#Mientras el sensor no reciba señal
	while GPIO.input(ECHO) == 0:
		#Mantenemos el tiempo actual mediante time.time()
		start = time.time()
	#Si el sensor recibe una señal...
	while GPIO.input(ECHO) == 1:
		#Guarda el tiempo actual mediante time.time() en otra variable
		stop = time.time()
	#Obtenemos el tiempo transcurrido entre envío y recepción
	duracion = stop - start
	#Distancia es igual al tiempo por la velocidad dividido en 2   d = (t x v)/2
	distancia = (duracion * 34300) / 2
	#Devolvemos la distancia (en centímetros) por pantalla
	print ("El obstáculo se encuentra a: " + str(distancia) + " cm")
	#Retorna el valor de la distancia a la cual se encuentra el obstáculo
	return distancia


def main():
	"""Función principal"""
	#Variable que define al ciclo infinito
	repite = True
	#Se inicia un ciclo infinito
	while repite:
		try:
			#Se llama a la función obstáculo
			obstaculo()
			#Realiza este proceso cada 1 segundo
			time.sleep(1)
		#Si se preciona ctrl C...
		except KeyboardInterrupt:
			#Termina el ciclo infinito y se finaliza el programa
			repite = False
			#Imprime que se ha finalizado el programa
			print ("Fin del programa")
			#Limpiamos los pines GPIO y salimos
			GPIO.cleanup()

#Función para llamar a la función principal
if __name__ == "__main__":
	#Función principal
	main()