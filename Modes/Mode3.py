
from Utils.Recognizer import Recognizer

class Mode3:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Word = ""
        print("New Mode3 Object Has been created ")

    def callBack(self, recognizer, audio):
        print("callBack Mode3")
        try:
            word = recognizer.recognize_google(audio_data=audio, key=None, language='en-US')
            if self.word == "your turn":
                pass
            elif self.word == "disconnect":
                pass
                self.recognizer.StopListen()
            else:
                print(" Something ... Mode 2")

        except IndexError:
            print("no internet connection")
        except LookupError:
            print("Could not understand audio")
        except Exception as e:
            print("error in callback mode 2")
            print("Error"+str(e))
