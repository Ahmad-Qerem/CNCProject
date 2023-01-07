from Utils.Recognizer import Recognizer
from Utils.SerialBluetooth import Bluetooth
from Modes.Mode1 import Mode1
from Modes.Mode2 import Mode2

class CncController:
    
    def __init__(self):
        self.Mode1STR = ["mode 1", "mode one", "mod one",
                      "mod 1", "mod1", "mud1", "mud 1", "hello"]
        self.Mode2STR = ["mode 2", "mode two", "mod two",
                      "mod 2", "mod2", "mud2", "mud 2", "hi"]
        self.BluetoothSerial = Bluetooth()
        self.recognizer = Recognizer()
        self.recognizer.StartListen(self.callBack)
        print("New CncController Object Has been created ")
        
    def callBack(self, recognizer, audio):
        print("callBack CncController")
        try:
            word = recognizer.recognize_google(audio, key=None, language='en-US')
            print(word)
            if (word in self.Mode1STR):
                print("before mode 1 ")
                GyroMode = Mode1(self.BluetoothSerial)
                GyroMode.GyroscopeToCnc()
                print("after mode 1 ")
                #del GyroMode
                #self.recognizer.StartListen(self.callBack)
            elif (word in self.Mode2STR):
                XOMode = Mode2(self.BluetoothSerial)
            elif word == "exit":
                self.recognizer.StopListen()
                self.BluetoothSerial.Disconnect()
                exit(0)
            else:
                print("Something ...")

            print("finish ")
        except LookupError:
            print("Could not understand audio")
        except IndexError:
            print("no internet connection")
        except Exception as e:
            print("error in callback ")
            print("Error"+str(e))