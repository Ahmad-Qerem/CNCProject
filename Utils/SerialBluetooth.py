
import os
from time import sleep
import serial

class Bluetooth:
    def __init__(self):
        self.XVal = 0
        self.YVal = 0
        self.Pen=False
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
        sleep(0.2)
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
                CommandToSend = f"G91 X{0} Y{Y} F200"
                self.SendCommandToCnc(CommandToSend)
        elif (self.YVal+Y) < 10 or (self.YVal+Y) > 450:
            print("Out Of Range Y")
            if (self.XVal+X) < 10 or (self.XVal+X) > 800:
               print("Out Of Range X")
            else:
                self.XVal += X
                CommandToSend = f"G91 X{X} Y{0} F200"
                self.SendCommandToCnc(CommandToSend)
        else:
            self.XVal += X
            self.YVal += Y
            CommandToSend = f"G91 X{X} Y{Y} F200"
            self.SendCommandToCnc(CommandToSend)

    def CncHome(self):
        print("CNC Homing")
        self.SendCommandToCnc("$X")
        self.SendCommandToCnc("$H")
        self.SendCommandToCnc("G92 X0 Y0")
        self.XVal = 0
        self.YVal = 0
        print("Homing Finished")

    def DrawBoard(self):
        self.SendGCode('board.g')
        

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
            self.Pen=True
            self.SendCommandToCnc("M5")

    def PenDown(self):
        if not self.Pen:
            self.SendCommandToCnc("M3 S45")

    def Disconnect(self):
        self.PenRaise()
        self.CncHome()
        self.BlueToothSerial.close()