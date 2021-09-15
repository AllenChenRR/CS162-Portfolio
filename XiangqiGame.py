# Author: Allen Chen (934266694)
# Date: 2/29/2020
# Description: Xiangqi Game



class XiangqiGame:
    """
    Chinese Chess Board Game that involves 16 pieces on each side of the board.
    Goal: Capture the opponent's general
    """
    def __init__(self):
        self._game_state = "UNFINISHED"
        self._board = Board()
        self._player_turn = 1  # 1 if Red's turn and -1 if Black's turn

    def make_move(self, start, end):
        """
        If valid, makes move and returns True , otherwise returns False
        """
        start_pos = self.parse_pos(start)  # Start and end position are lists that contain column and row
        end_pos = self.parse_pos(end)

        start_row = start_pos[0]  # Position of row and columns are assigned to variables
        start_col = start_pos[1]
        end_row = end_pos[0]
        end_col = end_pos[1]

        board = self._board.get_board()
        start_piece = board[start_row][start_col].get_piece()
        end_piece = board[end_row][end_col].get_piece()


        # If there is no piece to be moved or game is over or piece is to be moved to its original location
        if start_piece is None or self._game_state != "UNFINISHED"\
                or (start_row == end_row and start_col == end_col):
            return False

        start_piece_id = start_piece.get_player_id()  # Contains the player id associated with the piece
        end_piece_player_id = None
        if end_piece is not None:  # Executes if end piece contains a piece object
            end_piece_player_id = end_piece.get_player_id()

        # If Red's turn
        if self._player_turn == 1:
            if start_piece_id != 'r':  # If red moves a black piece
                return False
            if start_piece.is_legal_move(start, end, start_piece, end_piece_player_id, board) : # Checks the legal move conditions
                if self.move_piece(start, end):  # Returns False if move is invalid
                    # Checks if move violates flying general and puts self in check
                    if self.is_not_flying_general() is True and self.is_in_check("red") is False:
                        self.change_player_turn()
                        self.is_in_checkmate()
                        return True
                    else:  # Reverses the move if violates flying general rule
                        self.reverse_move(start, end, board,end_piece_player_id, end_piece)
                        return False

                else:
                    return False
            else:
                return False

        # If Black's turn
        elif self._player_turn == -1:
            if start_piece_id != 'b':  # If black moves a red piece
                return False
            if start_piece.is_legal_move(start, end, start_piece, end_piece_player_id, board):  # Checks the legal move conditions
                if self.move_piece(start, end):  # Returns False if move is invalid
                    if self.is_not_flying_general() is True and self.is_in_check("black") is False:
                        self.change_player_turn()
                        self.is_in_checkmate()
                        return True
                    else:  # Reverses the move if violates flying general rule
                        self.reverse_move(start, end, board, end_piece_player_id, end_piece)
                        return False
                else:
                    return False
            else:
                return False


    def change_player_turn(self):
        """Changes player turn by multiplying by -1. Turns are determined sign of the integer."""
        self._player_turn *= -1

    def set_player_turn(self, num):
        self._player_turn = num

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def set_game_state(self,winner):
        """Sets the game state to who won"""
        if winner == 'b':
            self._game_state = "BLACK_WON"
        else:
            self._game_state = "RED_WON"


    def parse_pos(self, pos):
        """Parse pos into a list of column and row respectively"""

        column = ord(pos[0]) - 97
        if len(pos) == 2:
            row = ord(pos[1]) - 49
        else:
            row = 9
        return [row, column]

    def location_to_pos(self,row, col):
        """Converts board index to string arguments"""

        pos_row = str(row + 1)
        pos_col = chr(col + 97)
        return pos_col + pos_row

    def move_piece(self,start_location, end_location):
        """
        Moves piece if move is legal, returns True and makes move.
        Returns False if piece is to move to ally piece
        """

        board = self._board.get_board()
        start_pos = self.parse_pos(start_location)  # Start and end position are lists that contain column and row
        end_pos = self.parse_pos(end_location)

        start_row = start_pos[0]  # Position of row and columns are assigned to variables
        start_col = (start_pos[1])
        end_row = end_pos[0]
        end_col = end_pos[1]

        #  Moves piece to new coordinate and sets old coordinate to hold no piece
        start_piece = board[start_row][start_col].get_piece()  # Sets the original start piece
        end_piece = board[end_row][end_col].get_piece()

        # If end location has no piece or piece attacks enemy
        if end_piece is None or start_piece.get_player_id() != end_piece.get_player_id():
            start_piece.set_location(end_location)  # Sets location of start piece to new location
            board[end_row][end_col].set_piece(start_piece)  # Sets end coordinate's piece to start piece
            board[start_row][start_col].set_piece(None)  # Sets start coordinate's piece to None
            return True
        # Returns False if piece attacks ally piece
        else:
            return False

    def display_board(self):
        self._board.display_board()

    def get_player_turn(self):
        """Returns the player turn. Positive if red. Negative if black"""
        return self._player_turn

    def is_in_check(self, player_side):
        """
       Checks if the player is in check
        """
        board = self._board.get_board()
        player_id = player_side[0]
        # Sets the appropriate player IDs
        if player_id == 'r':
            opp_player_id = 'b'
        else:
            opp_player_id = 'r'

        player_king_id = player_id + "G1"
        player_king_pos = ""

        # Finding the player's king
        for row in range(10):
            for col in range(9):
                if board[row][col].get_piece() is not None:
                    if board[row][col].get_piece().get_id() == player_king_id:
                        player_king_pos = self.location_to_pos(row,col)

        # Loops through all opposing pieces to attack the player's king
        for row in range(10):
            for col in range(9):
                if board[row][col].get_piece() is not None:
                    if board[row][col].get_piece().get_player_id() == opp_player_id:
                        opp_piece_pos = self.location_to_pos(row,col)
                        opp_piece = board[row][col].get_piece()
                        if opp_piece.is_legal_move(opp_piece_pos, player_king_pos,opp_piece, player_king_id,board):
                            return True
        return False  # Returns False if no opposing piece can attack the king

    def is_not_flying_general(self):
        board = self._board.get_board()
        red_king_id = "rG1"
        black_king_id = "bG1"

        for row in range(10):
            for col in range(9):
                if board[row][col].get_piece() is not None:
                    if board[row][col].get_piece().get_id() == red_king_id:
                        red_king_row = row
                        red_king_col = col
                    if board[row][col].get_piece().get_id() == black_king_id:
                        black_king_row = row
                        black_king_col = col


        #  Checks for flying general condition
        if black_king_col == red_king_col:
            for row in range(red_king_row + 1, black_king_row):
                if board[row][red_king_col].get_piece() is not None:
                    return True
        return False

    def reverse_move(self, start, end, board, end_piece_player_id,end_piece):
        start_pos = self.parse_pos(start)  # Start and end position are lists that contain column and row
        end_pos = self.parse_pos(end)

        start_row = start_pos[0]  # Position of row and columns are assigned to variables
        start_col = start_pos[1]
        end_row = end_pos[0]
        end_col = end_pos[1]

        # Sets piece back to start_pos on chess board
        board[start_row][start_col].set_piece(board[end_row][end_col].get_piece())

        if end_piece_player_id is None:  # If end_pos contained no piece
            board[end_row][end_col].set_piece(None)
        else:  # If end_pos contained a chess piece
            board[end_row][end_col].set_piece(end_piece)

    def is_in_checkmate(self):
        """Checks if game has resulted in a checkmate"""

        done = False  # Determines when to stop the loop to check
        checkmate = True
        if not self.is_in_check("red") and not self.is_in_check("black"):  # Exits the function if not one side is checked
            return False

        board = self._board.get_board()
        possible_move_list = []

        # Red's Turn: Creates a list of all possible positions for red to move
        if self.get_player_turn() == 1:  # Red's turn
            for row in range(10):
                for col in range(9):
                    if board[row][col].get_piece() is None or board[row][col].get_piece().get_player_id() == 'b':
                        possible_move_list.append(self.location_to_pos(row, col))

            # Checks for all possible moves
            for row in range(10):
                for col in range(9):
                    if board[row][col].get_piece() is not None:
                        if board[row][col].get_piece().get_player_id() == 'r':  # Loops through all the red pieces on board
                            start = self.location_to_pos(row,col)
                            for move in possible_move_list:  # Checks for move
                                if not done:
                                    end_loc = self.parse_pos(move)
                                    end_row = end_loc[0]
                                    end_col = end_loc[1]
                                    end_piece = board[end_row][end_col].get_piece()
                                    end_piece_player_id = None
                                    if end_piece is not None:
                                        end_piece_player_id = end_piece.get_player_id()
                                    if self.make_move(start, move) is True:
                                        if self.is_in_check("red") is False:  # If there is a way to get out of a check
                                            done = True
                                            checkmate = False
                                        self.reverse_move(start,move, board, end_piece_player_id, end_piece)
                                        self.set_player_turn(1)
            if checkmate:
                self.set_game_state('b')  # Black wins

        # Black's Turn: Creates a list of all possible positions for black to move
        elif self.get_player_turn() == -1:  # Blacks's turn
            for row in range(10):
                for col in range(9):
                    if board[row][col].get_piece() is None or board[row][col].get_piece().get_player_id() == 'r':
                        possible_move_list.append(self.location_to_pos(row, col))

            # Checks for all possible moves
            for row in range(10):
                for col in range(9):
                    if board[row][col].get_piece() is not None:
                        if board[row][col].get_piece().get_player_id() == 'b':  # Loops through all the black pieces on board
                            start = self.location_to_pos(row,col)
                            for move in possible_move_list:  # Checks for move
                                if not done:
                                    end_loc = self.parse_pos(move)
                                    end_row = end_loc[0]
                                    end_col = end_loc[1]
                                    end_piece = board[end_row][end_col].get_piece()
                                    end_piece_player_id = None
                                    if end_piece is not None:
                                        end_piece_player_id = end_piece.get_player_id()
                                    if self.make_move(start, move) is True:
                                        if self.is_in_check("black") is False:  # If there is a way to get out of a check
                                            done = True
                                            checkmate = False
                                        self.reverse_move(start,move, board, end_piece_player_id, end_piece)
                                        self.set_player_turn(-1)
            if checkmate:
                self.set_game_state('r')  # Red wins


