import sys

class AI():
    """
    This method allows the AI to choose his move.
    This AI can't manage the  king's role.

    """
    def __init__(self, board):
        super().__init__()
        self.replay = False
        # copy of the game board
        self.gameBoard = [row[:] for row in board]
        # Increase the recursion's limit
        limit = sys.getrecursionlimit()
        sys.setrecursionlimit(3500)

    def Simulation(self, selected_piece, row, col, isMax, depth, board):
        """
        Remove piece if a player eat it.
        Call the MinMaxValue function to get the value according to the simulation of the shot.

        :param selected_piece: The piece position
        :param row: The piece position in row with the move
        :param col: The piece position in col with the move
        :return: The result of the MinMaxValue funtion

        """
        tmp_board = [row[:] for row in self.gameBoard]
        maxRow = len(tmp_board)
        maxCol = len(tmp_board[maxRow - 1])
        if isMax:
            tmp_board[row][col] = 3
        else:
            tmp_board[row][col] = 2
        replay = False

        # Remove the white piece on the board if the AI eat it
        if isMax and (row + 1 < maxRow and col + 1 >= 0 and row == selected_piece[0] + 2 and col == selected_piece[1] + 2):
            tmp_board[row + 1][col + 1] = 1
        elif isMax and (row + 1 < maxRow and col - 1 >= 0 and row == selected_piece[0] + 2 and col == selected_piece[1] - 2):
            tmp_board[row + 1][col - 1] = 1
        # Remove the black piece on the board if the Player eat it
        elif not isMax and (row - 1 < maxRow and col + 1 >= 0 and row == selected_piece[0] - 2 and col == selected_piece[1] + 2):
            tmp_board[row - 1][col + 1] = 1
        elif not isMax and (row - 1 < maxRow and col - 1 >= 0 and row == selected_piece[0] - 2 and col == selected_piece[1] - 2):
            tmp_board[row - 1][col - 1] = 1

        # Check if a piece become a king
        if isMax and row == len(tmp_board) - 1:
            tmp_board[row][col] = 5
        elif not isMax and row == 0:
            tmp_board[row][col] = 4

        tmp_board[selected_piece[0]][selected_piece[1]] = 1

        self.replay = replay
        return self.MinMaxValue(depth, isMax, tmp_board)

    def PieceCanMove(self, tmp_board, isMax):
        """
        Get each move that the player can do.

        :return: Return a list containig each move that the player can do.
        """
        maxRow = len(tmp_board)
        maxCol = len(tmp_board[maxRow - 1])
        piece_move = []

        for row in range(0, maxRow):
            for col in range(0, maxCol):
                if (isMax and tmp_board[row][col] == 3) or (not isMax and tmp_board[row][col] == 2):
                    # Save all move that the black player can do in the piece_move list
                    if isMax and (row + 1 < maxRow and col - 1 >= 0 and tmp_board[row + 1][col - 1] == 1) or \
                            (row + 1 < maxRow and col + 1 < maxCol and tmp_board[row + 1][col + 1] == 1) or \
                            (row + 2 < maxRow and col - 2 >= 0 and tmp_board[row + 2][col - 2] == 1 and
                             tmp_board[row + 1][col - 1] == 2) or \
                            (row + 2 < maxRow and col + 2 < maxCol and tmp_board[row + 2][col + 2] == 1 and
                             tmp_board[row + 1][col + 1] == 2):
                        piece_move.append([row, col])

                    # Save all move that the white player can do in the piece_move list
                    if not isMax and (row - 1 >= 0 and col - 1 >= 0 and tmp_board[row - 1][col - 1] == 1) or \
                            (row - 1 >= 0 and col + 1 < maxCol and tmp_board[row - 1][col + 1] == 1) or \
                            (row - 2 >= 0 and col - 2 >= 0 and tmp_board[row - 2][col - 2] == 1 and
                             tmp_board[row - 1][col - 1] == 3) or \
                            (row - 2 >= 0 and col + 2 < maxCol and tmp_board[row - 2][col + 2] == 1 and
                             tmp_board[row - 1][col + 1] == 3):
                        piece_move.append([row, col])
        return piece_move

    def MinMaxDecision(self, depth):
        """
        Show each shot, the player can do.
        Call the MinMaxValue function to create the "shot tree".

        :param depth: The level.
        :return: Return a list containing the x and y position that the player will do.
        """
        maxRow = len(self.gameBoard)
        maxCol = len(self.gameBoard[maxRow - 1])
        selected = []
        destination = []
        value = []

        for row in range(0, maxRow):
            for col in range(0, maxCol):
                if self.gameBoard[row][col] == 3:
                    # if the player can move at the bottom left
                    if row + 1 < maxRow and col - 1 >= 0 and self.gameBoard[row + 1][col - 1] == 1:
                        selected.append([row, col])
                        destination.append([row + 1, col - 1])
                        value.append(self.Simulation([row, col], row + 1, col - 1, False, depth, self.gameBoard))

                    # if the player can move at the bottom right
                    if row + 1 < maxRow and col + 1 < maxCol and self.gameBoard[row + 1][col + 1] == 1:
                        selected.append([row, col])
                        destination.append([row + 1, col + 1])
                        value.append(self.Simulation([row, col], row + 1, col + 1, False, depth, self.gameBoard))

                    # if the player can move at the bottom left to eat the opponent
                    if row + 2 < maxRow and col - 2 >= 0 and self.gameBoard[row + 2][col - 2] == 1 and \
                            self.gameBoard[row + 1][col - 1] == 2:
                        selected.append([row, col])
                        return [[row, col], [row + 2, col - 2]]

                    # if the player can move at the bottom right to eat the opponent
                    if row + 2 < maxRow and col + 2 < maxCol and self.gameBoard[row + 2][col + 2] == 1 and \
                            self.gameBoard[row + 1][col + 1] == 2:
                        selected.append([row, col])
                        destination.append([row + 2, col + 2])
                        return [[row, col], [row + 2, col + 2]]

        tmp_val = value[0]
        idx = 0
        for count in range(0, len(value)):
            if value[count] > tmp_val:
                tmp_val = value[count]
                idx = count
        return [selected[idx], destination[idx]]

    def isWinner(self, tmp_board, numPlayer):
        """
        Show if the player win.

        :param tmp_board: The board.
        :param numPlayer: The player
        :return: True  if the player win, else it return false.
        """
        for row in tmp_board:
            for col in row:
                if col == numPlayer:
                    return False
        return True

    def Evaluation(self, board):
        """
        Return the value of the shot.

        :return: value that corresponds to the importance of the move.
        """
        # 1 for a normal piece, 1.5 for a king
        black, white = 0, 0
        for row in board:
            for cell in row:
                if cell == 3:
                    black += 1.0
                elif cell == 5:
                    black += 1.5
                elif cell == 2:
                    white += 1.0
                elif cell == 4:
                    white += 1.5
        return black - white

    def MinMaxValue(self, depth, isMax, tmp_board):
        """

        Get the best move according to the player.

        :param depth: The depth
        :param isMax: True if it's the player black, else false
        :param tmp_board: The board

        :return: The value of the best move
        """

        maxRow = len(tmp_board)
        maxCol = len(tmp_board[maxRow - 1])

        # If the player win
        if self.isWinner(tmp_board, 3):
            return 100
        # If the AI win
        if self.isWinner(tmp_board, 2):
            return -100

        # if there are no more depth
        if depth == 0:
            return self.Evaluation(tmp_board)

        vals = []
        piece_can_move = self.PieceCanMove(tmp_board, isMax)

        for piece in piece_can_move:
            # Simulation of the AI move
            # if the AI can move at the bottom left
            if isMax and piece[0] + 1 < maxRow and piece[1] - 1 >= 0 and tmp_board[piece[0] + 1][piece[1] - 1] == 1:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] + 1, piece[1] - 1, not isMax, depth - 1, tmp_board))
                # if the AI can move at the bottom right
            if isMax and piece[0] + 1 < maxRow and piece[1] + 1 < maxCol and tmp_board[piece[0] + 1][piece[1] + 1] == 1:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] + 1, piece[1] + 1, not isMax, depth - 1, tmp_board))
            # if the AI can move at the bottom left to eat the opponent
            if isMax and piece[0] + 2 < maxRow and piece[1] - 2 >= 0 and tmp_board[piece[0] + 2][piece[1] - 2] == 1 and \
                    tmp_board[piece[0] + 1][piece[1] - 1] == 2:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] + 2, piece[1] - 2, not isMax, depth - 1, tmp_board))
                # if the AI can move at the bottom right to eat the opponent
            if isMax and piece[0] + 2 < maxRow and piece[1] + 2 < maxCol and tmp_board[piece[0] + 2][piece[1] + 2] == 1 and \
                    tmp_board[piece[0] + 1][piece[1] + 1] == 2:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] + 2, piece[1] + 2, not isMax, depth - 1, tmp_board))

            # Simulation of the Player move
                # if the player can move at the top left
            if not isMax and piece[0] - 1 >= 0 and piece[1] - 1 >= 0 and tmp_board[piece[0] - 1][piece[1] - 1] == 1:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] - 1, piece[1] - 1, not isMax, depth - 1, tmp_board))
                # if the player can move at the top right
            if not isMax and piece[0] - 1 >= 0 and piece[1] + 1 < maxCol and tmp_board[piece[0] - 1][piece[1] + 1] == 1:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] - 1, piece[1] + 1, not isMax, depth - 1, tmp_board))
                # if the player can move at the top left to eat the opponent
            if not isMax and piece[0] - 2 >= 0 and piece[1] - 2 >= 0 and tmp_board[piece[0] - 2][piece[1] - 2] == 1 and \
                    tmp_board[piece[0] - 1][piece[1] - 1] == 3:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] - 2, piece[1] - 2, not isMax, depth - 1, tmp_board))
                # if the player can move at the top right to eat the opponent
            if not isMax and piece[0] - 2 >= 0 and piece[1] + 2 < maxCol and tmp_board[piece[0] - 2][piece[1] + 2] == 1 and \
                    tmp_board[piece[0] - 1][piece[1] + 1] == 3:
                vals.append(self.Simulation([piece[0], piece[1]], piece[0] - 2, piece[1] + 2, not isMax, depth - 1, tmp_board))

        retVal = 0
        if len(vals) > 0:
            retVal = vals[0]
        for elem in vals:
            if isMax and elem > retVal:
                retVal = elem
            elif not isMax and elem < retVal:
                retVal = elem
        return retVal
