import serial
import speech_recognition as sr
from datetime import date
from time import sleep
import cv2

GlobalWord=""
Flag=True
#what to do after each voice recognitions
def callBack(recognizer, audio ):
    global GlobalWord
    GlobalWord=recognizer.recognize_google(audio)
    global Flag
    Flag=True
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
ThreadInBackGround = recognizer.listen_in_background(mic,callBack)

#Main program start here
def main():
    while True:
        global Flag
        if GlobalWord == "today" and Flag:
            Flag=False
            print(date.today())

        if GlobalWord == "home" and Flag:
            Flag = False
            print("Set CNC Homing Command")
            x = "$X\r \n"
            BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)

            x = "$H\r \n"
            BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)

        if GlobalWord == "camera" and Flag:
            Flag = False
            print("Connecting camera ... ")
            captchaer = cv2.VideoCapture("http://192.168.1.9:8080/video")
            print("Connected")
            while True:
                _, frame = captchaer.read()
                cv2.imshow("test", frame)
                if GlobalWord == "disconnect":
                    break
            captchaer.release()
            cv2.destroyAllWindows()
            print("Camera Disconnected")

        if GlobalWord == "exit":
            ThreadInBackGround()
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            break

if __name__ == "__main__":
    main()

