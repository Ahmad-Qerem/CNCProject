import serial
import speech_recognition as sr
from datetime import date
from time import sleep
import cv2

GlobalWord=""

#what to do after each voice recognitions
def callBack(recognizer, audio ):
    GlobalWord=recognizer.recognize_google(audio)
    print(GlobalWord)

#connincting bluetooth with hc05 module at comm port 7 with 115200 baudrate
BlueToothSerial = serial.Serial("/dev/rfcomm7",115200)
print("BlueTooth Connected")

recognizer = sr.Recognizer()
mic = sr.Microphone()
print("Connect Recognizer")

#Remove noise from the background
with mic as source:
    recognizer.adjust_for_ambient_noise(source)
#Start thread for voice recognition
recognizer.listin_inBackground(mic,callBack)

#Main program start here
while True:

    if GlobalWord == "today":
        print(date.today())

    if GlobalWord == "home":
        print("Set CNC Homing Command")
        x = "$X\r \n"
        BlueToothSerial.write(x.encode("utf-8"))
        sleep(1)

        x = "$H\r \n"
        BlueToothSerial.write(x.encode("utf-8"))
        sleep(1)

    if GlobalWord == "camera":
        print("Connecting camera ... ")
        captchaer = cv2.VideoCapture("http://192.168.1.9:8080/video")
        print("Connected")
        while True:
            _, frame = captchaer.read()
            cv2.imshow("test", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        captchaer.release()
        cv2.destroyAllWindows()
        print("Camera Disconnected")

    if GlobalWord == "exit":
        print("...")
        sleep(1)
        print("...")
        sleep(1)
        print("...")
        sleep(1)
        print("Goodbye")
        break