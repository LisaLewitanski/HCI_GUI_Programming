from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QRect
from board import Board
from scoreBoard import ScoreBoard
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QWidget, QVBoxLayout, QLCDNumber, QSlider, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QPixmap, QLinearGradient, QPainterPath
import sys
import os
from PyQt5.QtWidgets import *

CLEAR_IMAGE = "./icons/clear.png"
PAUSE_IMAGE = "./icons/pause.png"
STATUS_IMAGE = "./icons/status.png"
HELP_IMAGE = "./icons/help.png"
EXIT_IMAGE = "./icons/logout.png"
ROBOT_EASY = "./icons/roboteasy.png"
ROBOT_MEDIUM = "./icons/robotmedium.png"
ROBOT_HARD = "./icons/robothard.png"


class Draughts(QMainWindow):
    """
    This class allows to create the board for the game and the scoreboard to display all information.
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initilization of the game board and the score board.

        :return: Nothing
        """
        # Initialization of the board class
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        # Initialization of the ScoreBoard class
        self.scoreBoard = ScoreBoard(self.tboard)
        self.tboard.setScoreBoard(self.scoreBoard)

        # Set the score board in a dockwidget at the right of the window
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)

        # Initialization of the status bar
        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # Start the class Board
        self.tboard.start()
        self.gameToolbar()

        # Initialization of the windows
        self.resize(900, 800)
        self.setFixedSize(self.size())
        self.center()
        self.setWindowTitle('Checkers')
        self.show()

    def center(self):
        """
        Centers the window on the screen
        :return: Nothing
        """

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def gameToolbar(self):
        """
        This function allows to create the Menubar.
        It contains th Game, the View, the Help and the Exit menu.
        :return: Nothing
        """
        # Declaration of each menu in the menu bar.
        mainMenu = self.menuBar()
        self.resetMenu = mainMenu.addMenu(" Game")
        self.aiMenu = mainMenu.addMenu(" AI")
        self.viewMenu = mainMenu.addMenu(" View")
        self.helpMenu = mainMenu.addMenu(" Help")
        self.exitMenu = mainMenu.addMenu(" Exit")

        # Initialization of each menu in the menu bar.
        self.gameSettings()
        self.gameAIEasy()
        self.gameAIMedium()
        self.gameAIHard()
        self.pauseGame()
        self.viewSettings()
        self.helpSettings()
        self.exitSettings()

    def gameSettings(self):
        """
        This function allows to reset the game.
        The shortcut is the following: Ctrl+R
        If the user click on this menu, the resetGame funtion will be call.

        :return: Nothing
        """
        resetAction = QAction(QIcon(CLEAR_IMAGE), "Reset", self)
        resetAction.setShortcut("Ctrl+R")
        self.resetMenu.addAction(resetAction)
        resetAction.triggered.connect(self.resetGame)

    def gameAIEasy(self):
        """
        This function allows to create a game against an artificial intelligence.
        The shortcut is the following: Ctrl+A
        If the user click on this menu, the AIPlayer funtion will be call.

        :return: Nothing
        """
        aiAction = QAction(QIcon(ROBOT_EASY), "Play against an easy AI", self)
        aiAction.setShortcut("Ctrl+A")
        self.aiMenu.addAction(aiAction)
        aiAction.triggered.connect(self.AIPlayerE)

    def gameAIMedium(self):
        """
        This function allows to create a game against an artificial intelligence.
        The shortcut is the following: Ctrl+A
        If the user click on this menu, the AIPlayer funtion will be call.

        :return: Nothing
        """
        aiAction = QAction(QIcon(ROBOT_MEDIUM), "Play against an medium AI", self)
        aiAction.setShortcut("Ctrl+Q")
        self.aiMenu.addAction(aiAction)
        aiAction.triggered.connect(self.AIPlayerM)

    def gameAIHard(self):
        """
        This function allows to create a game against an artificial intelligence.
        The shortcut is the following: Ctrl+A
        If the user click on this menu, the AIPlayer funtion will be call.

        :return: Nothing
        """
        aiAction = QAction(QIcon(ROBOT_HARD), "Play against an hard AI", self)
        aiAction.setShortcut("Ctrl+W")
        self.aiMenu.addAction(aiAction)
        aiAction.triggered.connect(self.AIPlayerH)

    def pauseGame(self):
        """
        This function allows set the game in pause.
        The shortcut is the following: Ctrl+P
        If the user click on this menu, the pause funtion will be call.

        :return: Nothing
        """
        resetAction = QAction(QIcon(PAUSE_IMAGE), "Pause / Continue", self)
        resetAction.setShortcut("Ctrl+P")
        self.resetMenu.addAction(resetAction)
        resetAction.triggered.connect(self.pause)

    def viewSettings(self):
        """
        This function allows to view the status of the game.
        The shortcut is the following: Ctrl+V
        If the user click on this menu, the viewStatus funtion will be call.

        :return: Nothing
        """

        resetAction = QAction(QIcon(STATUS_IMAGE), "View status", self)
        resetAction.setShortcut("Ctrl+V")
        self.viewMenu.addAction(resetAction)
        resetAction.triggered.connect(self.viewStatus)

    def helpSettings(self):
        """
        This function allows to display the rules of the game.
        The shortcut is the following: Ctrl+H
        If the user click on this menu, the help funtion will be call.

        :return: Nothing
        """

        helpAction = QAction(QIcon(HELP_IMAGE), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        self.helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

    def exitSettings(self):
        """
        This function allows to exit the checkers game.
        The shortcut is the following: Ctrl+E

        :return: Nothing
        """

        exitAction = QAction(QIcon(EXIT_IMAGE), "Exit", self)
        exitAction.setShortcut("Ctrl+E")
        self.exitMenu.addAction(exitAction)
        exitAction.triggered.connect(qApp.quit)

    def resetGame(self):
        """
        This function will initialize the game and the score board.

        :return: Nothing
        """
        # Initialization of the game
        self.tboard.init()
        self.tboard.start()
        # Initialization of the scoreBoard
        self.scoreBoard.setAI(False)
        self.scoreBoard.updateUI()
        self.tboard.setScoreBoard(self.scoreBoard)

    def pause(self):
        """
        This function will call the pause function in the Board class to set the game in pause.

        :return: Nothing
        """
        self.tboard.pause()

    def AIPlayerE(self):
        """
        Function to allows the player to play against an easy AI

        :return: Nothing
        """
        self.tboard.isAI = True
        self.scoreBoard.setAI(True)
        self.tboard.aiDifficulties = 1

    def AIPlayerM(self):
        """
        Function to allows the player to play against an medium AI

        :return: Nothing
        """
        self.tboard.isAI = True
        self.scoreBoard.setAI(True)
        self.tboard.aiDifficulties = 2

    def AIPlayerH(self):
        """
        Function to allows the player to play against an hard AI

        :return: Nothing
        """
        self.tboard.isAI = True
        self.scoreBoard.setAI(True)
        self.tboard.aiDifficulties = 3

    def viewStatus(self):
        """
        This function allows to display the status of the game in a QMessageBox.

        :return: Nothing
        """
        title = "Game status "
        message = self.tboard.status
        QMessageBox.about(self, title, message)
        self.show()

    def help(self):
        """
        This function display a QMessageBox. This box help the user to know what the application
        exactyly doing.
        Indeed, it contains rules of the game.

        :return: Nothing
        """
        title = "Help"
        message = "It's a checker game.\n" \
                  "The rules:\n" \
                  "Moves are allowed only on the dark squares, so pieces always move diagonally.\n" \
                  "Single pieces are always limited to forward moves.\n" \
                  "A piece making a move only on one square. A piece making a capturing move leaps over one of the opponent's pieces,\n" \
                  "landing in a straight diagonal line on the other side.\n" \
                  "Only one piece may be captured in a single jump; however, multiple jumps are allowed during a single turn.\n" \
                  "When a piece is captured, it is removed from the board.\n" \
                  "If a player is able to make a capture, there is no option; the jump must be made.\n" \
                  "If more than one capture is available, the player is free to choose whichever he or she prefers.\n" \
                  "When a piece reaches the furthest row from the player who controls that piece, it is crowned and becomes a king.\n" \
                  "One of the pieces which had been captured is placed on top of the king so that it is twice as high as a single piece.\n" \
                  "Kings are limited to moving diagonally but may move both forward and backward.\n" \
                  "Kings may combine jumps in several directions, forward and backward, on the same turn.\n" \
                  "Single pieces may shift direction diagonally during a multiple capture turn, but must always jump forward.\n"

        QMessageBox.about(self, title, message)
        self.show()

