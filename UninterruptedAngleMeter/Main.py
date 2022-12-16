import serial
import speech_recognition as sr
from datetime import date
from AngleMeterAlpha import AngleMeterAlpha
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

def GetDestination():
    angleMeter = AngleMeterAlpha()
    angleMeter.measure()
    PinFlag = False
    Pin="up"
    while True:
        global GlobalWord
        if GlobalWord == "disconnect":
            break

        if GlobalWord == "start" and not PinFlag:
            PinFlag = True
            Pin="down"

        if GlobalWord == "stop" and PinFlag:
            PinFlag = False
            Pin="up"

        x=angleMeter.get_kalman_roll()
        y=angleMeter.get_kalman_pitch()
        xPosition="idel"
        yPosition = "idel"

        if x<20 or x>-20:
            xPosition = "idel"
        elif x<80 and x>20:
            xPosition = "forward"
        elif x>-60 and x<-30:
            xPosition = "backward"

        if y<20 or y>-20:
            yPosition = "idel"
        elif y<80 and y>20:
            yPosition = "left"
        elif y>-60 and y<-30:
            yPosition = "right"

        print(xPosition, ",", yPosition ,Pin)
        # print(angleMeter.get_int_roll(), angleMeter.get_int_pitch())
        sleep(1)
    angleMeter.StopMeasure()
#connincting bluetooth with hc05 module at comm port 7 with 115200 baudrate
#BlueToothSerial = serial.Serial("/dev/rfcomm7",115200)
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
        if (GlobalWord == "mode 1" or GlobalWord == "mode one") and Flag:
            Flag = False
            GetDestination()

        if GlobalWord == "home" and Flag:
            Flag = False
            print("Set CNC Homing Command")
            x = "$X\r \n"
            #BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)

            x = "$H\r \n"
            #BlueToothSerial.write(x.encode("utf-8"))
            sleep(1)

        if GlobalWord == "camera" and Flag:
            Flag = False
            print("Connecting camera ... ")
            captchaer = cv2.VideoCapture("http://192.168.1.6:8080/video")
            print("Connected")
            while True:
                _, frame = captchaer.read()
                cv2.imshow("test", frame)
                if cv2.waitKey(1) == ord('q') or GlobalWord == "disconnect":
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

