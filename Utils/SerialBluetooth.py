
import os
from time import sleep
import serial

class Bluetooth:
    def __init__(self):
        self.XVal = 0
        self.YVal = 0
        self.Pen=True
        self.BlueToothSerial=None
        self.ConnectBlueTooth()
        print("New Bluetooth Object Has been created ")


    def ConnectBlueTooth(self):
        try:
            self.BlueToothSerial = serial.Serial("/dev/rfcomm0", 115200)
            # wake up cnc
            # self.BlueToothSerial.write("\n".encode("utf-8"))
            # sleep(2)
            # clear cnc message
            # self.BlueToothSerial.flushInput()
            print("BlueTooth Connected ")
        except Exception as e:
            print("Something Go Wrong In Bluetooth")
            print("Error:"+str(e))

    def SendCommandToCnc(self, Command):
        print("Sending :"+Command)
        x = Command+'\r \n'
        self.BlueToothSerial.write(x.encode("utf-8"))
        GRBLOut = self.BlueToothSerial.readline()
        print(GRBLOut.strip().decode("utf-8"))

    def SendPositionToCnc(self, X=0, Y=0):
        if (self.XVal+X) < 10 or (self.XVal+X) > 800:
            print("Out Of Range X")
            if (self.YVal+Y) < 10 or (self.YVal+Y) > 450:
                print("Out Of Range Y")
            else:
                self.YVal += Y
                CommandToSend = f"G91Y{Y}F2000"
                self.SendCommandToCnc(CommandToSend)
        elif (self.YVal+Y) < 10 or (self.YVal+Y) > 450:
            print("Out Of Range Y")
            if (self.XVal+X) < 10 or (self.XVal+X) > 800:
               print("Out Of Range X")
            else:
                self.XVal += X
                CommandToSend = f"G91X{X}F2000"
                self.SendCommandToCnc(CommandToSend)
        else:
            self.XVal += X
            self.YVal += Y
            CommandToSend = f"G91X{X}Y{Y}F2000"
            self.SendCommandToCnc(CommandToSend)

    def CncHome(self):
        print("CNC Homing")
        self.SendCommandToCnc("$X")
        self.PenRaise()
        self.SendCommandToCnc("$H")
        self.XVal = 0
        self.YVal = 0
        print("Homing Finished")

    def DrawBoard(self):
        self.SendGCode('/home/aa/graduation project/CNCProject/Utils/boardV2.g')

    def AbsoluteMove(self,X,Y):
        self.SendCommandToCnc('G90')
        self.XVal=X
        self.YVal=Y
        command=f"G1X{X}Y{Y}"
        self.SendCommandToCnc(command)

    def DrawCircle(self,X,Y):
        self.PenRaise()
        self.AbsoluteMove(X, Y)
        self.PenDown()
        self.SendGCode('/home/aa/graduation project/CNCProject/Utils/C.gcode')


    def DrawX(self, X, Y):
        self.PenRaise()
        self.AbsoluteMove(X, Y)
        self.PenDown()
        self.SendGCode('/home/aa/graduation project/CNCProject/Utils/draw_x.g')


    def SendGCode(self, filename):
            with open(filename) as f:
                while (True):
                    line = f.readline().strip('\n')
                    if not line:
                        break

                    if line[0] == ';':
                        # Comments start with semicolon
                        continue

                    self.SendCommandToCnc(line)

    def PenRaise(self):
        if self.Pen:
            self.Pen=False
            self.SendCommandToCnc("M3S90")

    def PenDown(self):
        if not self.Pen:
            self.Pen = True 
            self.SendCommandToCnc("M5")

    def TogglePen(self):
        self.Pen =not self.Pen
        
    def Disconnect(self):
        self.PenRaise()
        self.CncHome()
        self.BlueToothSerial.close()