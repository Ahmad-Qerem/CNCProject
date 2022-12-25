import sys
import serial
import speech_recognition as sr
from datetime import date
from time import sleep
import cv2

sys.path.append('/home/oth/AmrAhmedGradProject/CNCProject/UninterruptedAngleMeter')
from AngleMeterAlpha import AngleMeterAlpha as Gyroscope


class CncController:
    def ConnectBlueTooth(self):
        try:
            self.BlueToothSerial = serial.Serial("/dev/rfcomm7", 115200)
            # wake up cnc
            self.BlueToothSerial.write("\n".encode("utf-8"))
            sleep(2)
            # clear cnc message
            self.BlueToothSerial.flushInput()
            print("BlueTooth Connected ")
        except Exception as e:
            print("Something Go Wrong In Bluetooth")
            print("Error:"+str(e))

    def ConnectRecognizer(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        # Remove noise from the background
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Recognizer Is Ready To Listen ")

    def callBack(self, recognizer, audio):
        try:
            self.GlobalWord = recognizer.recognize_google(audio)
            self.GlobalWord = self.GlobalWord.lower()
            print(self.GlobalWord)
            self.RecognizeToDo()
        except LookupError:
            print("Could not understand audio")
        except IndexError:
            print("no internet connection")

    def StartListen(self):
        self.ThreadListenInBackGround = self.recognizer.listen_in_background(
            self.mic, self.callBack)

    def StopListen(self):
        self.ThreadListenInBackGround()

    def ConnectToCamera(self):
        self.Capture = cv2.VideoCapture("http://192.168.1.6:8080/video")
        print("Camera Connected")
        while True:
            _, frame = self.Capture.read()
            cv2.imshow("tic tac toe", frame)
            if cv2.waitKey(1) == ord('q') or self.GlobalWord == "disconnect":
                break
        self.Capture.release()
        cv2.destroyAllWindows()
        print("Camera Disconnected")

    def SendCommandToCnc(self, Command):
        print("Sending :"+Command)
        x = Command+"\n"
        self.BlueToothSerial.write(x.encode("utf-8"))
        GRBLOut = self.BlueToothSerial.readLine()
        print("GRBL :"+GRBLOut.strip())

    def CncHome(self):
        print("CNC Homing")
        self.SendCommandToCnc("$X")
        self.SendCommandToCnc("$H")
        self.SendCommandToCnc("G92 X0 Y0")
        self.XVal = 0
        self.YVal = 0
        print("Homing Finished")

    def SendPositionToCnc(self, X=0, Y=0):
        self.XVal += X
        self.YVal += Y
        CommandToSend = f"G91 X{X} Y{Y} F200"
        self.SendCommandToCnc(CommandToSend)

    def PositionToGRBLCommand(self, xPosition, yPosition, Pen):
        if Pen == "down" and not self.PenFlag:
            self.SendCommandToCnc("M3 S45")
            self.PenFlag = True
        elif Pen == "up" and self.PenFlag:
            self.SendCommandToCnc("M5")
            self.PenFlag = False

        if xPosition == "ideal" and yPosition == "ideal":
            pass
        elif xPosition == "forward" and yPosition == "ideal":
            self.SendPositionToCnc(10, 0)
        elif xPosition == "backward" and yPosition == "ideal":
            self.SendPositionToCnc(-10, 0)
        elif xPosition == "ideal" and yPosition == "right":
            self.SendPositionToCnc(0, 10)
        elif xPosition == "ideal" and yPosition == "lift":
            self.SendPositionToCnc(0, -10)
        elif xPosition == "forward" and yPosition == "right":
            self.SendPositionToCnc(10, 10)
        elif xPosition == "backward" and yPosition == "lift":
            self.SendPositionToCnc(-10, -10)
        elif xPosition == "backward" and yPosition == "right":
            self.SendPositionToCnc(-10, 10)
        elif xPosition == "forward" and yPosition == "lift":
            self.SendPositionToCnc(10, -10)

    def GyroscopeToCncMode(self):
        angleMeter = Gyroscope()
        angleMeter.measure()
        print("Gyroscope Connected")
        PinFlag = False
        Pen = "up"
        xPosition = "ideal"
        yPosition = "ideal"
        self.CncHome()

        while True:

            if self.GlobalWord == "disconnect":
                break

            elif self.GlobalWord == "start" and not PinFlag:
                PinFlag = True
                Pen = "down"

            elif self.GlobalWord == "stop" and PinFlag:
                PinFlag = False
                Pen = "up"

            x = angleMeter.get_kalman_roll()
            y = angleMeter.get_kalman_pitch()
            # angle to position
            if x < 20 and x > -20:
                xPosition = "ideal"
            elif x < 80 and x > 20:
                xPosition = "forward"
            elif x > -60 and x < -30:
                xPosition = "backward"

            if y < 20 and y > -20:
                yPosition = "ideal"
            elif y < 80 and y > 20:
                yPosition = "left"
            elif y > -60 and y < -30:
                yPosition = "right"

            stringToPrint = f"X : {x}\t Y: {y}\t Pen Status : {Pen}"
            stringToPrint2 = f"X Position : {xPosition}\t Y Position: {yPosition}\t Pen Status : {Pen}"
            print('-' * len(stringToPrint2))
            print(stringToPrint)
            print(stringToPrint2)
            self.PositionToGRBLCommand(xPosition, yPosition, Pen)

        angleMeter.StopMeasure()
        print("Gyroscope Disconnected")

    def RecognizeToDo(self):
        if self.GlobalWord == "today":
            print(date.today())

        elif (self.GlobalWord == "mode 1" or self.GlobalWord == "mode one"):
            self.GyroscopeToCncMode()

        elif self.GlobalWord == "camera":
            self.ConnectToCamera()

        elif self.GlobalWord == "exit":
            self.ThreadListenInBackGround()
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("...")
            sleep(1)
            print("Goodbye")
            exit(0)
        else:
            print("SomeThing ...")

    def __init__(self):
        self.GlobalWord = ""
        self.PenFlag = False
        self.DELAY = 1
        self.XVal = 0
        self.YVal = 0
        self.recognizer = None
        self.BlueToothSerial = None
        self.mic = None
        self.Capture = None
        self.ThreadListenInBackGround = None
        self.ConnectBlueTooth()
        self.ConnectRecognizer()
