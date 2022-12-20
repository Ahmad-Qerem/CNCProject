from CncController import CncController
from time import sleep
# Main program start here


def main():
    NewControllerModule = CncController()
    NewControllerModule.StartListen()
    while True:
        sleep(0.1)


if __name__ == "__main__":
    main()
