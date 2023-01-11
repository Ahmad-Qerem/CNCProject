from keras.models import load_model
import numpy as np
import cv2
import os
import sys
from Modes.TicTacToe.alphabeta import Tic,get_enemy,determine
from Modes.TicTacToe.utils import detections
from Modes.TicTacToe.utils import imutils
sys.path.append('/home/aa/graduation project/CNCProject/Utils')
from Utils.Recognizer import Recognizer

class Mode2:

    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Word=""
        self.FlagEndGame=False
        self.FlagTurn=False
        print("New Mode2 Object Has been created ")

    def callBack(self, recognizer, audio):
        print("callBack Mode2")
        try:
            self.word = recognizer.recognize_google(
                audio_data=audio, key=None, language='en-US')
            if self.word == "your turn":
                self.FlagTurn=True
            elif self.word == "disconnect":
                self.FlagEndGame=True
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


    def find_sheet_paper(frame, thresh, add_margin=True):
            """Detect the coords of the sheet of paper the game will be played on"""
            stats = detections.find_corners(thresh)
            # First point is center of coordinate system, so ignore it
            # We only want sheet of paper's corners
            corners = stats[1:, :2]
            corners = imutils.order_points(corners)
            # Get bird view of sheet of paper
            paper = imutils.four_point_transform(frame, corners)
            if add_margin:
                paper = paper[10:-10, 10:-10]
            return paper, corners


    def find_shape(cell):
        """Is shape and X or an O?"""
        mapper = {0: None, 1: 'X', 2: 'O'}
        cell = detections.preprocess_input(cell)
        idx = np.argmax(model.predict(cell))
        return mapper[idx]


    def get_board_template(thresh):
        """Returns 3 x 3 grid, a.k.a the board"""
        # Find grid's center cell, and based on it fetch
        # the other eight cells
        middle_center = detections.contoured_bbox(thresh)
        center_x, center_y, width, height = middle_center

        # Useful coords
        left = center_x - width
        right = center_x + width
        top = center_y - height
        bottom = center_y + height

        # Middle row
        middle_left = (left, center_y, width, height)
        middle_right = (right, center_y, width, height)
        # Top row
        top_left = (left, top, width, height)
        top_center = (center_x, top, width, height)
        top_right = (right, top, width, height)
        # Bottom row
        bottom_left = (left, bottom, width, height)
        bottom_center = (center_x, bottom, width, height)
        bottom_right = (right, bottom, width, height)

        # Grid's coordinates
        return [top_left, top_center, top_right,
                middle_left, middle_center, middle_right,
                bottom_left, bottom_center, bottom_right]


    def draw_shape(self,template, shape, coords):
        """Draw on a cell the shape which resides in it"""
        x, y, w, h = coords
        print('X = {} , Y = {} , width = {} , Hight = {}', x, y, w, h)
        if shape == 'O':
            centroid = (x + int(w / 2), y + int(h / 2))
            # self.BS.DrawCircle(x,y)
            cv2.circle(template, centroid, 10, (0, 0, 0), 2)
        elif shape == 'X':
            # Draws the 'X' shape
            cv2.line(template, (x + 10, y + 7), (x + w - 10, y + h - 7),
                    (0, 0, 0), 2)
            cv2.line(template, (x + 10, y + h - 7), (x + w - 10, y + 7),
                    (0, 0, 0), 2)
            #self.BS.DrawX(x, y)
        return template


    def play(self,vcap):
        """Play tic tac toe game with computer that uses the alphabeta algorithm"""
        # Initialize opponent (computer)
        board = Tic()
        history = {}
        message = True
        # Draw Board
        # self.BS.CncHome()
        # self.BS.DrawBoard()
        self.recognizer.StartListen(self.callBack)

        # Start playing
        while True:
            ret, frame = vcap.read()
            key = cv2.waitKey(1) & 0xFF
            if not ret:
                print('[INFO] finished video processing')
                break

            # Stop
            if key == ord('q') or self.FlagEndGame:
                print('[INFO] stopped video processing')
                break

            # Preprocess input
            # frame = imutils.resize(frame, 500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
            thresh = cv2.GaussianBlur(thresh, (7, 7), 0)
            paper, corners = self.find_sheet_paper(frame, thresh)
            # Four red dots must appear on each corner of the sheet of paper,
            # otherwise try moving it until they're well detected
            for c in corners:
                point = (int(c[0]), int(c[1]))
                cv2.circle(img=frame, center=point, radius=2,
                        color=(0, 0, 255), thickness=2)
            # Now working with 'paper' to find grid
            paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
            _, paper_thresh = cv2.threshold(
                paper_gray, 170, 255, cv2.THRESH_BINARY_INV)
            grid = self.get_board_template(paper_thresh)

            # Draw grid and wait until user makes a move
            for i, (x, y, w, h) in enumerate(grid):
                cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 0, 0), 2)
                if history.get(i) is not None:
                    shape = history[i]['shape']
                    paper = self.draw_shape(paper, shape, (x, y, w, h))

            # Make move
            if message:
                print('Make move, then press spacebar')
                message = False
            #if not key == 32 or not self.FlagTurn:
            if not key == 32:
                cv2.imshow('original', frame)
                cv2.imshow('bird view', paper)
                continue
            player = 'X'

            # User's time to play, detect for each available cell
            # where has he played
            available_moves = np.delete(np.arange(9), list(history.keys()))
            for i, (x, y, w, h) in enumerate(grid):
                if i not in available_moves:
                    continue
                # Find what is inside each free cell
                cell = paper_thresh[int(y): int(y + h), int(x): int(x + w)]
                shape = self.find_shape(cell)
                if shape is not None:
                    history[i] = {'shape': shape, 'bbox': (x, y, w, h)}
                    board.make_move(i, player)
                else:
                    ######################## drow nums 
                    pass    
                paper = self.draw_shape(paper, shape, (x, y, w, h))

            # Check whether game has finished
            if board.complete():
                break

            # Computer's time to play
            player = get_enemy(player)
            computer_move = determine(board, player)
            board.make_move(computer_move, player)
            history[computer_move] = {'shape': 'O', 'bbox': grid[computer_move]}
            paper = self.draw_shape(paper, 'O', grid[computer_move])

            # Check whether game has finished
            if board.complete():
                break

            # Show images
            cv2.imshow('original', frame)
            # cv2.imshow('thresh', paper_thresh)
            cv2.imshow('bird view', paper)
            message = True

        # Show winner
        winner = board.winner()
        height = paper.shape[0]
        text = 'Winner is {}'.format(str(winner))
        cv2.putText(paper, text, (10, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow('bird view', paper)
        cv2.waitKey(0) & 0xFF

        # Close windows
        vcap.release()
        cv2.destroyAllWindows()
        return board.winner()


    def RunGame(self,path):
        global model
        assert os.path.exists("/home/aa/graduation project/CNCProject/Modes/TicTacToe/data/model.h5"), '{} does not exist'
        model = load_model("/home/aa/graduation project/CNCProject/Modes/TicTacToe/data/model.h5")
        vcap = cv2.VideoCapture(path)
        winner = self.play(vcap)
        print('Winner is:', winner)