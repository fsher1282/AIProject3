

class MinMax:
    def __init__(self, matrix, move):
        self.matrix = matrix
        self.move = move

    def is_won(self):
        if len(self.o_pieces) == 0:
            return True
        else:
            return False

    def maxMove(self):
        minmax_result = self.calculate_min_max(self.matrix)
        start_pos = minmax_result[0]
        highest_weight = minmax_result[1]
        best_move = minmax_result[2]
        return start_pos, best_move

    def minMove(self):
        minmax_result = self.calculate_min_max(self.matrix)
        start_pos = minmax_result[0]
        lowest_weight = minmax_result[3]
        worst_move = minmax_result[4]
        return start_pos, worst_move


    def calculate_min_max(self,moves_list):  # Calculates the weight of the best move
        starting_pos = None
        best_branch_weight = 0
        best_branch = []
        worst_branch_weight = 20
        worst_branch = []
        #print("here they are")
        for move in range(0, len(moves_list)):  # for every potential move
            a_move = moves_list[move]
            value = a_move[0]
            this_starting_pos = a_move[1]  # Sets starting position to first item in list
            adj_options = a_move[2]  # Sets adjacent options to 2nd item in list
            jump_options = a_move[3]  # Sets jump options to 3rd item in list
            if jump_options[0][0]:  # If there are any jump opportunities
                print('jump')
                for branch in range(0, len(jump_options)):
                    a_branch = jump_options[branch]
                    this_branch_weight = self.assign_weight_for_branch(a_branch)
                    if this_branch_weight > best_branch_weight and a_branch:
                        best_branch_weight = this_branch_weight
                        best_branch = a_branch
                        starting_pos = this_starting_pos

                    elif this_branch_weight < worst_branch_weight and a_branch and this_branch_weight > 0:
                        starting_pos = this_starting_pos
                        worst_branch_weight = this_branch_weight
                        worst_branch = a_branch

            if adj_options:  # If there are any adjacent move opportunities

                for option in range(0, len(adj_options)):

                    adj_weight = self.assign_weight_for_adjacent(adj_options[option])
                    if adj_weight > best_branch_weight:
                        starting_pos = this_starting_pos
                        best_branch_weight = adj_weight
                        best_branch = [adj_options[option]]
                    elif adj_weight < worst_branch_weight and worst_branch_weight > 0:
                        starting_pos = this_starting_pos
                        worst_branch_weight = adj_weight
                        worst_branch = adj_options[option]
            else:
                print("")
        return starting_pos, best_branch_weight, best_branch, worst_branch_weight, worst_branch

    def assign_weight_for_branch(self, branch):
        branch_length = len(branch)
        if branch_length > 4:
            return 20
        elif branch_length > 3:
            return 17
        elif branch_length > 2:
            return 14
        elif branch_length > 1:
            return 11
        elif branch_length > 0:  # Branch length of 1
            return 8
        else:
            return 0

    def assign_weight_for_adjacent(self, adj_location):  # Need to work out how we want to assign weights to functions
        return 5

    def make_move(self, player):  # TODO needs to be remade into a class method
        potential_move = None
        if player == "x" or player == 'X':
            potential_move = self.maxMove()
        if player == 'o' or player == 'O':
            potential_move = self.minMove()
        self.move.move_piece(player, potential_move[0], potential_move[1])





