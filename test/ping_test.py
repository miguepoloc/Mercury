# -*- coding: utf-8 -*-
import subprocess
import time


def internet():
	"""Realiza un ping a google"""
	while True:
		w = subprocess.Popen(["ping", "-c 1", "www.google.com"],
			stdout=subprocess.PIPE)
		w.wait()
		if w.poll():
			print ("No hay internet")
			time.sleep(0.5)
		else:
			print ("Si hay internet")
			time.sleep(0.5)

internet()