import board
import dumb_Bot as db
import move
import min_max


class Bot:

    def __init__(self, color):
        self.color = color
        self.dumb_bot = db.DumbBot()
        self.board = board.Board()
        self.board.generate_board()
        self.move = move.Move(self.board.grid)
        self.matrix = self.dumb_bot.game_matrix(self.board.grid, 'x')
        self.min_max = min_max.MinMax(self.matrix, self.move)

    def make_move(self):
        """
        Returns a tuple. The first is the coordinates for the piece that's moving.
        The second item is an array that contains the positions it
        ends up in or the steps in a multiple jump. All coordinates are in a string
        format "AxB" where A is the x coordinate and B is the Y coordinate.

        for a piece at (2,3) jumping to (4,5) and then (2,7)
            it should return ("2x3", ["4x5", "2x7"])
        """
        self.dumb_bot.o_locations = []
        self.dumb_bot.x_locations = []
        self.dumb_bot.kings = []
        self.matrix = self.dumb_bot.game_matrix(self.board.grid, 'x')
        print(self.matrix)
        self.min_max = min_max.MinMax(self.matrix, self.move)
        piece = self.min_max.maxMove()[0]
        pieceType = self.dumb_bot.get_piece_type(piece)
        print(pieceType)
        self.min_max.make_move(pieceType)
        return self.min_max.maxMove()

    def receive_move(self, move):
        """
        Receives a move from the other bot and applies it to
        to its own gamestate. The move is in the same format that makemove sends in.

        If it receives an invalid move, it returns False.

        Else, it returns true.
        """
        mv = move

        self.move.move_piece('o', mv[0], mv[1])

    def get_board_str(self):
        """
        returns a string representing the board. You can do this however you want,
        as long as it makes sense.
        """
        return self.board.print_player_board()

