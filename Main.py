# from CncController import CncController
from time import sleep
from TicTacToe import play

# Main program start here


def main():
    # NewControllerModule = CncController()
    # NewControllerModule.StartListen()
    # while True:
    #    sleep(0.1)
    play.RunGame("http://192.168.1.6:8080/video")


if __name__ == "__main__":
    main()
