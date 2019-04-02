from board import Board
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QListWidget, QTextEdit, QDockWidget, QAction, \
    QFileDialog, QWidget, QVBoxLayout, QLCDNumber, QSlider, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap, QLinearGradient, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSlot
from PyQt5 import QtGui, QtCore
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, Qt
import sip

PATH_BLACK_PIECE = "./icons/black_piece_panel.png"
PATH_WHITE_PIECE = "./icons/white_piece_panel.png"

WINNER_P1 = "The winner is: player 1 !"
WINNER_P2 = "The winner is: player 2 !"
WINNER_AI = "The winner is: the AI !"


class ScoreBoard(QDockWidget):
    """
    This class allows to display the scoreboard.

    """
    def __init__(self, Board):
        super().__init__()
        self.initUI(Board)

    def initUI(self, Board):
        """
        Initialization of the ScoreBoard UI.

        :param Board: The class board which manages the game.
        :return: Nothing
        """

        # Set if the player play against an AI
        self.ai = False

        # Initalization of the window
        self.resize(200, 800)
        self.setFixedSize(self.size())
        self.center()
        self.setWindowTitle('Game Panel')

        # Initialization of the Board class
        self.boardInfos = Board

        # Initialization of the QWidget which contain all information
        self.dockedWidget = QWidget(self)
        self.setWidget(self.dockedWidget)

        # Initialization of the timer and the players information
        self.timer = self.display_timer()
        self.infosPlayer1 = self.displayInfoPlayer1()
        self.infosPlayer2 = self.displayInfoPlayer2()

        # Set all information in the widget
        self.dockedWidget.setLayout(QVBoxLayout())
        self.dockedWidget.layout().addWidget(self.timer)
        self.dockedWidget.layout().addWidget(self.infosPlayer1)
        self.dockedWidget.layout().addWidget(self.infosPlayer2)

    def setAI(self, isAI):
        """
        Set the boolean to true to modify the player's name

        :return: Nothing
        """
        self.ai = isAI

    def updateUI(self):
        """
        Update the UI to display the timer and when the user want to create a new game.

        :return: Nothing
        """
        # deletion of the timer widget with the timer's child
        self.dockedWidget.layout().removeWidget(self.timer)
        sip.delete(self.timer)
        self.timer = None

        # deletion of the player one widget with the players one's child
        self.dockedWidget.layout().removeWidget(self.infosPlayer1)
        sip.delete(self.infosPlayer1)
        self.infosPlayer1 = None

        # deletion of the player two widget with the player two's child
        self.dockedWidget.layout().removeWidget(self.infosPlayer2)
        sip.delete(self.infosPlayer2)
        self.infosPlayer2 = None

        # Initialization of the timer and the player's information
        self.timer = self.display_timer()
        self.infosPlayer1 = self.displayInfoPlayer1()
        self.infosPlayer2 = self.displayInfoPlayer2()

        # Set all information in the widget
        self.dockedWidget.layout().addWidget(self.timer)
        self.dockedWidget.layout().addWidget(self.infosPlayer1)
        self.dockedWidget.layout().addWidget(self.infosPlayer2)

    def displayInfoPlayer1(self):
        """

        This function allows to create the widget which contains the player one information.
        It displays the player name, the turn, the timer, the number of remaining and jumps.

        :return: playerOne: The widget which contains all information of the user
        """
        # Initialization of the player number
        name_player = 2
        # Initialization of player name
        if self.ai:
            player = QLabel("AI")
        else:
            player = QLabel("Player")

        # Initialization of the layout
        grid = QGridLayout()

        # Set all information's player in the layout
        grid.addWidget(self.get_image_player(name_player), 1, 1, 1, 2)
        grid.addWidget(self.get_turn(name_player), 1, 2, 1, 3)
        grid.addWidget(player, 2, 1)
        grid.addWidget(self.get_player_timer(name_player), 3, 1)
        grid.addWidget(self.get_remaining_label(name_player), 4, 1)
        grid.addWidget(self.get_jumps_label(name_player), 5, 1)

        # Initialization of the widget
        playerOne = QWidget(self)

        # Set the player layout in the widget
        playerOne.setLayout(grid)
        return playerOne

    def displayInfoPlayer2(self):
        """

        This function allows to create the widget which contains the player two information.
        It displays the player name, the turn, the timer, the number of remaining and jumps.

        :return: playerTwo: The widget which contains all information of the user
        """
        # Initialization of the player number
        name_player = 1

        # Initialization of player name
        if self.ai:
            player = QLabel("Player")
        else:
            player = QLabel("Opponent")

        # Initialization of the layout
        grid = QGridLayout()

        # Set all information's player in the layout
        grid.addWidget(self.get_image_player(name_player), 1, 1, 1, 2)
        grid.addWidget(self.get_turn(name_player), 1, 2, 1, 3)
        grid.addWidget(player, 2, 1)
        grid.addWidget(self.get_player_timer(name_player), 3, 1)
        grid.addWidget(self.get_remaining_label(name_player), 4, 1)
        grid.addWidget(self.get_jumps_label(name_player), 5, 1)

        # Initialization of the widget
        playerTwo = QWidget(self)

        # Set the player layout in the widget
        playerTwo.setLayout(grid)
        return playerTwo

    def get_player_timer(self, namePlayer):
        """
        This function allows to know the player's turn and display his timer if it's his turn.
        The format is the following: 'Timer: 00:00:00'

        :param namePlayer: The player number.
        :return: The Qlabel which contains the player's timer.
        """
        if self.boardInfos.player_turn == 1 and namePlayer == 1:
            timeP = "Timer: " + self.boardInfos.timePlayer.toString("mm:ss")
        elif self.boardInfos.player_turn == 2 and namePlayer == 2:
            timeP = "Timer: " + self.boardInfos.timePlayer.toString("mm:ss")
        else:
            timeP = "Timer: Stopped"
        return QLabel(timeP)

    def get_image_player(self, playerName):
        """
        This function allows to display the player's image.


        :param playerName: Player number
        :return: The image of the player (QPixmap)
        """
        image = QLabel()
        if playerName == 1:
            pixmap = QtGui.QPixmap(PATH_WHITE_PIECE)
        else:
            pixmap = QtGui.QPixmap(PATH_BLACK_PIECE)
        image.setPixmap(pixmap)
        return image

    def get_turn(self, namePlayer):
        """
        This function allows to get the player's turn and return a QLabel which contains 'Your turn' beside
        his image if it's his turn.
        If not the function return an empty QLabel.

        :param namePlayer: The player number
        :return: The QLabel which contains the player turn.
        """
        if self.boardInfos.player_turn == 1 and namePlayer == 1:
            return QLabel(" Your Turn")
        elif self.boardInfos.player_turn == 2 and namePlayer == 2:
            return QLabel(" Your Turn")
        else:
            return QLabel("")

    def get_remaining_label(self, numPlayer):
        """
        This function allows to get the player's ramaining and return it in a QLabel.
        The sentence have this format:  'Remaining: 12'.

        :param numPlayer: The player number .
        :return: QLabel which contains the player's remaining.
        """
        if numPlayer == 1:
            numRemaining = self.boardInfos.playersRemaining[0]
        else:
            numRemaining = self.boardInfos.playersRemaining[1]
        strRemaining = "Remaining: " + str(numRemaining)
        return QLabel(strRemaining)

    def get_jumps_label(self, numPlayer):
        """
        This function allows to get the player's jumps and return it in a QLabel.
        The sentence have this format:  'Jumps: 12'.

        :param numPlayer: The player number .
        :return: QLabel which contains the player's jumps.
        """
        if numPlayer == 1:
            numJumps = self.boardInfos.playersJumps[0]
        if numPlayer == 2:
            numJumps = self.boardInfos.playersJumps[1]
        strJump = "Jumps: " + str(numJumps)
        return QLabel(strJump)

    def display_timer(self):
        """
        This function allows to display the timer of the name of the winner.

        If the game is not over it get the timer and return it in to a QLabel.
        The format is the following: 'Time Passed: 00:00'

        If the game is  over it get the winner's name and return it in to a QLabel.

        :return: The QLabel which contains the timer or the winner of the game.
        """

        if self.boardInfos.timePassed:
            if self.boardInfos.winner == 1:
                winnerGame = WINNER_P1
            elif self.boardInfos.winner == 2:
                winnerGame = WINNER_P2
            elif self.boardInfos.winner == 3:
                winnerGame = WINNER_AI
            return QLabel(winnerGame)
        else:
            gameTime = "Time Passed: " + self.boardInfos.time.toString("mm:ss")
            return QLabel(gameTime)

    def center(self):
        '''centers the window on the screen'''
        pass