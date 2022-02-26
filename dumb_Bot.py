import random as rand


# Method to check if piece is on board
def is_on_board(point):
    row = point[0]
    col = point[1]
    return 1 <= row < 9 and \
           1 <= col < 9


def display_matrix(move_matrix):
    for i in move_matrix:
        print(i)


class DumbBot:
    def __init__(self):
        self.x_locations = []  # tracks all positions of x pieces
        self.o_locations = []  # tracks all positions of o pieces
        self.all_valid_moves = []  # List will return all moves player/bot can make
        self.piece = None
        self.normal_moves = []
        self.all_jump_moves = []
        self.kings = []

    # Searches board for all pieces and appends them to locations list
    def dumb_helper(self, present_board):
        for y, row in enumerate(present_board):
            for x, col in enumerate(row):
                if col == 'x' or col == 'X':
                    self.x_locations.append([x, y])

                if col == 'o' or col == 'O':
                    self.o_locations.append([x, y])

                # Appends kings into separate list
                if col == 'X' or col == 'O':
                    self.kings.append([x, y])

        return [self.x_locations, self.o_locations]

    def select_piece(self, decision):
        if not decision:
            return False

        index = rand.randint(0, len(decision) - 1)
        self.piece = decision[index]
        return self.piece

    # Returns what type a selected piece is
    def get_piece_type(self, piece):
        piece_type = ''
        if piece in self.o_locations and piece in self.kings:
            piece_type = 'O'
        elif piece in self.x_locations and piece in self.kings:
            piece_type = 'X'
        elif piece in self.x_locations and piece not in self.kings:
            piece_type = 'x'
        elif piece in self.o_locations and piece not in self.kings:
            piece_type = 'o'

        return piece_type

    def add_to_list(self, viable_moves):
        if viable_moves is not None:
            for i in viable_moves:
                self.all_valid_moves.append(i)

    # Function calculates movement for all pieces
    def valid_ai_move(self, selected_piece, piece_type):
        self.piece = selected_piece

        if piece_type == 'x' or self.piece in self.kings:
            if self.piece[0] == 1 and self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] + 1, self.piece[1] + 1])

            elif self.piece[0] == 8 and self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] - 1, self.piece[1] + 1])

            elif 2 <= self.piece[0] < 8 and 0 < self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] + 1, self.piece[1] + 1])
                self.normal_moves.append([self.piece[0] - 1, self.piece[1] + 1])

        if piece_type == 'o' or self.piece in self.kings:
            if self.piece[0] == 1 and self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] + 1, self.piece[1] - 1])

            elif self.piece[0] == 8 and self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] - 1, self.piece[1] - 1])

            elif 2 <= self.piece[0] < 8 and 0 < self.piece[1] < 8:
                self.normal_moves.append([self.piece[0] + 1, self.piece[1] - 1])
                self.normal_moves.append([self.piece[0] - 1, self.piece[1] - 1])

        return self.normal_moves

    # Checks to see if any moves calculated are valid
    def check_spots(self, moves):
        self.normal_moves = moves

        for i in self.normal_moves[:]:
            if i in self.o_locations:
                self.normal_moves.remove(i)
                continue

            elif i in self.x_locations:
                self.normal_moves.remove(i)
                continue

            elif is_on_board(i) is False:
                self.normal_moves.remove(i)
                continue

        self.add_to_list(self.normal_moves)
        return self.normal_moves

    # Remove invalid jump points and append valid ones to self.all_jump_moves
    def check_jumps(self, potential_jumps):
        jumps = potential_jumps
        for i in jumps[:]:
            print(jumps)
            if i in self.o_locations:
                jumps.remove(i)

            elif i in self.x_locations:
                jumps.remove(i)

            elif is_on_board(i) is False:
                jumps.remove(i)
                break

            else:
                self.all_jump_moves.append(i)

        return jumps

    # Function recursively calculates all jumps a piece can make based on location
    def calc_jumps(self, pieces, piece_type):
        jumps = []
        taken_spots = [self.o_locations, self.x_locations]
        for piece in pieces:
            # Neighbor Points
            p1 = [piece[0] - 1, piece[1] - 1]
            p2 = [piece[0] + 1, piece[1] - 1]
            p3 = [piece[0] - 1, piece[1] + 1]
            p4 = [piece[0] + 1, piece[1] + 1]

            # Jump position coordinates
            jump_up_left = [piece[0] - 2, piece[1] - 2]
            jump_up_right = [piece[0] + 2, piece[1] - 2]
            jump_down_left = [piece[0] - 2, piece[1] + 2]
            jump_down_right = [piece[0] + 2, piece[1] + 2]

            # All possible reasons to end the loop
            if is_on_board(piece) is False:
                break

            elif piece_type in self.kings == False:
                if is_on_board(jump_down_left) is False and \
                        is_on_board(jump_down_right) is False:
                    break

                elif is_on_board(jump_up_left) is False and \
                        is_on_board(jump_up_right) is False:
                    break


            elif jump_down_left in taken_spots \
                    and jump_down_right in taken_spots:
                break

            elif jump_up_left in taken_spots \
                    and jump_up_right in taken_spots:
                break

            elif jump_up_left in taken_spots \
                    and jump_up_right in taken_spots \
                    and jump_down_left in taken_spots \
                    and jump_down_right in taken_spots:
                break

            elif jump_up_left in jumps \
                    or jump_up_right in jumps:
                break

            # Calculate jumps w/ 'x' piece
            elif piece_type == 'x':

                if p3 in self.o_locations:
                    jumps.append(jump_down_left)

                if p4 in self.o_locations:
                    jumps.append(jump_down_right)

                checked_jumps = self.check_jumps(jumps)  # Remove invalid jump points
                self.calc_jumps(checked_jumps, 'x')  # Recursive call

            # Calculate jumps w/ 'o' piece
            elif piece_type == 'o':

                if p1 in self.x_locations:
                    jumps.append(jump_up_left)

                if p2 in self.x_locations:
                    jumps.append(jump_up_right)

                checked_jumps = self.check_jumps(jumps)
                self.calc_jumps(checked_jumps, 'o')

            # Calculate jumps w/ 'X' piece
            elif piece_type == 'X':
                if p1 in self.o_locations:
                    jumps.append(jump_up_left)

                if p2 in self.o_locations:
                    jumps.append(jump_up_right)

                if p3 in self.o_locations:
                    jumps.append(jump_down_left)

                if p4 in self.o_locations:
                    jumps.append(jump_down_right)

                checked_jumps = self.check_jumps(jumps)  # Remove invalid jump points
                self.calc_jumps(checked_jumps, 'X')  # Recursive call

            # Calculate jumps w/ 'O' piece
            elif piece_type == 'O':
                if p1 in self.x_locations:
                    jumps.append(jump_up_left)

                if p2 in self.x_locations:
                    jumps.append(jump_up_right)

                if p3 in self.x_locations:
                    jumps.append(jump_down_left)

                if p4 in self.x_locations:
                    jumps.append(jump_down_right)

                checked_jumps = self.check_jumps(jumps)  # Remove invalid jumps
                self.calc_jumps(checked_jumps, 'O')  # Recursive call

        return self.all_jump_moves

    # When calculating jumps this separates each jump path into different sub-lists
    def format_jump_path(self):
        jumps = self.all_jump_moves
        i = 0
        while i < len(self.all_jump_moves) - 1:
            if self.all_jump_moves[i][0] == self.all_jump_moves[i + 1][0] or \
                    self.all_jump_moves[i][1] == self.all_jump_moves[i + 1][1]:
                jumps = [self.all_jump_moves[0::2], self.all_jump_moves[1::3]]

            i += 1

        return jumps

    # Puts all pieces that can move into a list structured as old_piece, single_moves, jumps
    def return_all_moves(self, piece_type, old_pieces, normal_moves, jumps):
        all_valid_moves = []

        if len(normal_moves) > 0 and len(jumps) > 0:
            all_valid_moves.append(piece_type)
            all_valid_moves.append(old_pieces)
            all_valid_moves.append([normal_moves])
            all_valid_moves.append([[jumps]])

        elif len(normal_moves) > 0 and len(jumps) == 0:
            all_valid_moves.append(piece_type)
            all_valid_moves.append(old_pieces)
            all_valid_moves.append(normal_moves)
            all_valid_moves.append([[jumps]])

        elif len(jumps) > 0:
            all_valid_moves.append(piece_type)
            all_valid_moves.append(old_pieces)
            all_valid_moves.append([normal_moves])
            all_valid_moves.append([jumps])

        return all_valid_moves

    # Iterates through all pieces to find all moves/jumps
    def game_matrix(self, checker_board, team):

        current_board = self.dumb_helper(checker_board)
        pieces = None

        self.x_locations = []
        self.o_locations = []
        self.x_locations = current_board[0]
        self.o_locations = current_board[1]

        move_matrix = []

        if team == 'x':
            pieces = self.x_locations
        elif team == 'o':
            pieces = self.o_locations

        for i in pieces:
            self.normal_moves = []
            self.all_jump_moves = []
            self.all_valid_moves = []
            self.normal_moves = []
            self.all_jump_moves = []
            self.piece = i
            piece_type = self.get_piece_type(i)
            moves = self.valid_ai_move(i, piece_type)
            normal_moves = self.check_spots(moves)
            self.calc_jumps([i], piece_type)
            jumps = self.format_jump_path()

            if len(jumps) > 1:
                for index in jumps:
                    new_k = []
                    for elem in index:
                        if elem not in new_k:
                            new_k.append(elem)
                    jumps = new_k

                    all_moves = self.return_all_moves(piece_type, i, normal_moves, jumps)
                    move_matrix.append(all_moves)
            else:
                all_moves = self.return_all_moves(piece_type, i, normal_moves, jumps)

                if len(all_moves) > 0:
                    move_matrix.append(all_moves)
                else:
                    continue

        return move_matrix
