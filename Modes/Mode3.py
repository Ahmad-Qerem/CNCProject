from Utils.Recognizer import Recognizer
from ttgLib.TextToGcode import ttg
from time import sleep
class Mode3:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Flag = False
        print("New Mode3 Object Has been created ")

    def callBack(self, recognizer, audio):
        print("callBack Mode3")
        try:
            word = recognizer.recognize_google(audio_data=audio, key=None, language='en-US')
            print("this is type of word : "+word)
            if self.word == "disconnect":
                self.Flag = True
                self.recognizer.StopListen()

            elif isinstance(word,str):
                Data = ttg(word, 5, 0, "return", 6000).toGcode(
                    "M5", "M3S90", "G0", "G1")
                print(Data)
                self.BS.SendList(Data)
                print(" Something ... Mode 3")

        except Exception as e:
            print("error in callback mode 3")
            print("Error"+str(e))

    def ActiveMode3(self):
        self.recognizer.StartListen(self.callBack)
        while True:
            if self.Flag:
                break
            sleep(1)
        
