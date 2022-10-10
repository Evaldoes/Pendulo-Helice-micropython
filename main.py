from machine import Timer, Pin, PWM, UART, ADC
from time import sleep
from mpu6050 import mpu6050_get_gyro_values

frequency = 50
motor = PWM(Pin(26), frequency)
MPU_interrupt = Pin(27, Pin.IN)
# giro = mpu6050.MPU6050()
# motor.duty(0)
# ENABLE = Pin()
gyroDataY = []
u = [0.0, 0.0]
y = [0.0, 0.0]
ao = -0.980198673306755
bo = 0.019801326693245
systemOutput = 0.0
input = 0.0
outputOld = 0.0
gyroTime = Timer(0)
counter = 1
listOld = []
listNew = []
# pot = ADC(Pin(34))
# pot.width(ADC.WIDTH_10BIT)
# pot.atten(ADC.ATTN_11DB)
isCalibrated = False

testRunnig = False

uart2 = UART(2, baudrate=115200, tx=17, rx=16)

duty_map = 0


# mpu6050_init()
def getNewSample(pin):
    try:
        # giro.teste()
        # print(mpu6050_get_gyro_values())
        data = mpu6050_get_gyro_values()
        if len(data) != None:
            emulated_plant(data[0], duty_map)
            # print(data)
        # led_adjustment()
    except TypeError:
        # print('entro aqui')
        pass


def emulated_plant(gyroInput, current_duty):
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
    # print("value = {}\n duty = {}\n\n".format(listOld, listNew))
    message = '{},{},{}\n'.format(str(counter), str(round(outputOld, 2)), str(round(current_duty, 4)))
    counter += 1
    # print("teste =  {}".format(gyroInput))
    uart2.write(message.encode())
    print(str(round(outputOld, 2)))
    return systemOutput


def led_adjustment():
    gyroDataY = mpu6050_get_gyro_values()
    # emulated_plant(gyroDataY[0], duty_map)


def mapPotenciometer(value, in_min, in_max, out_min, out_max):
    scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    print(scaled_value)
    return scaled_value


# micropython.alloc_emergency_exception_buf(100)

MPU_interrupt.irq(trigger=Pin.IRQ_RISING, handler=getNewSample)

while True:

    # if (isCalibrated == False):
    #     # pot_value = 1023
    #     # duty_cycle = /
    #     motor.duty(int(mapPotenciometer(1023, 0, 1023, 51.15, 102.3)))
    #     sleep(2)
    #     # pot_value = 0
    #     # duty_cycle = mapPotenciometer(pot_value, 0, 1023, 51.15, 102.3
    #     motor.duty(int(mapPotenciometer(0, 0, 1023, 51.15, 102.3)))
    #
    #     # motor.duty(int(duty_cycle))
    #     sleep(3)
    #     isCalibrated = True
    ######################################333
    sleep(5)
    if (testRunnig == False):
        # gyroTime.init(period=200, callback=led_adjustment())  # periodo e em mili
        # for x in range(1, 5):
        # duty_map = int(mapPotenciometer((x * 4.97), 0, 90, 51.2, 102.4))
        motor.duty(60)

        sleep(20)
        testRunnig = True

############################33333333
# pot_value = pot.read()
# print('Pot:'.format(pot_value))
# duty_cycle = mapPotenciometer(pot_value, 0, 1023, (1023 / 20), (1023 / 10))
# # print(duty_cycle)
# print('duty:'.format(duty_cycle))
# motor.duty(int(duty_cycle))
# sleep(0.1)
