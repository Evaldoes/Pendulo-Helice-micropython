from machine import Pin, I2C
from time import sleep

MPU6050_ADDR = 0x68  # Endereço I2C padrão para o MPU6050
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
# mpu6050_int = Pin(2, Pin.IN, Pin.PULL_UP)
# led = Pin(2, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)

# endereços Power Management (Hex)
PWR_MGMT_1 = 0x6B
INT_ENABLE = 0x38

# endereços do sensor de temperatura (Hex)
TEMP_OUT_L = 0x42
TEMP_OUT_H = 0x41
TEMP_SENSITIVITY_LSBC = 340.0
TEMP_OFFSET = 36.53  # bits menos significativos por centigrado

# endereços do acelerometro (Hex)
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
ACCEL_SENSITIVITY_LSBG = 13384.0  # bits menos significativos por força gravitacional

# endereços do giroscopio (Hex)
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48
GYRO_SENSITIVITY_LSBG = 131.0  # bits menos significativos por grau por segundo


def mpu6050_init():
    i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, bytes([0]))
    i2c.writeto_mem(MPU6050_ADDR, INT_ENABLE, bytes([1]))  # enable interrupt on data ready (DATA_READ_EN)


def teste():
    # mpu6050_int.irq(trigger=Pin.IRQ_FALLING, handler=print_data())
    print('entrou aqui')


# def interrupt_data():
#     mpu6050_init()
#     # mpu6050_int = Pin(2, Pin.IN, Pin.PULL_UP)
#     mpu6050_int.irq(trigger=Pin.IRQ_FALLING, handler=print_data)
#

def combine_register_values(highValue, lowValue):
    if not highValue[0] & 0x80:
        return highValue[0] << 8 | lowValue[0]
    return -((highValue[0] ^ 255) << 8) | (lowValue[0] ^ 255) + 1


def mpu6050_get_temp_celsius():
    mpu6050_init()
    temp_high = i2c.readfrom_mem(MPU6050_ADDR, TEMP_OUT_H, 1)
    temp_low = i2c.readfrom_mem(MPU6050_ADDR, TEMP_OUT_L, 1)
    return (combine_register_values(temp_high, temp_low) / TEMP_SENSITIVITY_LSBC) + TEMP_OFFSET


def mpu6050_get_accel_values():
    mpu6050_init()
    accel_x_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_H, 1)
    accel_x_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_XOUT_L, 1)
    accel_y_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_H, 1)
    accel_y_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_L, 1)
    accel_z_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_ZOUT_H, 1)
    accel_z_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_ZOUT_L, 1)
    return [
        combine_register_values(accel_x_high, accel_x_low) / ACCEL_SENSITIVITY_LSBG,
        combine_register_values(accel_y_high, accel_y_low) / ACCEL_SENSITIVITY_LSBG,
        combine_register_values(accel_z_high, accel_z_low) / ACCEL_SENSITIVITY_LSBG,
    ]


def mpu6050_get_gyro_values():
    mpu6050_init()
    gyro_x_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_H, 1)
    gyro_x_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_XOUT_L, 1)
    gyro_y_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_H, 1)
    gyro_y_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_YOUT_L, 1)
    gyro_z_high = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_ZOUT_H, 1)
    gyro_z_low = i2c.readfrom_mem(MPU6050_ADDR, ACCEL_ZOUT_L, 1)
    return [
        combine_register_values(gyro_x_high, gyro_x_low) / GYRO_SENSITIVITY_LSBG,
        combine_register_values(gyro_y_high, gyro_y_low) / GYRO_SENSITIVITY_LSBG,
        combine_register_values(gyro_z_high, gyro_z_low) / GYRO_SENSITIVITY_LSBG,
    ]


def print_data():
    print("Temperature:\t", mpu6050_get_temp_celsius(), "°C")
    print("Accelerometer:\t", mpu6050_get_accel_values(), "g")
    print("Gyroscope:\t", mpu6050_get_gyro_values(), "°/s")
    # mpu6050_int.value(not mpu6050_int.value())
    # led.value(not led.value())
    print("\n\n")
    sleep(1.5)


# def button_callback():
#     print('entrou aqui')
#     button.irq(trigger=Pin.IRQ_FALLING, handler=lambda t: led.value(not led.value()))
