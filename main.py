from mpu6050 import  print_data, mpu6050_init, mpu6050_get_gyro_values
from machine import Timer, Pin, PWM, UART
from time import sleep

gyroDataY = []
ao = -0.980198673306755
bo = 0.019801326693245
systemOutput = 0.0
input = 0.0
outputOld = 0.0
gyroTime = Timer(0)

counter = 1
listOld = []
listNew = []

u = [0.0, 0.0]
y = [0.0, 0.0]

pwm = PWM(Pin(2), freq=1000, duty=0)
uart2 = UART(2, baudrate=115200, tx=17, rx=16)


def emulated_plant(gyroInput):
    global counter
    outputOld = gyroInput

    # listOld.append(outputOld)
    u[0] = gyroInput
    y[0] = bo * u[1] - ao * y[1]

    y[1] = y[0]  ## atualiza a saída do sistema
    u[1] = u[0]  ## atualiza o esforço



    systemOutput = y[0]
    # listNew.append(systemOutput)
    # uart.write('{},{}'.format(outputOld,systemOutput))
    # print("old = {}\nnew = {}\n\n".format(listOld, listNew))

    message = '{},{},{}\n'.format(counter, outputOld,systemOutput)
    counter += 1
    uart2.write(message.encode())
    print(message)
    return systemOutput


def led_adjustment():
    gyroDataY = mpu6050_get_gyro_values()
    emulated_plant(gyroDataY[0])


while True:
    gyroTime.init(period=2000, mode=Timer.PERIODIC, callback=led_adjustment())
    # for i in range(0, 1023):
    #     print(i)
    #     pwm.duty(i)
    #     sleep(0.1)
    #     pwm.duty(0)
    # pwm.deinit()

    # mpu6050_init()
    # print_data()
    # button_callback()

## motor2


#
# from machine import Pin, PWM, ADC
# from time import sleep
# import random
#
# frequency = 50
#
# motor = PWM(Pin(2), frequency)
# pot = ADC(Pin(34))
# pot.width(ADC.WIDTH_10BIT)
# pot.atten(ADC.ATTN_11DB)
#
#
# def scale_value(value, in_min, in_max, out_min, out_max):
#     scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#     return scaled_value
#
#
# def teste():
#     return random.randrange(0, 350)
#
#
# while True:
#     # motor = PWM(Pin(2), frequency)
#     pot_value = teste()
#     duty_cycle = scale_value(pot_value, 0, 1023, (1023 / 20), (1023 / 10))
#     print(duty_cycle)
#     motor.duty(int(duty_cycle))
#     sleep(0.1)
#
