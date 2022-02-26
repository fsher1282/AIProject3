import bot
adaption = {'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8}


def input_adapter(coordinate):
    for i in coordinate[0].split():
        new = [adaption[i], int(coordinate[1])]
        return new


# Theo did the main
if __name__ == '__main__':
    print("yea boi")
    game = bot.Bot('None')
    playing = True
    while playing:

        if len(game.dumb_bot.o_locations) == 0 or len(game.dumb_bot.x_locations) == 0:
            playing = False
            break

        game.get_board_str()

        initial_coords_list = []
        print('Example of a coordinate is A6')
        item = input("Enter coordinate you'd like to move for O: ")

        x = input_adapter(item)
        initial_coords_list.append(x)
        print(initial_coords_list)

        moved_coords_list = []
        jumps = True

        print('Example: B5, D7')
        item = input("Enter the coordinate of where to move O: ")
        y = input_adapter(item)
        moved_coords_list.append(y)
        print(moved_coords_list)

        player_move = (x, moved_coords_list)
        print(player_move)
        game.get_board_str()

        game.receive_move(player_move)
        game.get_board_str()
        print(game.make_move())
        game.get_board_str()


print('gg')
