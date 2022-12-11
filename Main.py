import serial
import speech_recognition as sr
from datetime import date
from time import sleep

BlueToothSerial = serial.Serial("/dev/rfcomm7",115200)
print("BlueTooth Connected")

r = sr.Recognizer()
mic = sr.Microphone()
print("Connect Recognizer")
try :
    while 1:
        with mic as source:
            audio = r.listen(source)
        words = r.recognize_google(audio)
        print(words)
        if words == "today":
            print(date.today())
        if words == "home":
            print("Set CNC Homing Command")
            x = "$X\r \n"
            BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)
            x = "$H\r \n"
            BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)
        if words == "exit":
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            break
