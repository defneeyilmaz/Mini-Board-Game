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

    def position_conversion(self, matrix):
        position = int((matrix[0] * 3) + matrix[1] + 1)
        return position

    def matrix_conversion(self, position):
        row = (int(position) - 1) // 3
        col = (int(position) - 1) % 3
        return row, col

    def set_state(self, positions):
        tile = 1
        for x in positions:
            matrix_form = self.matrix_conversion(x)
            self.board.set_initial_tile_position(tile, (matrix_form[0], matrix_form[1]))
            tile += 1
        self.initial_state = positions

    def set_goal_state(self, positions):
        tile = 1
        for x in positions:
            matrix_form = self.matrix_conversion(x)
            self.board.set_goal_tile_position(tile, (matrix_form[0], matrix_form[1]))
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
        #print(self.board.tiles[0].initial_position)

        print("Now, set the goal state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)

        g_positions = [input(), input(), input()]
        g_positions = self.check_position(g_positions)
        self.set_goal_state(g_positions)
        #print(self.goal_state)
        #print(self.board.tiles[0].goal_position)
        self.moving_tiles_astar()

    def manhattan_distance(self, goal_position, next_tile_position):
        return abs(int(goal_position[0]) - int(next_tile_position[0])) + abs(int(goal_position[1]) - int(next_tile_position[1]))
        #h_cost = self.manhattan_distance((row ,col), next_tile)

    def get_step_cost(self, tile, next_tile):
        if not tile.initial_position[0] == next_tile[0]:
            return 2
        elif not tile.initial_position[1] == next_tile[1]:
            return 1

    def possible_moves(self, tile):
        row, col = tile.initial_position
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for i, j in possible_moves:
            new_row, new_col = row + i, col + j

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                next_tile = (new_row, new_col)

                step_cost = self.get_step_cost(tile, next_tile)
                h_cost = self.manhattan_distance(tile.goal_position, next_tile)
                total_cost = tile.cost + step_cost + h_cost

                tile.fringe.append((str(self.position_conversion(next_tile)),total_cost))

    def moving_tiles_astar(self):
        max_step = 10
        tile_order = [1, 2, 3]
        current_step = 0

        while current_step < max_step:
            for tile_number in tile_order:
                if current_step >= max_step:
                    break

                tile = self.board.tiles[tile_number - 1]

                if tile.initial_position == tile.goal_position:
                    tile_order.remove(tile_number)
                    continue

                self.possible_moves(tile)
                least_cost_path = min(tile.fringe, key=lambda x: x[1])
                tile.expansion_order.append(least_cost_path[0])
                tile.initial_position = self.matrix_conversion(least_cost_path[0])
                tile.fringe.remove(least_cost_path)

                current_step += 1

                if self.board.is_goal_state():
                    print("Goal state reached!")
                    return True

                #if there is a tile in the position it is trying to move to, it won't proceed
                #fringe, expansion order print

        print("Goal state not reached within 10 steps.")
        return False