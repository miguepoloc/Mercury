#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO         #Importamos la librería GPIO
import time                     #Importamos time (time.sleep)
GPIO.setmode(GPIO.BCM)          #Ponemos la placa en modo BCM

def obstaculo():                       #Función encargada de detectar un obstáculo
    TRIGGER = 25                    #Usamos el pin GPIO 25 como TRIGGER
    ECHO = 24                       #Usamos el pin GPIO 7 como ECHO
    GPIO.setup(TRIGGER,GPIO.OUT)    #Configuramos Trigger como salida
    GPIO.setup(ECHO,GPIO.IN)        #Configuramos Echo como entrada
    GPIO.output(TRIGGER,False)      #Ponemos el pin 25 como BAJO
    GPIO.output(TRIGGER,True)           #Enviamos un pulso de ultrasonidos
    time.sleep(0.00001)                 #Una pequeñña pausa
    GPIO.output(TRIGGER,False)          #Apagamos el pulso
    start = time.time()                 #Guarda el tiempo actual mediante time.time()
    while GPIO.input(ECHO)==0:          #Mientras el sensor no reciba señal...
        start = time.time()             #Mantenemos el tiempo actual mediante time.time()
    while GPIO.input(ECHO)==1:          #Si el sensor recibe una señal...
        stop = time.time()              #Guarda el tiempo actual mediante time.time() en otra variable
    duracion = stop-start               #Obtenemos el tiempo transcurrido entre envío y recepción
    distancia = (duracion * 34300)/2    #Distancia es igual al tiempo por la velocidad dividido en 2   D = (T x V)/2
    print "El obstáculo se encuentra a: "+str(distancia)+" cm" #Devolvemos la distancia (en centímetros) por pantalla
    return distancia                    #Retorna el valor de la distancia a la cual se encuentra el obstáculo

def main():         #Función principal
    repite=True     #Variable que define al ciclo infinito
    while repite:   # Se inicia un ciclo infinito
        try:
            obstaculo()             #Se llama a la función Lux
            time.sleep(1)           #Realiza este proceso cada 1 segundo
        except KeyboardInterrupt:   #Si se preciona ctrl C...
            repite=False            #Termina el ciclo infinito y se finaliza el programa
            print "Fin del programa"    #Imprime que se ha finalizado el programa
            GPIO.cleanup()              #Limpiamos los pines GPIO y salimos

if __name__=="__main__":    #Función para llamar a la función principal
   main()                   #Función principal