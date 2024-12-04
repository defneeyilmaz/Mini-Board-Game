from Board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.initial_state = None
        self.goal_state = None

    def check_position(self, position):
        while not self.check_state(position):
            print("Please enter valid positions.\n")
            position = [input(), input(), input()]
        return position

    def check_state(self, positions):
        if not len(positions) == 3:
            return False
        elif not len(set(positions)) == len(positions):
            return False
        for x in positions:
            try:
                if not (1 <= int(x) <= 9):
                    return False
            except ValueError:
                return False
        return True

    def set_state(self, positions):
        tile = 1
        for x in positions:
            row = (int(x)-1) // 3
            col = (int(x)-1) % 3
            self.board.set_initial_tile_position(tile, (int(row), int(col)))
            tile += 1
        self.goal_state = positions

    def set_goal_state(self, positions):
        tile = 1
        for x in positions:
            row = (int(x) - 1) // 3
            col = (int(x) - 1) % 3
            self.board.set_goal_tile_position(tile, (int(row), int(col)))
            tile += 1
        self.goal_state = positions

    def begins(self):
        print("\nWelcome to the mini board game!")
        print("You need to set the initial and goal states to start the game.\n")
        print("Set the initial state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)

        i_positions = [input(), input(), input()]
        i_positions = self.check_position(i_positions)
        self.set_state(i_positions)
        Board.print_board(self.board)

        print("Now, set the goal state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)

        g_positions = [input(), input(), input()]
        g_positions = self.check_position(g_positions)
        self.set_goal_state(g_positions)

    def manhattan_distance(self, tile):
        return (abs(tile.initial_position[0] - tile.goal_position[0]) +
                abs(tile.initial_position[1] - tile.goal_position[1]))

    def get_neighbors(self,tile):
        vertical_neighbors = []
        vertical_neighbors.append(tile.initial_position[1]-1)
        horizontal_neighbors = []

    #def move_tile_astar(self,tile):
        #manhattan distance
        #get_neighbours
        #move tile and update its cost

    def moving_tiles(self):
        max_step = 10
        tile_order = [1, 2, 3]
        current_step = 0

        while current_step < max_step:
            for tile_number in tile_order:
                if current_step >= max_step:
                    break

                tile = self.board.tiles[tile_number - 1]
                goal_position = tile.goal_position

                if tile.initial_position == goal_position:
                    tile_order.remove(tile_number)
                    continue

                #self.board.move_tile_astar(tile)

                current_step += 1

                if self.board.is_goal_state():
                    print("Goal state reached!")
                    return True

        print("Goal state not reached within 10 steps.")
        return False