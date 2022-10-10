# Complete project details at https://RandomNerdTutorials.com

from machine import Timer, Pin, PWM, UART, ADC
from time import sleep

frequency = 50
motor = PWM(Pin(26), frequency)

motor.duty(0)
isCalibrated = False


def mapPotenciometer(value, in_min, in_max, out_min, out_max):
    scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return scaled_value


# mpu6050_init()
if (isCalibrated == False):
    print('entrou no boot')

    # pot_value = 1023
    # duty_cycle = /
    sleep(5)
    # motor.duty(int(mapPotenciometer(1023, 0, 1023, 51.15, 102.3)))
    # sleep(2)
    # pot_value = 0
    # duty_cycle = mapPotenciometer(pot_value, 0, 1023, 51.15, 102.3
    motor.duty(int(mapPotenciometer(0, 0, 90, 51.2, 102.4)))

    # motor.duty(int(duty_cycle))
    sleep(5)
    isCalibrated = True













# try:
#   import usocket as socket
# except:
#   import socket
#
# from machine import Pin
# import network
#
# import esp
# esp.osdebug(None)
#
# import gc
# gc.collect()
#
# ssid = 'NET VIRTUA C50'
# password = '2222148330'
#
# station = network.WLAN(network.STA_IF)
#
# station.active(True)
# station.connect(ssid, password)
#
# while station.isconnected() == False:
#   pass
#
# print('Connection successful')
# print(station.ifconfig())
#
# led = Pin(2, Pin.OUT)