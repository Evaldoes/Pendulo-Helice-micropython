# Pêndulo com hélice

Código do meu TCC em Engenharia da Computação: um pêndulo movido por hélice, com firmware em MicroPython para ESP32.

## Organização

- `main.py`, `motor.py`, `main_motor.py`, `boot.py`: firmware e acionamento do motor por PWM
- `mpu6050.py`: leitura do giroscópio MPU6050
- `wifimgr.py`: configuração do Wi-Fi da placa
- `read_serial.py`: grava em `data/` as medições recebidas pela porta serial
- `plotGraphOctave.m`, `media.m`: análise das medições no Octave
- `data/`: medições feitas em 2022
