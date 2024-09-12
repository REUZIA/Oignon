import machine
from utime import sleep

uart= machine.UART(1,baudrate=9600)  # initialisation UART

while True:
    if uart.any():  # si nous avons reçu quelque chose...
        print(uart.readline().decode('utf-8'))  # noud affichons le message reçu
    sleep(0.5)