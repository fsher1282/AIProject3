
class Board:
    def __init__(self):
        self.dimensions = 9
        self.grid = []

    def is_on_board(self, row, col):
        return 1 <= row < self.dimensions and \
            1 <= col < self.dimensions

    # Generates new board
    def generate_board(self):
        # Create player board
        x_label = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for player_row in range(self.dimensions):
            self.grid.append([])

            for i, player_col in enumerate(range(self.dimensions)):
                if player_col == 0:
                    self.grid[player_row].append(str(i + player_row))
                    self.grid[player_col] = x_label

                elif player_row == 0:
                    break

                else:
                    self.grid[player_row].append('.')   # Creates board full of blank spots


        # Creates pieces in starting positions
        for col in range(self.dimensions):
            for row in range(self.dimensions):
                if (row + col) % 2 == 1:  # if spot is technically accessible
                    if 0 < row < 4 and col > 0:  # Initializes x for top of board
                        self.grid[row][col] = 'x'
                    if row > 5 and col > 0:  # Initializes o for bottom of board
                        self.grid[row][col] = 'o'

    # Print player board
    def print_player_board(self):
        for player_row in self.grid:
            print(" ".join(player_row))