class Board:
    """
    Represents a Board with coordinate objects.
    Each coordinate object will accept parameters with rows and columns
    to identify its position in the 2-D array
    """
    def __init__(self):

        # Board of 9 columns and 10 rows of Coordinate objects
        self._board = [[Coordinate(i, j) for i in range(9)] for j in range(10)]

        self._board[3][0].set_piece(Soldier("a4", "rS1"))   # Red Soldiers
        self._board[3][2].set_piece(Soldier("c4", "rS2"))
        self._board[3][4].set_piece(Soldier("e4", "rS3"))
        self._board[3][6].set_piece(Soldier("g4", "rS4"))
        self._board[3][8].set_piece(Soldier("i4", "rS5"))

        self._board[2][1].set_piece(Cannon("b3", "rC1"))  # Red Cannons
        self._board[2][7].set_piece(Cannon("h3", "rC2"))

        self._board[0][0].set_piece(Chariot("a1", "rR1"))  # Red Chariots
        self._board[0][8].set_piece(Chariot("i1", "rR2"))

        self._board[0][1].set_piece(Horse("b1", "rH1"))  # Red Horses
        self._board[0][7].set_piece(Horse("h1", "rH2"))

        self._board[0][2].set_piece(Elephant("c1", "rE1"))  # Red Elephants
        self._board[0][6].set_piece(Elephant("g1", "rE2"))

        self._board[0][3].set_piece(Advisor("d1", "rA1"))  # Red Advisors
        self._board[0][5].set_piece(Advisor("f1", "rA2"))

        self._board[0][4].set_piece(General("e1", "rG1"))  # Red General

        self._board[6][0].set_piece(Soldier("a7", "bS1"))   # Black Soldiers
        self._board[6][2].set_piece(Soldier("c7", "bS2"))
        self._board[6][4].set_piece(Soldier("e7", "bS3"))
        self._board[6][6].set_piece(Soldier("g7", "bS4"))
        self._board[6][8].set_piece(Soldier("i7", "bS5"))

        self._board[7][1].set_piece(Cannon("b8", "bC1"))  # Black Cannons
        self._board[7][7].set_piece(Cannon("h8", "bC2"))

        self._board[9][0].set_piece(Chariot("a10", "bR1"))  # Black Chariots
        self._board[9][8].set_piece(Chariot("i10", "bR2"))

        self._board[9][1].set_piece(Horse("b10", "bH1"))  # Black Horses
        self._board[9][7].set_piece(Horse("h10", "bH2"))

        self._board[9][2].set_piece(Elephant("c10", "bE1"))  # Black Elephants
        self._board[9][6].set_piece(Elephant("g10", "bE2"))

        self._board[9][3].set_piece(Advisor("d10", "bA1"))  # Black Advisors
        self._board[9][5].set_piece(Advisor("f10", "bA2"))

        self._board[9][4].set_piece(General("e10", "bG1"))  # Black General

    def display_board(self):
        """Prints the chess board with labeled columns and rows"""
        board = self._board
        col = "A"
        row = 1

        print(end="|")
        for i in range(9):  # Prints column labels of board
            print(" " + col + " |", end="")
            col = chr(ord(col) + 1)
        print()

        for i in range(10):  # Prints the board
            print(end="|")
            for j in range(9):
                if board[i][j].get_piece() is not None:
                    print(board[i][j].get_piece().get_id(), end ="|")
                else:
                    print("   ", end = "|")
            print(" " + str(row))
            if i != 4 and i != 9:
                print("____" * 9)
            if i == 4:
                print("~~~~~~~~~~~~~~~~RIVER~~~~~~~~~~~~~~~")
            row += 1

    def get_board(self):
        return self._board


