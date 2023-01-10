
import sys
from time import sleep
sys.path.append('/home/aa/graduation project/CNCProject/Utils')
from AngleMeterO.AngleMeterO import AngleMeter
from Recognizer import Recognizer
class Mode1:
    disconnect = ['disconnect']
    start = ['start','hello','down']
    stop = ['stop','up']
    home = ['home']

    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Flag = False
        self.PenFlag= True
        self.Sent=True
        self.Delay=0.5
        self.recognizer.StartListen(self.callBack)
        print("New Mode1 Object Has been created ")

    def DecreaseDelay(self):
        if self.Delay >= 0.5 :
            self.Delay -= 0.5

    def IncreaseDelay(self):
        if self.Delay <= 2:
            self.Delay += 0.5

    def callBack(self, recognizer, audio):
        print("callBack Mode1")

        try:
            word = recognizer.recognize_google(
                audio_data=audio, key=None, language='en-US')
            print(word)
            if word in self.start:
                self.PenFlag = True
                self.Sent=False

            elif word in self.stop :
                self.PenFlag = False
                self.Sent=False

            elif word == 'slow':
                self.IncreaseDelay()
            elif word == 'fast':
                self.DecreaseDelay()
                
            elif word in self.home :
                self.Flag = True
                sleep(1)
                self.Flag = False
                self.GyroscopeToCnc()

            elif word in self.disconnect:
                self.Flag = True
                self.recognizer.StopListen()
            else:
                print(" Something ... Mode 1")
        except IndexError:
            print("no internet connection")
        except LookupError:
            print("Could not understand audio")
        except Exception as e:
            print("error in callback ")
            print("Error"+str(e))

    def PositionToGRBLCommand(self, xPosition, yPosition):
        if xPosition == "ideal" and yPosition == "ideal":
            pass
        elif xPosition == "forward" and yPosition == "ideal":
            self.BS.SendPositionToCnc(10, 0)
        elif xPosition == "backward" and yPosition == "ideal":
            self.BS.SendPositionToCnc(-10, 0)
        elif xPosition == "ideal" and yPosition == "right":
            self.BS.SendPositionToCnc(0, -10)
        elif xPosition == "ideal" and yPosition == "left":
            self.BS.SendPositionToCnc(0, 10)
        elif xPosition == "forward" and yPosition == "right":
            self.BS.SendPositionToCnc(10, -10)
        elif xPosition == "backward" and yPosition == "left":
            self.BS.SendPositionToCnc(-10, 10)
        elif xPosition == "backward" and yPosition == "right":
            self.BS.SendPositionToCnc(-10, -10)
        elif xPosition == "forward" and yPosition == "left":
            self.BS.SendPositionToCnc(10, 10)

    def GyroscopeToCnc(self):
        angleMeter = AngleMeter()
        angleMeter.measure()
        print("Gyroscope Connected")
        xPosition = "ideal"
        yPosition = "ideal"
        self.BS.CncHome()
        while True:
            if self.Flag:
                break

            if not self.Sent:
                self.Sent = True
                if self.PenFlag:
                    self.BS.PenDown()
                else:
                    print("this is up")
                    self.BS.PenRaise()
                
            sleep(self.Delay)
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

            # stringToPrint = f"X : {x}\t Y: {y}"
            # stringToPrint2 = f"X Position : {xPosition}\t Y Position: {yPosition}"
            # print('-' * len(stringToPrint2))
            # print(stringToPrint)
            # print(stringToPrint2)
            self.PositionToGRBLCommand(xPosition, yPosition)
        self.BS.PenRaise()
        angleMeter.StopMeasure()
        print("Gyroscope Disconnected")
