from CncController import CncController
from time import sleep

def main():
     NewControllerModule = CncController()
     while True:
        sleep(0.1)
  
if __name__ == "__main__":
    main()