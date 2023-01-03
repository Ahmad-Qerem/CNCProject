import Recognizer
import sys
sys.path.append('../Utils')


class Mode2:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.StartPlay()

    def callBack(self, recognizer, audio):
        try:
            word = recognizer.recognize_google(
                audio, key=None, language='en-US')
            if word == "start":
                self.BS.PenDown()
            elif word == "stop":
                self.BS.PenRaise()
            elif word == "home":
                self.BS.PenRaise()
                self.BS.CncHome()
            elif word == "disconnect":
                self.recognizer.StopListen()
            else:
                print(" Something ... Mode 2")

        except LookupError:
            print("Could not understand audio")
        except IndexError:
            print("no internet connection")
        except Exception as e:
            print("error in callback ")
            print("Error"+str(e))

  
    def StartPlay():
        pass