class Coordinate:
    def __init__(self, col, row):
        self._piece = None
        self._col = col
        self._row = row

    def set_piece(self, piece):
        self._piece = piece

    def get_piece(self):
        return self._piece

    def get_col(self):
        return self._col

    def get_row(self):
        return self._row


class Pieces:
    """Class that represents all the chess pieces"""

    def __init__(self, location, id_code):
        self._location = location
        self._id_code = id_code

    def get_location(self):
        return self._location

    def set_location(self, new_location):
        self._location = new_location

    def get_id(self):
        return self._id_code

    def get_player_id(self):
        return self._id_code[0]

    def parse_positions(self, start_pos, end_pos):
        """Parse board position into a location of row and column on board"""

        start_column = ord(start_pos[0]) - 97
        if len(start_pos) == 2:
            start_row = ord(start_pos[1]) - 49
        else:
            start_row = 9
        end_column = ord(end_pos[0]) - 97
        if len(end_pos) == 2:
            end_row = ord(end_pos[1]) - 49
        else:
            end_row = 9
        return [start_row, start_column, end_row, end_column]




class General(Pieces):

    """
    Class for the General
    """

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Returns True if end location is a valid """
        """General moves should only move +1 or -1 from its starting row and col"""

        # Checks for legality if end position contains a piece and it does not attack own side's piece
        parsed_positions = self.parse_positions(start_pos, end_pos)
        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        # Case for red General
        if start_piece.get_player_id() == 'r':  # Start piece is guaranteed to contain a piece, binds red to the palace
            if 3 <= end_col <= 5 and 0 <= end_row <= 2:
                if abs(start_col - end_col) >= 1 and abs(start_row - end_row) >= 1:
                    return False
                else:
                    return True
            else:
                return False
        # Case for black General
        else:
            if 3 <= end_col <= 5 and 7 <= end_row <= 9:  # Binds end_pos to the palace
                if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:  # Guarantees that diagonal movements will return false
                    return False
                else:
                    return True
            else:
                return False

class Advisor(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """
        Method that checks whether move is legal based on starting and ending position
        :param start_pos: String argument of the starting coordinate
        :param end_pos: String argument of the ending coordinate
        :param start_piece:
        :param end_piece_player_id:
        :return: True if move is valid, otherwise False
        """
        parsed_positions = self.parse_positions(start_pos, end_pos)
        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        # Case for Red's side
        if start_piece.get_player_id() == 'r':
            if not (3 <= end_col <= 5 and 0 <= end_row <= 2): # Returns False when is to move outside the palace
                return False
            else:
                if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:  # Checks if end_pos forces a move diagonally
                    return True
                else:
                    return False

        # Case for Black's side
        else:
            if not (3 <= end_col <= 5 and 7 <= end_row <= 9): # Returns False when is to move outside the palace
                return False
            else:
                if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:  # Checks if end_pos forces a move diagonally
                    return True
                else:
                    return False



class Elephant(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Method that checks whether move is legal based on starting and ending position"""
        parsed_positions = self.parse_positions(start_pos, end_pos)

        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        if start_piece.get_player_id() == 'r': # If elephant is red

            if end_row >= 5: # Checks if end_pos forces red elephant to cross river
                return False

            # Check elephant moves diagonally two spaces
            elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:

                # Elephant moving to the left
                if end_col - start_col == -2:
                    if end_row - start_row == -2: # Elephant moving diagonal up and left
                        if board[start_row -1][start_col -1].get_piece() is None:
                            return True
                        else:
                            return False
                    else: # Elephant moving to the diagonal down and left
                        if board[start_row + 1][start_col - 1].get_piece() is None:
                            return True
                        else:
                            return False

                # Elephant moving to the right
                else:
                    if end_row - start_row == -2: # Elephant moving diagonal up and right
                        if board[start_row -1][start_col + 1].get_piece() is None:
                            return True
                        else:
                            return False
                    else: # Elephant moving to the diagonal down and right
                        if board[start_row + 1][start_col + 1].get_piece() is None:
                            return True
                        else:
                            return False

            else:  # Elephant does not move diagonally two spaces
                return False

        else:  # If elephant is black
            if end_row <= 4:  # If elephant end_pos forces black elephant to cross river
                return False

            # Check elephant moves diagonally two spaces
            elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 2:

                # Elephant moving to the left
                if end_col - start_col == -2:
                    if end_row - start_row == -2:  # Elephant moving diagonal up and left
                        if board[start_row - 1][start_col - 1].get_piece() is None:
                            return True
                        else:
                            return False
                    else:  # Elephant moving to the diagonal down and left
                        if board[start_row + 1][start_col - 1].get_piece() is None:
                            return True
                        else:
                            return False

                # Elephant moving to the right
                else:
                    if end_row - start_row == -2:  # Elephant moving diagonal up and right
                        if board[start_row - 1][start_col + 1].get_piece() is None:
                            return True
                        else:
                            return False
                    else:  # Elephant moving to the diagonal down and right
                        if board[start_row + 1][start_col + 1].get_piece() is None:
                            return True
                        else:
                            return False

            else:  # Elephant does not move diagonally two spaces
                return False










