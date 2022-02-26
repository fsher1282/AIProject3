# Luke created the movement system
class Move:
    def __init__(self, grid):
        self.x_direction = 'down'
        self.o_direction = 'up'
        self.grid = grid
        print("new grid is: " + str(self.grid))

    def is_on_board(self, row, col):
        return 1 <= row < 9 and \
            1 <= col < 9

# Returns point at given row and column value
    def get_point(self, row, col):
        return self.grid[row][col]

    def point_available(self, row, col):
        if self.get_point(row, col) == '.' and (row + col) % 2 == 1: # If point is empty and is valid
            return True
        else:
            return False

    def set_point(self, row, col, value):
        self.grid[row][col] = value

    def move_piece(self, player_value, old_coordinate, new_coordinate):  # Moves piece from previous location
        old_row = old_coordinate[1]
        old_col = old_coordinate[0]
        new_coordinate = new_coordinate[0]
        print(new_coordinate)
        if any(isinstance(el, list) for el in new_coordinate):
            new_row = new_coordinate[0][1]
            new_col = new_coordinate[0][0]
        else:
            new_row = new_coordinate[1]
            new_col = new_coordinate[0]

        direction = self.get_direction(old_row, old_col)
        # If move is in correct direction and new point is available

        if self.in_correct_direction(direction, old_row, new_row) and self.point_available(new_row, new_col):
            # If new point is a neighbor of old point
            if self.is_neighbor(old_row, old_col, new_row, new_col):
                self.set_point(new_row, new_col, self.get_point(old_row, old_col))  # Put value of old spot into new spot
                self.set_point(old_row, old_col, '.')    # replace value of old spot with .
                self.make_king(new_row, new_col)
                print('made move')


            # If new point is reachable by a single jump
            elif self.is_jumpable(player_value, old_row, old_col, new_row, new_col):
                self.set_point(new_row, new_col, self.get_point(old_row, old_col))  # Put value of old spot into new spot
                self.set_point(old_row, old_col, '.')  # replace value of old spot with .
                self.make_king(new_row, new_col)
                if any(isinstance(el, list) for el in new_coordinate):
                    for i in range(1, len(new_coordinate)):
                        old_row = new_coordinate[i-1][1]
                        old_col = new_coordinate[i-1][0]

                        new_row = new_coordinate[i][1]
                        new_col = new_coordinate[i][0]
                        self.is_jumpable(player_value,old_row,old_col,new_row,new_col)
                        self.set_point(new_row, new_col,
                                       self.get_point(old_row, old_col))  # Put value of old spot into new spot
                        self.set_point(old_row, old_col, '.')  # replace value of old spot with .
                        self.make_king(new_row, new_col)

                return


            else:
                print("Moving a piece here is not permitted")
                return

        else:
               # piece cannot move in that direction
            print("Piece cannot move in that direction")
            return
    def make_king(self, new_row, new_col): # Makes piece into a king if it needs to be made into king
        if self.get_direction(new_row, new_col) == "down":
            if new_row == 8:
                self.set_point(new_row, new_col, "X")
        if self.get_direction(new_row, new_col) == "up":
            if new_row == 1:
                self.set_point(new_row, new_col, "O")

    def neighbor_points(self, row, col):    # Determines the direct neighbors to a given point may move to.
        p1 = (row - 1, col - 1)
        p2 = (row - 1, col + 1)
        p3 = (row + 1, col - 1)
        p4 = (row + 1, col + 1)
        points = [p1, p2, p3, p4]
        neighbor_points = []

        for point in points:
            if self.is_on_board(point[0], point[1]):
                neighbor_points.append(point)
            elif not self.is_on_board(point[0], point[1]):
                neighbor_points.append(None)
        # Must account for points that are jump points
        return neighbor_points

    # Returns true if point is a neighbor, false if not a neighbor
    def is_neighbor(self, old_row, old_col, new_row, new_col):
        t1 = (new_row, new_col)
        if t1 in self.neighbor_points(old_row, old_col):    # If the spot is a neighboring point
            return True
        else:
            return False

    def get_direction(self, row, col):
        if self.grid[row][col] == 'x':
            return self.x_direction
        if self.grid[row][col] == 'o':
            return self.o_direction
        else:
            return None

    def in_correct_direction(self, direction, old_row, new_row):
        if direction == 'down' and old_row - new_row < 0:
            return True
        if direction == 'up' and old_row - new_row > 0:
            return True
        if direction == None:
            return True
        else:
            return False

    def is_jumpable(self, player_value, old_row, old_col, new_row, new_col):
        # todo implement player to check if neighbor is an enemy piece
        jump_direction = self.get_jump_direction(old_row, old_col, new_row, new_col)  # Find direction of jump neighbor

        # If the neighbor
        # Find direct neighbor in the same direction
        direct_neighbor = self.neighbor_points(old_row, old_col)[jump_direction]

        if direct_neighbor is not "." and direct_neighbor is not player_value:  # if the piece to be jumped is an enemy
            self.remove_piece(direct_neighbor[0], direct_neighbor[1])  # Remove the jumped piece
            return True
        else:
            return False

    def get_jump_direction(self, old_row, old_col, new_row, new_col):
        # 0 == up left, 1 == up right, 2 == down left, 3 == down right
        if old_row - new_row < 0:  # Down
            if old_col - new_col < 0:  # Right
                return 3
            elif old_col - new_col > 0:  # Left
                return 2
        elif old_row - new_row > 0:  # Up
            if old_col - new_col < 0:  # Right
                return 1
            elif old_col - new_col > 0:     # Left
                return 0

    def remove_piece(self, row, col):
        self.grid[row][col] = '.'
