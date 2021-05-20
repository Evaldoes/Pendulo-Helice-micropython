from mpu6050 import button_callback, print_data, mpu6050_init

while True:
    mpu6050_init()
    print_data()
    button_callback()