class Horse(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Method that checks whether move is legal based on starting and ending position"""
        parsed_positions = self.parse_positions(start_pos, end_pos)

        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        #  For horizontal movements for the horse
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2:
            # For movement going left
            if end_col - start_col == -2:
                if board[start_row][start_col-1].get_piece() is None: # Checks if horse is blocked
                    return True
                else:
                    return False
            # For movement going right
            else:
                if board[start_row][start_col + 1].get_piece() is None: # Checks if horse is blocked
                    return True
                else:
                    return False

        # For vertical movement for the horse
        elif abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1:
            # For movement going down
            if end_row - start_row == 2:
                if board[start_row + 1][start_col].get_piece() is None:
                    return True
                else:
                    return False
            # For movement going up
            if end_row - start_row == -2:
                if board[start_row - 1][start_col].get_piece() is None:
                    return True
                else:
                    return False

        # Returns False if invalid end_pos for the horse
        else:
            return False


class Chariot(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Method that checks whether move is legal based on starting and ending position"""
        parsed_positions = self.parse_positions(start_pos, end_pos)
        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        if start_row != end_row and start_col != end_col:  # Moving non-orthogonally
            return False

        if start_row == end_row:  # Moving horizontally
            col_difference = end_col - start_col

            if col_difference > 0:  # Moving to the right of the board
                for col in range(start_col + 1, end_col):  # Checks if there is a piece between start_col and end_col
                    if board[start_row][col].get_piece() is not None:
                        return False
                # When there is no piece to impede path, check if position is empty or piece is enemy piece
                if end_piece_player_id is None or start_piece.get_player_id() != end_piece_player_id:
                    return True

            if col_difference < 0:  # Moving to the left of the board
                for col in range(start_col - 1, end_col, -1): # Checks to the left of the board
                    # If there is a piece to block movement to the end_pos, return False
                    if board[start_row][col].get_piece() is not None:
                        return False
                if end_piece_player_id is None or start_piece.get_player_id() != end_piece_player_id:
                    return True

        if start_col == end_col:  # Moving verticially
            row_difference = end_row - start_row

            if row_difference > 0:  # Moving down the board
                for row in range(start_row + 1, end_row):
                    if board[row][start_col].get_piece() is not None:  # If no piece is impeding path to end_pos
                        return False
                # Checks if end_pos is empty or an enemy piece is on end_pos
                if end_piece_player_id is None or start_piece.get_player_id() != end_piece_player_id:
                    return True

            if row_difference < 0:
                for row in range(start_row -1, end_row, -1):
                    if board[row][start_col].get_piece() is not None:  # If no piece is impeding path to end_pos
                        return False
                    # Checks if end_pos is empty or an enemy piece is on end_pos
                if end_piece_player_id is None or start_piece.get_player_id() != end_piece_player_id:
                    return True





class Cannon(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Method that checks whether move is legal based on starting and ending position"""
        parsed_positions = self.parse_positions(start_pos, end_pos)

        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]
        count = 0  # Count will track how many pieces are between start and end_pos

        if start_row != end_row and start_col != end_col:  # Moving diagonally
            return False

        # If cannon moves to an empty position
        # if end_piece_player_id is None:

        if start_row == end_row:  # Moving horizontally
            col_difference = end_col - start_col

            if col_difference > 0:  # Moving to the right of the board
                for col in range(start_col + 1, end_col):  # Checks if there is a piece between start_col and end_col
                    if board[start_row][col].get_piece() is not None:
                        count += 1

            if col_difference < 0:  # Moving to the left of the board
                for col in range(start_col - 1, end_col, -1): # Checks to the left of the board
                    # If there is a piece to block movement to the end_pos, return False
                    if board[start_row][col].get_piece() is not None:
                        count += 1

        if start_col == end_col:  # Moving vertically
            row_difference = end_row - start_row

            if row_difference > 0:  # Moving down the board
                for row in range(start_row + 1, end_row):
                    if board[row][start_col].get_piece() is not None:  # If no piece is impeding path to end_pos
                        count += 1


            if row_difference < 0:  # Moving up the board
                for row in range(start_row -1, end_row, -1):
                    if board[row][start_col].get_piece() is not None:  # If no piece is impeding path to end_pos
                        count += 1

        # 1 piece between start_pos and end_pos and end_pos contains a chess piece
        if count == 1 and end_piece_player_id is not None:
            return True
        # end_pos has no piece and there are no pieces to impede path
        elif end_piece_player_id is None and count == 0:
            return True
        # Returns False for all other scenarios
        else:
            return False

class Soldier(Pieces):

    def is_legal_move(self, start_pos, end_pos, start_piece, end_piece_player_id, board):
        """Method that checks whether move is legal based on starting and ending position"""
        parsed_positions = self.parse_positions(start_pos, end_pos)
        start_row = parsed_positions[0]
        start_col = parsed_positions[1]
        end_row = parsed_positions[2]
        end_col = parsed_positions[3]

        # Case for Red
        if start_piece.get_player_id() == 'r':

            # Red soldier hasn't crossed river
            if 3 <= start_row <= 4:
                if end_row - start_row == 1 and start_col == end_col:
                    return True

            # Red solider has crossed river
            else:
                # Checks if movement forces a diagonal
                if end_row - start_row == 1 and abs(end_col - start_col) == 1:
                    return False
                # Rules out the diagonal and checks if movement is valid
                elif end_row - start_row == 1 or abs(end_col - start_col) == 1:
                    return True
                else:
                    return False

        # Case for Black
        else:
            # Black soldier hasn't crossed river
            if 5 <= start_row <= 6:
                if end_row - start_row == -1 and start_col == end_col:
                    return True
                else:
                    return False

            # Black soldier has crossed the river
            else:
                # Checks if movement forces a diagonal
                if end_row - start_row == -1 and abs(end_col - start_col) == 1:
                    return False
                # Rules out the diagonal and checks if movement is valid
                elif end_row - start_row == -1 or abs(end_col - start_col) == 1:
                    return True

                else:
                    return False

def main():
    game = XiangqiGame()

if __name__ == "__main__":
    main()

