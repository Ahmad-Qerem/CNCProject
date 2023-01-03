import serial
import time

bluetooth=serial.Serial("/dev/rfcomm7",115200)

while True:
    a=input("enter:-")
    string='X{0}'.format(a)
    bluetooth.write(a.encode("utf-8"))
