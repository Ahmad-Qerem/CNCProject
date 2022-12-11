#to connect the bluetooth write the fowlloing:
#$ hcitool scan
# this will show the bluetooth mac addres that connected
#sudo rfcomm connect hci0 <Mac Address> 1
#where <Mac Address> from the first command

#to install serial library
#$ sudo pip3 install pyserial


import serial
import time
BlueToothSerial = serial.Serial("/dev/rfcomm7",115200)
print("BlueTooth Connected")
try :
    while 1:
        x =input()
        x=x+'\r \n'
        BlueToothSerial.write(x.encode("utf-8"))
        time.sleep(1)

except KeyboardInterrupt:
    print("Quit")

