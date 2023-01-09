
import speech_recognition as sr


class Recognizer:
    def __init__(self):
        self.recognizer=None
        self.mic = None
        self.ThreadListenInBackGround = None
        self.ConnectRecognizer()
        print("New Recognizer Object Has been created ")


    def ConnectRecognizer(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=1)
        # Remove noise from the background
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Recognizer Is Ready To Listen ")

    def StartListen(self, callBack):
        self.ThreadListenInBackGround = self.recognizer.listen_in_background(
            source=self.mic, callback=callBack)

    def StopListen(self):
        self.ThreadListenInBackGround()
