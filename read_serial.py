# import animate as animate
import os
from serial import Serial
import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation
from matplotlib import style
import datetime as dt

serialPort = Serial('/dev/ttyUSB1', baudrate=115200, timeout=10000)
# serialPort.open()
init = False
step = False
outputOld = str()
systemOutput = str()

# inicializa a serial port
if serialPort.isOpen:
    print('\nTudo Certo, Serial port está aberta. Configuração:\n')
    print(serialPort, "\n")  # print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
sample = []  # store trials here (n)
gyroXData = []  # store relative frequency here
systemOutputData = []  # for theoretical probability


# This function is called periodically from FuncAnimation
def animate(i, sample, gyroXData):
    # Aquire and parse data from serial port
    line = serialPort.readline()  # ascii
    # print(line)
    line_as_list = line.split(b',')
    print(line_as_list)
    j = float(line_as_list[0])
    # print(j)
    gyroData = line_as_list[1]
    gyroData_as_list = gyroData.split(b'\n')
    gyroData_float = float(gyroData_as_list[0])
    # print(gyroData_float)

    systemOutput = line_as_list[2]
    systemOutput_as_list = systemOutput.split(b'\n')
    systemOutput_float = float(systemOutput_as_list[0])

    # Add x and y to lists
    sample.append(j)
    gyroXData.append(gyroData_float)
    systemOutputData.append(systemOutput_float)

    # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(sample, gyroXData, label="Dado do Giroscópio")
    ax.plot(sample, systemOutputData, label="Saida do Sistema")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    plt.title('Pêndulo Hélice')
    plt.ylabel('°/s')
    plt.xlabel('Tempo (ms)')

    plt.legend()
    # plt.axis([1, None, 0, 1.1])  # Use for arbitrary number of trials
    # plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(sample, gyroXData), interval=100)
plt.show()
# try:
#     while True:
#         received = port.read(1)
#         received = received.decode()
#         if received == '$':
#             init = True
#             continue
#
#         if received == ',':
#             step = True
#             continue
#
#         if received == '#':
#             init = False
#             step = False
#
#             if outputOld != '' and systemOutput != '':
#
#
#             outputOld = str()
#             systemOutput = str()
#             continue
#
#         if init and step is False:
#             outputOld += received
#             continue
#
#         if init and step:
#             systemOutput += received
#
# except KeyboardInterrupt as e:
#     pass
#
# finally:
#     port.close()
