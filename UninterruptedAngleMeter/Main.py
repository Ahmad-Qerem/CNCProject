import serial
import speech_recognition as sr
from datetime import date
from AngleMeterAlpha import AngleMeterAlpha
from time import sleep
import cv2

GlobalWord=""
Flag=True
DELAY=1
XVal=0
YVal=0
#what to do after each voice recognitions
def callBack(recognizer, audio ):
    global GlobalWord
    GlobalWord=recognizer.recognize_google(audio)
    global Flag
    Flag=True
    print(GlobalWord)

def ClearLines(NLines=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2k'
    for idx in range(NLines):
        print(LINE_UP, end=LINE_CLEAR)
def SendPosition(BlueToothSerial,xPosition,yPosition,Pen):
    if xPosition=="ideal" and yPosition=="ideal":
        pass
    elif xPosition=="forward" and yPosition=="ideal":
        global XVal
        XVal+=10
        x = f"G1 X{XVal} Y{0} F1000 \r \n"
        BlueToothSerial.write(x.encode("utf-8"))
    elif xPosition == "backward" and yPosition == "ideal":
        global XVal
        XVal -= 10
        x = f"G1 X{XVal} Y{0} F1000 \r \n"
        BlueToothSerial.write(x.encode("utf-8"))
    elif xPosition == "ideal" and yPosition == "right":
        global YVal
        YVal += 10
        x = f"G1 X{0} Y{YVal} F1000 \r \n"
        BlueToothSerial.write(x.encode("utf-8"))
    elif xPosition == "ideal" and yPosition == "lift":
        global YVal
        YVal -= 10
        x = f"G1 X{0} Y{YVal} F1000 \r \n"
        BlueToothSerial.write(x.encode("utf-8"))
    sleep(DELAY)


def GetDestination(BlueToothSerial):
    angleMeter = AngleMeterAlpha()
    angleMeter.measure()
    print("Gyroscope Connected")
    PinFlag = False
    Pen="up"

    print("Set CNC Homing Command")
    x = "$X\r \n"
    BlueToothSerial.write(x.encode("utf-8"))
    sleep(DELAY)

    x = "$H\r \n"
    BlueToothSerial.write(x.encode("utf-8"))
    sleep(DELAY*10)

    x = "G92 X0 Y0 \r \n"
    BlueToothSerial.write(x.encode("utf-8"))
    sleep(DELAY)
    print("Homing Finished")

    while True:
        global GlobalWord
        if GlobalWord == "disconnect":
            break

        elif GlobalWord == "start" and not PinFlag:
            PinFlag = True
            Pen="down"

        elif GlobalWord == "stop" and PinFlag:
            PinFlag = False
            Pen="up"

        x=angleMeter.get_kalman_roll()
        y=angleMeter.get_kalman_pitch()
        xPosition="ideal"
        yPosition = "ideal"

        if x<20 and x>-20:
            xPosition = "ideal"
        elif x<80 and x>20:
            xPosition = "forward"
        elif x>-60 and x<-30:
            xPosition = "backward"

        if y<20 and y>-20:
            yPosition = "ideal"
        elif y<80 and y>20:
            yPosition = "left"
        elif y>-60 and y<-30:
            yPosition = "right"

        stringToPrint = f"X : {x}\t Y: {y}\t Pen Status : {Pen}"
        stringToPrint2 = f"X Position : {xPosition}\t Y Position: {yPosition}\t Pen Status : {Pen}"
        print('-' * len(stringToPrint2))
        print(stringToPrint)
        print(stringToPrint2)
        SendPosition(BlueToothSerial,xPosition,yPosition,Pen)
        #ClearLines(3)
        # print(angleMeter.get_int_roll(), angleMeter.get_int_pitch())
    angleMeter.StopMeasure()

#Main program start here
def main():
    while True:
        try:
            # connincting bluetooth with hc05 module at comm port 7 with 115200 baudrate
            BlueToothSerial = serial.Serial("/dev/rfcomm7",115200)
            print("BlueTooth Connected")

            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            print("Connect Recognizer")

            # Remove noise from the background
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
            # Start thread for voice recognition
            ThreadInBackGround = recognizer.listen_in_background(mic, callBack)

            while True:
                global Flag
                if GlobalWord == "today" and Flag:
                    Flag = False
                    print(date.today())

                elif (GlobalWord == "mode 1" or GlobalWord == "mode one") and Flag:
                    Flag = False
                    GetDestination(BlueToothSerial)



                elif GlobalWord == "camera" and Flag:
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

                elif GlobalWord == "exit":
                    ThreadInBackGround()
                    print("...")
                    sleep(1)
                    print("...")
                    sleep(1)
                    print("...")
                    sleep(1)
                    print("Goodbye")
                    break
                else:
                    sleep(1)
                    print("...")

        except speech_recognition.UnknownValueError():
            recognizer = sr.Recognizer()
            continue

if __name__ == "__main__":
    main()