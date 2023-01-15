from math import inf
from time import sleep
import sys
from random import choice
sys.path.append('/home/aa/graduation project/CNCProject/Utils')
from Utils.Recognizer import Recognizer

one = ['one', '1', 'won', 'Wayne']
two = ['tool', 'two', 'too', 'Tool', '2',]
three = ['three', '3', 'free', 'III']
four = ['four', '4', 'for', '']
five = ['five', '5', 'life', 'fight', 'Fife',]
six = ['six', '6', 'sex']
seven = ['seven', '7', 'oven', 'surgeon', 'Susan', 'season', 'session']
eight = ['eight', '8', 'it']
nine = ['nine', '9', '9:00', 'Line']


class Mode2:
    def __init__(self, BluetoothSerial):
        self.BS = BluetoothSerial
        self.recognizer = Recognizer()
        self.Word = ""
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.FlagEndGame = False
        self.Done = False
        self.Index = 4
        self.Row = 2
        self.Col = 2

        print("New Mode2 Object Has been created ")

    def callBack(self, recognizer, audio):
        print("callBack Mode2")
        try:

            word = recognizer.recognize_google(
                audio, key=None, language='en-US')
            word = word.split(' ')[1]

            print("THE WORD IS : "+word)
            if word in one:
                self.Index = 1
                self.Done = True
            elif word in two:
                self.Index = 2
                self.Done = True
            elif word in three:
                self.Index = 3
                self.Done = True
            elif word in four:
                self.Index = 4
                self.Done = True
            elif word in five:
                self.Index = 5
                self.Done = True
            elif word in six:
                self.Index = 6
                self.Done = True
            elif word in seven:
                self.Index = 7
                self.Done = True
            elif word in eight:
                self.Index = 8
                self.Done = True
            elif word in nine:
                self.Index = 9
                self.Done = True
            elif word == "disconnect":
                self.FlagEndGame = True
                recognizer.StopListen()
            else:
                print(" Something ... Mode 2")

        except Exception as e:
            print("error in callback mode 2")
            print("Error"+str(e))
    
    def Gameboard(self, board):
        chars = {1: 'X', -1: 'O', 0: ' '}
        for i in range(1,4):
            for j in range(1,4):
                ch = chars[board[i-1][j-1]]
                if (ch==' '):
                    ch = ((i-1) * 3 + (j-1))+1
                print(f'| {ch} |', end='')
            print('\n' + '---------------')
        print('===============')

    def Clearboard(self, board):
        for x, row in enumerate(board):
            for y, col in enumerate(row):
                board[x][y] = 0

    def winningPlayer(self, board, player):
        conditions = [[board[0][0], board[0][1], board[0][2]],
                      [board[1][0], board[1][1], board[1][2]],
                      [board[2][0], board[2][1], board[2][2]],
                      [board[0][0], board[1][0], board[2][0]],
                      [board[0][1], board[1][1], board[2][1]],
                      [board[0][2], board[1][2], board[2][2]],
                      [board[0][0], board[1][1], board[2][2]],
                      [board[0][2], board[1][1], board[2][0]]]

        if [player, player, player] in conditions:
            return True

        return False

    def gameWon(self, board):
        return self.winningPlayer(board, 1) or self.winningPlayer(board, -1)

    def printResult(self, board):
        if self.winningPlayer(board, 1):
            print('X has won! ' + '\n')

        elif self.winningPlayer(board, -1):
            print('O\'s have won! ' + '\n')

        else:
            print('Draw' + '\n')

    def blanks(self, board):
        blank = []
        for x, row in enumerate(board):
            for y, col in enumerate(row):
                if board[x][y] == 0:
                    blank.append([x, y])

        return blank

    def boardFull(self, board):
        if len(self.blanks(board)) == 0:
            return True
        return False

    def setMove(self, board, x, y, player):
        board[x][y] = player

    def playerMove(self, board):
        e = True
        moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
                 4: [1, 0], 5: [1, 1], 6: [1, 2],
                 7: [2, 0], 8: [2, 1], 9: [2, 2]}
        while e:
            try:
                # move = int(input('Enter a number between 1-9: '))
                print('Enter a number between 1-9: ')
                while not self.Done:
                    sleep(0.5)
                self.Done = False
                move = self.Index
                if move < 1 or move > 9:
                    print('Invalid Move! Try again!')
                elif not (moves[move] in self.blanks(board)):
                    print('Invalid Move! Try again!')
                else:
                    self.setMove(board, moves[move][0], moves[move][1], 1)
                    self.BS.DrawMove('X', moves[move][0], moves[move][1])

                    self.Gameboard(board)
                    e = False
            except (KeyError, ValueError):
                print('Enter a number!')

    def getScore(self, board):
        if self.winningPlayer(board, 1):
            return 10

        elif self.winningPlayer(board, -1):
            return -10

        else:
            return 0

    def abminimax(self, board, depth, alpha, beta, player):
        row = -1
        col = -1
        if depth == 0 or self.gameWon(board):
            return [row, col, self.getScore(board)]

        else:
            for cell in self.blanks(board):
                self.setMove(board, cell[0], cell[1], player)
                score = self.abminimax(board, depth - 1, alpha, beta, -player)
                if player == 1:
                    # X is always the max player
                    if score[2] > alpha:
                        alpha = score[2]
                        row = cell[0]
                        col = cell[1]

                else:
                    if score[2] < beta:
                        beta = score[2]
                        row = cell[0]
                        col = cell[1]

                self.setMove(board, cell[0], cell[1], 0)

                if alpha >= beta:
                    break

            if player == 1:
                return [row, col, alpha]

            else:
                return [row, col, beta]

    def o_comp(self, board):
        if len(self.blanks(board)) == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
            self.setMove(board, x, y, -1)
            self.BS.DrawMove('O', x, y)

            self.Gameboard(board)

        else:
            result = self.abminimax(
                board, len(self.blanks(board)), -inf, inf, -1)
            self.setMove(board, result[0], result[1], -1)
            self.BS.DrawMove('O', result[0], result[1])
            self.Gameboard(board)

    def x_comp(self, board):
        if len(self.blanks(board)) == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
            self.setMove(board, x, y, 1)
            self.BS.DrawMove('X', result[0], result[1])

            self.Gameboard(board)

        else:
            result = self.abminimax(board, len(
                self.blanks(board)), -inf, inf, 1)
            self.setMove(board, result[0], result[1], 1)
            self.BS.DrawMove('X', result[0], result[1])

            self.Gameboard(board)

    def makeMove(self, board, player, mode):
        if mode == 1:
            if player == 1:
                self.playerMove(board)

            else:
                self.o_comp(board)
        else:
            if player == 1:
                self.o_comp(board)
            else:
                self.x_comp(board)

    def pvc(self):
        order = choice([1, 2])
        board = self.board
        self.Clearboard(board)

        if order == 2:
            currentPlayer = -1
        else:
            currentPlayer = 1
        self.BS.CncHome()
        self.BS.DrawBoard()
        self.BS.AbsoluteMove(40,40)
        self.recognizer.StartListen(self.callBack)
        while not (self.boardFull(self.board) or self. gameWon(self.board) or self.FlagEndGame):
            self.makeMove(self.board, currentPlayer, 1)
            currentPlayer *= -1

        self.printResult(self.board)
        self.recognizer.StopListen()





