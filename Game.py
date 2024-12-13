from Board import Board
from Tile import Tile
from Node import Node

class Game:
    def __init__(self):
        self.board = Board()
        self.initial_state = None
        self.goal_state = None
        self.root_node = None
        self.temp_node = None
        self.expansion_order = []
        self.fringe = [[] for _ in range(3)]
        self.max_step = 10
        self.current_step = 0

    def print_expanded_node(self, node):
        board = [['_' for _ in range(3)] for _ in range(3)]
        for x in range(3):
            row, col = self.matrix_conversion(node.state[x])
            board[row][col] = str(x+1)
        for row in board:
            print(" ".join(row))

    def show_expansions(self):
        return "-".join(str(x) for x in self.expansion_order)

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
        print()

        i_positions = [input(), input(), input()]
        i_positions = self.check_position(i_positions)
        self.set_state(i_positions)
        print("\nInitial state:")
        Board.print_board(self.board, "current")

        print("Now, set the goal state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)
        print()

        g_positions = [input(), input(), input()]
        g_positions = self.check_position(g_positions)
        self.set_goal_state(g_positions)
        self.root_node = Node(i_positions, 0, None, None)

        # Wrap heuristic values in lists
        heuristics = self.heuristic_distances(i_positions, g_positions)
        self.root_node.heuristic = [[h] for h in heuristics]  # Fix here
        self.temp_node = self.root_node

        print("\nGoal state:")
        Board.print_board(self.board, "goal")
        self.moving_tiles_astar()

    def get_occupied_positions(self, tile):
        positions = []
        tiles = [1,2,3]
        tiles.remove(tile.value)
        for x in tiles:
            positions.append(self.board.tiles[x-1].initial_position)
        return positions

    def manhattan_distance(self, goal_position, next_tile_position):
        return abs(int(goal_position[0]) - int(next_tile_position[0])) + abs(int(goal_position[1]) - int(next_tile_position[1]))

    def heuristic_distances(self, initials, goals):
        heuristics = []
        for x in range(3):
            i = self.matrix_conversion(initials[x])
            g = self.matrix_conversion(goals[x])
            heuristics.append(abs(int(g[0]) - int(i[0])) + abs(int(g[1]) - int(i[1])))
        return heuristics

    def get_step_cost(self, tile, next_tile):
        if tile.initial_position[0] != next_tile[0]:
            return 1
        elif tile.initial_position[1] != next_tile[1]:
            return 2

    def is_initial_goal(self, initials, goals):
        if initials == goals:
            return True

    def possible_moves(self, tile):
        row, col = tile.initial_position
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        occupied_positions = self.get_occupied_positions(tile)
        moves = []

        for i, j in possible_moves:
            new_row, new_col = row + i, col + j
            next_tile = (new_row, new_col)

            # Skip if the next position is out of bounds or occupied
            if 0 <= new_row < 3 and 0 <= new_col < 3 and next_tile not in occupied_positions and next_tile != tile.initial_position:
                step_cost = self.get_step_cost(tile, next_tile)
                h_cost = self.manhattan_distance(tile.goal_position, next_tile)
                total_cost = self.temp_node.cost[int(tile.value) - 1][0] + step_cost + h_cost

                positions = self.initial_state[:]
                positions[int(tile.value) - 1] = str(self.position_conversion(next_tile))
                node = Node(positions, self.temp_node.get_depth() + 1, self.temp_node, tile.value)

                # Copy heuristic structure properly
                node.heuristic = [h[:] for h in self.temp_node.heuristic]  # Fix here
                node.heuristic[int(tile.value) - 1][0] = h_cost
                node.total_cost[int(tile.value) - 1][0] = total_cost

                moves.append((node, total_cost, step_cost))

        moves.sort(key=lambda x: (
            x[1], self.manhattan_distance(tile.goal_position, self.matrix_conversion(int(x[0].state[tile.value - 1])))))

        for move in moves:
            self.fringe[tile.value - 1].append(move)

        return len(moves), tile.value

    def moving_tiles_astar(self):
        tile_order = [1, 2, 3]
        visited_positions = {1: set(), 2: set(), 3: set()}  # Track visited positions for each tile
        visited_states = set()  # Track the entire board state to avoid revisiting
        progress_made = False

        self.expansion_order.append(self.temp_node.state)
        print("\n-------Expansion " + str(self.current_step + 1) + "-------\n")
        print("Expanded Node:")
        Board.print_board(self.board, "current")
        self.current_step += 1

        if self.is_initial_goal(self.initial_state, self.goal_state):
            print("\nThe initial board state is the goal state!")
            print("Total cost --> 0")
            progress_made = True
        else:
            while self.current_step < self.max_step:

                for tile_number in tile_order:
                    if self.current_step >= self.max_step:
                        break

                    tile = self.board.tiles[tile_number - 1]

                    # Skip tiles already in their goal position
                    if tile.initial_position == tile.goal_position:
                        continue

                    # Attempt to move the tile
                    possible_move, tile_value = self.possible_moves(tile)

                    if possible_move > 0:
                        #or current tile's fringe is not empty
                        print("\n-------Expansion "+str(self.current_step+1)+"-------\n")
                        # Find the least cost path from the fringe
                        least_cost_path = min(self.fringe[tile_number-1], key=lambda x: x[1])
                        self.fringe[tile_number-1].remove(least_cost_path)
                        self.temp_node = least_cost_path[0]

                        new_position = least_cost_path[0].state[tile_number - 1]
                        state_tuple = tuple(least_cost_path[0].state)

                        # Check if the position or state has already been visited
                        if state_tuple in visited_states:
                            continue  # Skip already visited states

                        visited_states.add(state_tuple)  # Add the new state to visited states
                        visited_positions[tile.value].add(new_position)  # Track the position of the tile

                        # Update the tile's position
                        tile.initial_position = self.matrix_conversion(new_position)

                        print(f"Tile #{tile_value} is moving to position {new_position}")
                        print(f"Current path cost for played tile is --> {least_cost_path[2]}")
                        print(f"Current cost(heuristic and position cost) of the state is --> {least_cost_path[1]}")
                        heuristic_sum = 0
                        for heuristic in self.temp_node.heuristic:
                            heuristic_sum+=heuristic[0]
                        print(f"Current heuristic for this state is --> {heuristic_sum}")
                        self.expansion_order.append(least_cost_path[0])
                        print("\nExpanded Node:")
                        self.print_expanded_node(least_cost_path[0])
                        self.set_state(least_cost_path[0].state)

                        progress_made = True
                    else:
                        print(f"Tile {tile.value} cannot make any moves at the moment.")

                    # Check if the board is in the goal state
                    if self.board.is_goal_state():
                        print("Goal state reached!")
                        return True

                    self.current_step += 1

                # If no progress is made, break the loop
                if not progress_made:
                    print("No progress made. Breaking loop.")
                    break
            print("Goal state not reached within 10 steps.")
            return False