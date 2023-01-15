from time import sleep
from Utils.Recognizer import Recognizer
from Utils.SerialBluetooth import Bluetooth
from Modes.Mode1 import Mode1
from Modes.Mode2 import Mode2
from Modes.Mode3 import Mode3

Mode1STR = ["mode 1", "mode one", "mod one",
            "mod 1", "mod1", "mud1", "mud 1","mud run",
            "Baldwin", "mullet one", "Northland", "Multan",
            "1", "one", "Note 1", "Note one", "smart one",
            "smart 1", "smart1", "hello"]

Mode2STR = ["mode 2", "mode two", "mod two",
            "mod 2", "mod2", "mud2", "mud 2", "hi"]

Mode3STR = ["mode 3", "mode three", "mod three",
            "mod 3", "mod3", "mud3", "mud 3"]

BluetoothSerial = Bluetooth()

def callBack(recognizer, audio):
    print("callBack Main")
    try:
        word = recognizer.recognize_google(
            audio, key=None, language='en-US')
        print(word)
        if (word in Mode1STR):
            GyroMode = Mode1(BluetoothSerial)
            GyroMode.GyroscopeToCnc()
            del GyroMode
            recognizer.StartListen(callBack)
        elif (word in Mode2STR):
            XOMode = Mode2(BluetoothSerial)
            XOMode.start()
            del XOMode
        elif (word in Mode3STR):
            WriteMode = Mode3(BluetoothSerial)
            WriteMode.ActiveMode3(BluetoothSerial)
            del WriteMode
        elif word == "exit":
            BluetoothSerial.Disconnect()
            recognizer.StopListen()
            exit(0)
        else:
            print("Something ...")

    except Exception as e:
        print("error in callback ")
        print("Error"+str(e))


def main():
    recognizer = Recognizer()
    recognizer.StartListen(callBack)
    while True:
        sleep(0.5)
  
if __name__ == "__main__":
    main()