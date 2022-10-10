from machine import Pin, PWM, ADC
from time import sleep

frequency = 50
motor = PWM(Pin(2), frequency)
pot = ADC(Pin(34))
pot.width(ADC.WIDTH_10BIT)
pot.atten(ADC.ATTN_11DB)

isCalibrated = False


def mapPotenciometer(value, in_min, in_max, out_min, out_max):
    scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return scaled_value

def calibrateMotor():
    global isCalibrated
    if (isCalibrated != False):
        pot_value = 1023
        sleep(5)
        pot_value = 0
        isCalibrated = True


while True:
    # pot_value = pot.read()
    if (isCalibrated != False):
        pot_value = 1023
        sleep(2)
        pot_value = 0
        isCalibrated = True
    sleep(4)
    pot_value = 204
    print(pot_value)
    duty_cycle = mapPotenciometer(pot_value, 0, 1023, 51.15, 102.3)
    # duty_cycle = mapPotenciometer(pot_value, 0, 1023, (1023 / 20), (1023 / 10))
    print(duty_cycle)
    motor.duty(int(duty_cycle))
    sleep(0.1)
