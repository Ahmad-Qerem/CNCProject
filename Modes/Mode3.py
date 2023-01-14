
from Utils.Recognizer import Recognizer
from ttgLib.TextToGcode import ttg

class Mode3:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        print("New Mode3 Object Has been created ")

    def callBack(self, recognizer, audio):
        print("callBack Mode3")
        try:
            word = recognizer.recognize_google(audio_data=audio, key=None, language='en-US')
            Data = ttg(word, 1, 0, "visualize", 6000).toGcode("M5", "M3S90", "G0", "G1")
            print(Data)
            self.BS.SendList(Data)
            if self.word == "disconnect":
                self.recognizer.StopListen()
            else:
                print(" Something ... Mode 3")

        except IndexError:
            print("no internet connection")
        except LookupError:
            print("Could not understand audio")
        except Exception as e:
            print("error in callback mode 2")
            print("Error"+str(e))

    def ActiveMode3(self):
        self.recognizer.StartListen()

        