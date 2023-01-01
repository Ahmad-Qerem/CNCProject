# from CncController import CncController
from time import sleep
from TicTacToe import play

# Main program start here


def main():
    # NewControllerModule = CncController()
    # NewControllerModule.StartListen()
    # while True:
    #    sleep(0.1)
    # play.RunGame("http://192.168.1.6:8080/video")
    while(True):
        try :
            play.RunGame("http://192.168.1.9:8080/video")
            #play.RunGame(0)
        except Exception as e :
            print("Error : "+ str(e))
            sleep(1)
        
if __name__ == "__main__":
    main()
