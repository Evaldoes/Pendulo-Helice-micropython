#coding: utf-8
import itertools
import threading
import time
import sys
import os

class begin:
	stop=False

	def __init__(self):
		pass

	def animate(self):
		for c in itertools.cycle(['\x1b[1;31m•    \x1b[1;36m|', '\x1b[1;32m••   \x1b[1;36m/', '\x1b[1;34m•••  \x1b[1;36m-', '\x1b[1;35m•••• \x1b[1;36m\\']):
		        if self.stop == True:
			   self.stop == False
			   sys.stdout.write("")
			   sys.stdout.flush()
			   return
		        else:
	        	   sys.stdout.write('\r\x1b[1;32mloading ' + c)
		           sys.stdout.flush()
        		   time.sleep(0.2)

	def star(self,text):
		    text = text.upper()
		    lo = 0
		    teln = len(text) - 1
		    while True:
		      if self.stop == True:
		         self.stop = False
			 return ""
		      else:
		         tek = text[:lo] + text[lo].swapcase() + text[lo+1:]
		         sys.stdout.write("\r\x1b[1;32m[+]\x1b[1;34m "+tek)
		         sys.stdout.flush()
		         time.sleep(0.2)
			 lo -=-1
			 if lo > teln:
		            lo = 0



	def start(self,tup="Subscribe JustA Hacker"):
	        t = threading.Thread(target=self.star,args=(tup,))
	        t.start()

        def play(self):
		b = threading.Thread(target=self.animate)
		b.start()
