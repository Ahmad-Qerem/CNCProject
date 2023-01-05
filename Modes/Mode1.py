
import sys
sys.path.append('/home/aa/graduation project/CNCProject/Utils')
from AngleMeterO.AngleMeterO import AngleMeter
from Recognizer import Recognizer
class Mode1:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Flag = False
        self.GyroscopeToCnc()
        print("New Mode1 Object Has been created ")

        
    def callBack(self, recognizer, audio):
        print("callBack Mode1")

        try:
            word = recognizer.recognize_google(audio, key=None, language='en-US')
            print(word)
            if word == "hello":
                self.BS.PenDown()
            elif word == "stop" :
                self.BS.PenRaise()
            elif word == "home" :
                self.BS.PenRaise()  
                self.BS.CncHome()
            elif word == "disconnect":
                self.Flag = True
                self.recognizer.StopListen()
            else:
                print(" Something ... Mode 1")
        except LookupError:
            print("Could not understand audio")
        except IndexError:
            print("no internet connection")
        except Exception as e:
            print("error in callback ")
            print("Error"+str(e))

    def PositionToGRBLCommand(self, xPosition, yPosition):
        if xPosition == "ideal" and yPosition == "ideal":
            pass
            #print("this is ideal")
        elif xPosition == "forward" and yPosition == "ideal":
            self.BS.SendPositionToCnc(10, 0)
            print("this is forward")
        elif xPosition == "backward" and yPosition == "ideal":
            self.BS.SendPositionToCnc(-10, 0)
        elif xPosition == "ideal" and yPosition == "right":
            self.BS.SendPositionToCnc(0, 10)
        elif xPosition == "ideal" and yPosition == "left":
            self.BS.SendPositionToCnc(0, -10)
        elif xPosition == "forward" and yPosition == "right":
            self.BS.SendPositionToCnc(10, 10)
        elif xPosition == "backward" and yPosition == "left":
            self.BS.SendPositionToCnc(-10, -10)
        elif xPosition == "backward" and yPosition == "right":
            self.BS.SendPositionToCnc(-10, 10)
        elif xPosition == "forward" and yPosition == "left":
            self.BS.SendPositionToCnc(10, -10)

    def GyroscopeToCnc(self):
        angleMeter = AngleMeter()
        angleMeter.measure()
        print("Gyroscope Connected")
        xPosition = "ideal"
        yPosition = "ideal"
        self.BS.CncHome()
        self.recognizer.StartListen(self.callBack)
        while True:
            if self.Flag:
                break
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
            stringToPrint = f"X : {x}\t Y: {y}"
            stringToPrint2 = f"X Position : {xPosition}\t Y Position: {yPosition}"
            #print('-' * len(stringToPrint2))
            #print(stringToPrint)
            #print(stringToPrint2)
            self.PositionToGRBLCommand(xPosition, yPosition)
        angleMeter.StopMeasure()
        print("Gyroscope Disconnected")