
import os
from time import sleep
import serial

class Bluetooth:
    def __init__(self):
        self.XVal = 0
        self.YVal = 0
        self.Pen=True
        self.BlueToothSerial=None
        self.BoardPositions = [(150, 70), (110,70),
                               (70,70), (150, 110), (110, 110), (70, 110), (150, 150), (110, 150), (70, 150)]
        self.ConnectBlueTooth()
        print("New Bluetooth Object Has been created ")


    def DrawMove(self,Player='O',I=0,J=0):
        index =(I) * 3 + (J)
        print("This is I" + str(I))
        print("This is J" + str(J))
        print("This is Index"+ str(index))
        Offset=20
        X, Y = self.BoardPositions[index]
        X2, Y2 = X+Offset, Y+Offset
        if Player == 'O':
            self.AbsoluteMove(X2,Y2)
            self.SendGCode(
                '/home/aa/graduation project/CNCProject/Utils/draw_o.g')
        else :
            self.AbsoluteMove(X+10, Y+10)
            self.SendGCode(
                '/home/aa/graduation project/CNCProject/Utils/draw_x.g')
            
        sleep(1)    
        self.AbsoluteMove(40,40)
        
    def DrawWinLine(self,GroupIndex):

        if GroupIndex == 0:
            i = 0 
            j = 2
        elif GroupIndex == 1:
            i = 3
            j = 5
        elif GroupIndex == 2:
            i = 6
            j = 8
        elif GroupIndex == 3:
            i = 0
            j = 6
        elif GroupIndex == 4:
            i = 1
            j = 7
        elif GroupIndex == 5:
            i = 2
            j = 8
        elif GroupIndex == 6:
            i = 0
            j = 8
        elif GroupIndex == 7:
            i = 2
            j = 6


        X1, Y1 = self.BoardPositions[i]
        X2, Y2 = self.BoardPositions[j]
        self.PenRaise()
        self.AbsoluteMove(X1+20,Y1+20)
        self.PenDown()
        command = f'G1 X{X2+20} Y{Y2+20} F2000'
        self.SendCommandToCnc(command)
        self.PenRaise()
        self.AbsoluteMove(40,40)

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
        sleep(0.3)
        GRBLOut = self.BlueToothSerial.readline()
        print(GRBLOut.strip().decode("utf-8"))

    def SendList(self,List):
        for command in List:
            self.SendCommandToCnc(command)
            sleep(0.3)
        

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
        self.PenRaise()
        self.SendCommandToCnc("$H")
        self.XVal = 0
        self.YVal = 0
        print("Homing Finished")

    def DrawBoard(self):
        self.SendGCode('/home/aa/graduation project/CNCProject/Utils/boardV2.g')

    def DrawLetter(self,url):
        self.SendCommandToCnc("$X")
        self.PenDown()
        self.SendCommandToCnc("G1F4000")
        self.SendGCode(url)
        self.PenRaise()

    def AbsoluteMove(self,X,Y):
        self.XVal=X
        self.YVal=Y
        command=f"G0X{X}Y{Y}"
        self.SendCommandToCnc(command)


    def DrawX(self, X, Y):
        self.PenRaise()
        self.AbsoluteMove(X, Y)
        self.PenDown()
        self.SendGCode('/home/aa/graduation project/CNCProject/Utils/draw_x.g')


    def SendGCode(self, filename):
            with open(filename) as f:
                while (True):
                    sleep(1)
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