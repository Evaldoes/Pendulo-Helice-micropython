import os
from serial import Serial
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
from matplotlib import style
import datetime as dt


port = Serial('/dev/ttyUSB1', baudrate=115200, timeout=1000)
init = False
step = False

outputOld = str()
systemOutput = str()


try:
    while True:
        received = port.read(1)
        received = received.decode()
        if received == '$':
            init = True
            continue

        if received == ',':
            step = True
            continue

        if received == '#':
            init = False
            step = False

            if outputOld != '' and systemOutput != '':
                print(outputOld)
            outputOld = str()
            systemOutput = str()
            continue

        if init and step is False:
            outputOld += received
            continue

        if init and step:
            systemOutput += received

except KeyboardInterrupt as e:
    pass

finally:
    port.close()
