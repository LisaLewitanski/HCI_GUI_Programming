from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QTimer, QTime
from PyQt5.QtGui import QPainter, QColor, QImage
from PyQt5.QtWidgets import *

# from piece import Piece
import time
from ai import AI

WHITE_PIECE = "./icons/white_piece.png"
BLACK_PIECE = "./icons/black_piece2.png"
WHITE_KING = "./icons/white_king.png"
BLACK_KING = "./icons/black_king.png"
WHITE_SQUARE = "./icons/white_square.png"
BLACK_SQUARE = "./icons/black_square.png"
FPLAYER = "Waiting first player to play"
SPLAYER = "Waiting second player to play"
AIPLAYER = "Waiting AI player to play"
ENDGAME = "The game is over"


class Board(QFrame):
    """
    Everything to handle the game: Drawing pieces and the board, Handling the mouse and the game logic
    """
    msg2Statusbar = pyqtSignal(str)

    # todo set the board with and height in square
    boardWidth = 8
    boardHeight = 8
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.init()

    def init(self):
        """
        Initialise all values

        :return:
        """
        self.boardArray = [[0, 3, 0, 3, 0, 3, 0, 3],
                           [3, 0, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 3, 0, 3, 0, 3],
                           [1, 0, 1, 0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1],
                           [2, 0, 2, 0, 2, 0, 2, 0],
                           [0, 2, 0, 2, 0, 2, 0, 2],
                           [2, 0, 2, 0, 2, 0, 2, 0]]
        # Timer initialization

        self.timer = QTimer()
        self.time = QTime(0, 0, 0)
        self.timer.timeout.connect(self.timerEventGame)

        self.timerPlayer = QTimer()
        self.timePlayer = QTime(0, 1, 0)
        self.timer.timeout.connect(self.timerEventPlayer)

        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        # image de la piece de base m'voyez
        self.image = QImage(WHITE_PIECE)
        # self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.reset_game()
        self.selected_piece = [-1, -1]
        self.player_turn = 1
        # nombre de piece = [nb de piece joueur 1, nb de piece jour 2]
        self.playersRemaining = [12, 12]
        # nombre de jump = [nb de jump joueur 1, nb de jump jour 2]
        self.playersJumps = [0, 0]
        self.scoreBoard = None
        self.status = FPLAYER
        # si le temps du joueur a timeout
        self.timePassed = False
        self.startTime = 0
        self.interval = 0
        # pour changer l'affichage si on jou contre une AI
        self.isAI = False
        self.winner = -1
        self.aiDifficulties = 2

    def timerEventGame(self):
        """
        This function allows to update the game timer and update the scoreBoard.

        :return: Nothing
        """
        # Update the game timer
        self.time = self.time.addSecs(1)
        # Update de UI of the scoreBoard
        self.scoreBoard.updateUI()

    def initPlayerTimer(self):
        """
        Init the player timer when the player begin his turn.

        :return: Nothing
        """
        self.timerPlayer = QTimer()
        self.timePlayer = QTime(0, 1, 0)

    def startTimerInter(self, interval):
        """
        Start the player timer with an given interval.

        :param interval: The interval from which time must resume
        :return: Nothing
        """
        self.timerPlayer.start(interval)

    def startTimerPlayer(self):
        """"
        Function to start a player timer with an interval of 1000.
        """
        self.interval = 1000
        self.startTime = time.time()
        self.timerPlayer.start(1000)

    def timerEventPlayer(self):
        """
        This function allows to update the timer of the player one.

        :return: Nothing
        """
        self.timePlayer = self.timePlayer.addSecs(-1)
        if self.timerPlayer.isActive():
            if self.timePlayer.minute() * 60 + self.timePlayer.second() < 1:
                self.timePassed = True
                self.timerPassedEndGame()
        self.scoreBoard.updateUI()

    def setScoreBoard(self, scoreBoard):
        """
        This function allows to get the scoreBoard class to use it later in the code.

        :param scoreBoard: The class scoreBoard
        :return: Nothing
        """
        self.scoreBoard = scoreBoard

    def print_board_array(self):
        """
        Prints the boardArray in an attractive way

        :return: Nothing
        """

        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mouse_pos_to_col_row(self, event):
        """
        Convert the mouse click event to a row and column.

        :param event: The click event
        :return: The click's position with the following format: [x, y] (Example: [3, 4])
        """

        return [int(event.x() / self.square_width()), int(event.y() / self.square_height())]

    def square_width(self):
        """
        This function allows to return the width of one square in the board.

        :return: The width of one square in the board.
        """
        return self.contentsRect().width() / Board.boardWidth

    def square_height(self):
        """
        This function allows to return the height of one square in the board.

        :return: The height of one square in the board
        """

        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        """starts game"""
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.reset_game()
        self.timer.start(1000)
        self.startTimerPlayer()
        # self.timerPlayer.start(1000)

    def pause(self):
        """pauses game"""

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timerPlayer.stop()
            self.timer.stop()
            self.status = "Game paused"
            elapsedTime = self.startTime - time.time()
            self.startTime -= elapsedTime
            self.interval -= int(elapsedTime * 1000)

        else:
            self.timer.start()
            self.startTimerInter(self.interval)
            if self.player_turn == 1:
                self.status = FPLAYER
            elif self.isAI:
                self.status = AIPLAYER
            else:
                self.status = SPLAYER
            self.scoreBoard.updateUI()

        self.update()

    def paintEvent(self, event):
        """paints the board and the pieces of the game"""
        painter = QPainter(self)
        self.draw_board_squares(painter)
        self.draw_pieces(painter)

    def new_place(self, turn, row, col, change):
        """
        Change the piece place

        :param turn:
        :param row:
        :param col:
        :param change:
        :return:
        """
        self.boardArray[row][col] = self.boardArray[self.selected_piece[1]][self.selected_piece[0]]
        if (row == 0 and self.boardArray[row][col] == 2) or (row == 7 and self.boardArray[row][col] == 3):
            self.boardArray[row][col] += 2
        self.boardArray[self.selected_piece[1]][self.selected_piece[0]] = 1
        if change == 1:
            self.selected_piece = [-1, -1]
        else:
            self.selected_piece = [col, row]
        self.player_turn = turn
        self.scoreBoard.updateUI()

    def first_player_take(self, row, col):
        """
        Take a piece for the first player

        :param row:
        :param col:
        :return:
        """
        p = 2
        change = 1
        b = 0
        r = self.selected_piece[1]
        c = self.selected_piece[0]
        if self.boardArray[r][c] == 2 and r > 1 and c > 1 and self.boardArray[r - 2][c - 2] == 1 and \
                        self.boardArray[r - 1][c - 1] == 3:
            b = 1
        elif self.boardArray[r][c] == 2 and r > 1 and c < 6 and self.boardArray[r - 2][c + 2] == 1 and \
                        self.boardArray[r - 1][c + 1] == 3:
            b = 1
        if b == 0 and self.player_turn == 1 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] - 1 \
                and (col == self.selected_piece[0] + 1 or col == self.selected_piece[0] - 1):
            self.new_place(2, row, col, change)
        elif self.player_turn == 1 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] - 2 \
                and col == self.selected_piece[0] + 2 and self.boardArray[row + 1][col - 1] == 3:
            self.boardArray[row + 1][col - 1] = 1
            self.playersRemaining[1] -= 1
            if self.playersRemaining[1] == 0:
                self.timePassed = True
                self.player_turn = 2
                self.timerPassedEndGame()
            self.playersJumps[0] += 1
            if row > 1 and col > 1 and self.boardArray[row - 2][col - 2] == 1 and self.boardArray[row - 1][col - 1] == 3:
                p = 1
                change = 0
            elif row > 1 and col < 6 and self.boardArray[row - 2][col + 2] == 1 and self.boardArray[row - 1][col + 1] == 3:
                p = 1
                change = 0
            self.new_place(p, row, col, change)
        elif self.player_turn == 1 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] - 2 \
                and col == self.selected_piece[0] - 2 and self.boardArray[row + 1][col + 1] == 3:
            self.boardArray[row + 1][col + 1] = 1
            self.playersRemaining[1] -= 1
            if self.playersRemaining[1] == 0:
                self.timePassed = True
                self.player_turn = 2
                self.timerPassedEndGame()
            self.playersJumps[0] += 1
            if row > 1 and col > 1 and self.boardArray[row - 2][col - 2] == 1 and self.boardArray[row - 1][col - 1] == 3:
                p = 1
                change = 0
            elif row > 1 and col < 6 and self.boardArray[row - 2][col + 2] == 1 and self.boardArray[row - 1][col + 1] == 3:
                p = 1
                change = 0
            self.new_place(p, row, col, change)

    def second_player_take(self, row, col):
        """
        Take a piece for the second player

        :param row:
        :param col:
        :return:
        """
        p = 1
        change = 1
        b = 0
        r = self.selected_piece[1]
        c = self.selected_piece[0]
        if self.boardArray[r][c] == 3 and r < 6 and c > 1 and self.boardArray[r + 2][c - 2] == 1 and \
                        self.boardArray[r + 1][c - 1] == 2:
            b = 1
        elif self.boardArray[r][c] == 3 and r < 6 and c < 6 and self.boardArray[r + 2][c + 2] == 1 and \
                        self.boardArray[r + 1][c + 1] == 2:
            b = 1
        if b == 0 and self.player_turn == 2 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] + 1 \
                and (col == self.selected_piece[0] + 1 or col == self.selected_piece[0] - 1):
            self.new_place(p, row, col, change)
        elif self.player_turn == 2 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] + 2 \
                and col == self.selected_piece[0] + 2 and self.boardArray[row - 1][col - 1] == 2:
            self.boardArray[row - 1][col - 1] = 1
            self.playersRemaining[0] -= 1
            if self.playersRemaining[0] == 0:
                self.timePassed = True
                self.player_turn = 1
                self.timerPassedEndGame()
            self.playersJumps[1] += 1
            if row < 6 and col > 1 and self.boardArray[row + 2][col - 2] == 1 and self.boardArray[row + 1][col - 1] == 2:
                p = 2
                change = 0
            elif row < 6 and col < 6 and self.boardArray[row + 2][col + 2] == 1 and self.boardArray[row + 1][col + 1] == 2:
                p = 2
                change = 0
            self.new_place(p, row, col, change)
        elif self.player_turn == 2 and self.boardArray[row][col] == 1 and row == self.selected_piece[1] + 2 \
                and col == self.selected_piece[0] - 2 and self.boardArray[row - 1][col + 1] == 2:
            self.boardArray[row - 1][col + 1] = 1
            self.playersRemaining[0] -= 1
            if self.playersRemaining[0] == 0:
                self.timePassed = True
                self.player_turn = 1
                self.timerPassedEndGame()
            self.playersJumps[1] += 1
            if row < 6 and col > 1 and self.boardArray[row + 2][col - 2] == 1 and self.boardArray[row + 1][col - 1] == 2:
                p = 2
                change = 0
            elif row < 6 and col < 6 and self.boardArray[row + 2][col + 2] == 1 and self.boardArray[row + 1][col + 1] == 2:
                p = 2
                change = 0
            self.new_place(p, row, col, change)

    def mousePressEvent(self, event):
        """
        Get the pos clicked and call the game logic
        :param event:
        :return:
        """
        if not self.isPaused:
            clicked = self.mouse_pos_to_col_row(event)
            if clicked:
                self.logicGame(clicked)

    def AI(self):
        """
        Creates the AI class with the array board.
        Then, it get the positions choosed by the AI.
        Finally it call the logic Game to move the piece.

        :return: Nothing
        """

        self.selected_piece = [-1, -1]
        self.ai = AI(self.boardArray)
        positions = self.ai.MinMaxDecision(self.aiDifficulties)
        self.logicGame([positions[0][1], positions[0][0]])
        self.logicGame([positions[1][1], positions[1][0]])

    def timerPassedEndGame(self):
        """
        When a player take a lot of time to play (1 minutes)

        :return: -1 (value for the end of the game)
        """
        self.status = ENDGAME
        self.timerPlayer.stop()
        self.timer.stop()
        if self.player_turn == 1:
            if not self.isAI:
                self.winner = 2
            else:
                self.winner = 3
        else:
            self.winner = 1
        # self.scoreBoard.updateUI()
        # self.init()
        return -1

    def logicGame(self, positions):
        """
        Game logic to manage pieces moves
        :param positions:
        :return:
        """
        row = positions[1]
        col = positions[0]
        if self.timePassed:
            return self.timerPassedEndGame()
        if self.player_turn == 1:
            self.status = FPLAYER
        elif self.isAI:
            self.status = AIPLAYER
        else:
            self.status = SPLAYER

        if self.selected_piece == [-1, -1]:
            if self.player_turn == 1:
                b = 0
                for r in range(0, len(self.boardArray)):
                    for c in range(0, len(self.boardArray[0])):
                        if self.boardArray[r][c] == 2 and r > 1 and c > 1 and self.boardArray[r - 2][c - 2] == 1 and self.boardArray[r - 1][c - 1] == 3:
                            b = 1
                        elif self.boardArray[r][c] == 2 and r > 1 and c < 6 and self.boardArray[r - 2][c + 2] == 1 and self.boardArray[r - 1][c + 1] == 3:
                            b = 1
                if self.boardArray[row][col] == self.player_turn + 1:
                    if (b == 0 and row > 0 and col > 0 and self.boardArray[row - 1][col - 1] == 1) \
                            or (b == 0 and row > 0 and col < 7 and self.boardArray[row - 1][col + 1] == 1):
                        self.selected_piece = positions
                    elif row > 1 and col > 1 and self.boardArray[row - 2][col - 2] == 1 and self.boardArray[row - 1][col - 1] == 3:
                        self.selected_piece = positions
                    elif row > 1 and col < 6 and self.boardArray[row - 2][col + 2] == 1 and self.boardArray[row - 1][col + 1] == 3:
                        self.selected_piece = positions
            elif self.player_turn == 2:
                b = 0
                for r in range(0, len(self.boardArray)):
                    for c in range(0, len(self.boardArray[0])):
                        if self.boardArray[r][c] == 3 and r < 6 and c > 1 and self.boardArray[r + 2][c - 2] == 1 and self.boardArray[r + 1][c - 1] == 2:
                            b = 1
                        elif self.boardArray[r][c] == 3 and r < 6 and c < 6 and self.boardArray[r + 2][c + 2] == 1 and self.boardArray[r + 1][c + 1] == 2:
                            b = 1
                if self.boardArray[row][col] == self.player_turn + 1:
                    if (b == 0 and row < 7 and col > 0 and self.boardArray[row + 1][col - 1] == 1) \
                        or (b == 0 and row < 7 and col < 7 and self.boardArray[row + 1][col + 1] == 1):
                        self.selected_piece = positions
                    elif row < 6 and col > 1 and self.boardArray[row + 2][col - 2] == 1 and self.boardArray[row + 1][col - 1] == 2:
                        self.selected_piece = positions
                    elif row < 6 and col < 6 and self.boardArray[row + 2][col + 2] == 1 and self.boardArray[row + 1][col + 1] == 2:
                        self.selected_piece = positions

        else:
            if self.selected_piece == positions:
                self.selected_piece = [-1,-1]
                return
            self.first_player_take(row, col)
            self.second_player_take(row, col)
            if self.player_turn == 1:
                self.status = FPLAYER
            else:
                self.status = SPLAYER
            self.initPlayerTimer()
            self.startTimerPlayer()
            if self.player_turn == 2 and self.isAI:
                self.AI()

    def keyPressEvent(self, event):
        """processes key press events if you would like to do any"""
        if not self.isStarted or self.curPiece.shape() == Piece.NoPiece:
            super(Board, self).keyPressEvent(event)
            return
        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.try_move(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.try_move(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down:
            self.try_move(self.curPiece.rotateRight(), self.curX, self.curY)
        elif key == Qt.Key_Up:
            self.try_move(self.curPiece.rotateLeft(), self.curX, self.curY)
        elif key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_D:
            self.oneLineDown()
        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        """handles timer event"""

        #todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

    def reset_game(self):
        """clears pieces from the board"""

        # 2d int/Piece array to story the state of the game
        # 2 pion blanc, 3 pion noir
        self.boardArray = [[0, 3, 0, 3, 0, 3, 0, 3],
                           [3, 0, 3, 0, 3, 0, 3, 0],
                           [0, 3, 0, 3, 0, 3, 0, 3],
                           [1, 0, 1, 0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1],
                           [2, 0, 2, 0, 2, 0, 2, 0],
                           [0, 2, 0, 2, 0, 2, 0, 2],
                           [2, 0, 2, 0, 2, 0, 2, 0]]
        self.selected_piece = [-1, -1]
        # self.print_board_array()

    def try_move(self, new_x, new_y):
        """tries to move a piece"""

    def draw_board_squares(self, painter):
        """
        This function allows to draw all the square on the board.

        :param painter: The painter
        :return: Nothing
        """

        # todo set the default colour of the brush
        images = [QImage(WHITE_SQUARE), QImage(BLACK_SQUARE)]
        idx = 0
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                #painter.save()
                # Todo set this value equal the transformation you would like in the column direction (x)
                colTransformation = col * self.square_width()

                # Todo set this value equal the transformation you would like in the column direction (y)
                row_transformation = row * self.square_height()

                final_image = images[idx].scaled(self.square_width(), self.square_height())
                painter.drawImage(colTransformation, row_transformation, final_image)
                #painter.restore()
                idx = 1 if idx == 0 else 0
            idx = 1 if idx == 0 else 0

    def color_brush_white(self, row, col, i):
        """
        Set the brush color for white pieces
        :param row:
        :param col:
        :param i:
        :return:
        """
        brush_color = Qt.black
        if self.player_turn == 1 and self.selected_piece[1] == row and self.selected_piece[0] == col:
            brush_color = QColor.fromRgb(100, 255, 100)
        elif self.player_turn == 1 and self.selected_piece == [-1, -1]:
            if i > 0 and row > 0 and col > 0 and self.boardArray[row - 1][col - 1] == 1:
                brush_color = Qt.white
            elif i > 0 and row > 0 and col < 7 and self.boardArray[row - 1][col + 1] == 1:
                brush_color = Qt.white
            elif row > 1 and col > 1 and self.boardArray[row - 2][col - 2] == 1 and self.boardArray[row - 1][col - 1] == 3:
                brush_color = Qt.white
            elif row > 1 and col < 6 and self.boardArray[row - 2][col + 2] == 1 and self.boardArray[row - 1][col + 1] == 3:
                brush_color = Qt.white
        return brush_color

    def color_brush_black(self, row, col, i):
        """
        Set the brush color for black pieces
        :param row:
        :param col:
        :param i:
        :return:
        """
        brush_color = Qt.black
        if self.player_turn == 2 and self.selected_piece[1] == row and self.selected_piece[0] == col:
            brush_color = QColor.fromRgb(100, 100, 255)
        elif self.player_turn == 2 and self.selected_piece == [-1, -1]:
            if i > 0 and row < 7 and col > 0 and self.boardArray[row + 1][col - 1] == 1:
                brush_color = QColor.fromRgb(255, 0, 255)
            elif i > 0 and row < 7 and col < 7 and self.boardArray[row + 1][col + 1] == 1:
                brush_color = QColor.fromRgb(255, 0, 255)
            elif row < 6 and col > 1 and self.boardArray[row + 2][col - 2] == 1 and self.boardArray[row + 1][col - 1] == 2:
                brush_color = QColor.fromRgb(255, 0, 255)
            elif row < 6 and col < 6 and self.boardArray[row + 2][col + 2] == 1 and self.boardArray[row + 1][col + 1] == 2:
                brush_color = QColor.fromRgb(255, 0, 255)
        return brush_color

    def draw_pieces(self, painter):
        """draw the prices on the board"""
        brush_color = QColor.fromRgb(200, 200, 200)
        images = [QImage(WHITE_PIECE), QImage(BLACK_PIECE), QImage(WHITE_KING), QImage(BLACK_KING), QImage(BLACK_SQUARE)]
        idx = 0
        i = 0
        y = 1
        while i < 2:
            for row in range(0, len(self.boardArray)):
                for col in range(0, len(self.boardArray[0])):
                    #painter.save()
                    col_transformation = col * self.square_width()
                    row_transformation = row * self.square_height()
                    ## Todo victoire quand bloquer

                    if self.boardArray[row][col] == 2:
                        brush_color = self.color_brush_white(row, col, i)
                        idx = 0
                    elif self.boardArray[row][col] == 1:
                        brush_color = Qt.black
                        idx = 4
                    elif self.boardArray[row][col] == 3:
                        brush_color = self.color_brush_black(row, col, i)
                        idx = 1
                    elif self.boardArray[row][col] == 4:
                        brush_color = self.color_brush_white(row, col, i)
                        idx = 2
                    elif self.boardArray[row][col] == 5:
                        brush_color = self.color_brush_black(row, col, i)
                        idx = 3
                    elif self.boardArray[row][col] == 6:
                        brush_color = QColor.fromRgb(128, 128, 128)
                    if self.boardArray[row][col] != 0:
                        painter.setPen(brush_color)
                        if brush_color == Qt.white or brush_color == QColor.fromRgb(255, 0, 255):
                            y = 2
                        # Todo draw some the pieces as eclipses
                        radius_width = (self.square_width() / 10 * 8) / 2
                        radius_height = (self.square_height() / 10 * 8) / 2
                        center = QPoint(col_transformation + (self.square_width() / 2),
                                        row_transformation + (self.square_height() / 2))
                        if idx != 4:
                            painter.drawEllipse(center, radius_width, radius_height)
                            self.image = images[idx].scaled(radius_width * 2, radius_height * 2)
                            painter.drawImage(center.x() - radius_width, center.y() - radius_height, self.image)
                        #painter.restore()
                        self.update()
            i += y