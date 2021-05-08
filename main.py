from mpu6050 import   teste, button_callback,print_data ,mpu6050_init, mpu6050_get_temp_celsius, mpu6050_get_gyro_values, mpu6050_get_accel_values


while True:
    mpu6050_init()
    print_data()
    button_callback()
