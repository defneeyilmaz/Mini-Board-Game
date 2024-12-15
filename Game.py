from Board import Board
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
        for node in range(len(self.expansion_order)):
            print(f"____ Expansion {node+1} ____")
            self.print_expanded_node(self.expansion_order[node])

    #gettin the valid positions
    def check_position(self, position):
        while not self.check_state(position):
            print("Please enter valid positions.\n")
            position = [input(), input(), input()]
        return position

    #validating given positions
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

    #conversion function for (1,2) -> 6
    def position_conversion(self, matrix):
        position = int((matrix[0] * 3) + matrix[1] + 1)
        return position

    #conversion function for 5 -> (1,1)
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

    #setting initial state by user input
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

        #setting goal state by user input
        g_positions = [input(), input(), input()]
        g_positions = self.check_position(g_positions)
        self.set_goal_state(g_positions)
        self.root_node = Node(i_positions, 0, None, None)

        #wrapping heuristic values in lists
        heuristics = self.heuristic_distances(i_positions, g_positions)
        self.root_node.heuristic = [[h] for h in heuristics]  # Fix here
        self.temp_node = self.root_node

        print("\nGoal state:")
        Board.print_board(self.board, "goal")
        self.moving_tiles_astar()

    #getting other tiles' current positions
    def get_occupied_positions(self, tile):
        positions = []
        tiles = [1,2,3]
        tiles.remove(tile.value)
        for x in tiles:
            positions.append(self.board.tiles[x-1].initial_position)
        return positions

    #tile-specific heuristic value
    def manhattan_distance(self, goal_position, next_tile_position):
        return (abs(int(goal_position[0]) - int(next_tile_position[0])) +
                abs(int(goal_position[1]) - int(next_tile_position[1])))

    #calculating state's heuristic values
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
        return initials == goals

    def possible_moves(self, tile):
        row, col = tile.initial_position
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        occupied_positions = self.get_occupied_positions(tile)
        moves = []

        for i, j in possible_moves:
            new_row, new_col = row + i, col + j
            next_tile = (new_row, new_col)

            #skip if the next position is out of bounds or occupied
            if 0 <= new_row < 3 and 0 <= new_col < 3 and next_tile not in occupied_positions and next_tile != tile.initial_position:
                step_cost = self.get_step_cost(tile, next_tile)
                h_cost = self.manhattan_distance(tile.goal_position, next_tile)
                total_cost = step_cost + h_cost

                positions = self.initial_state[:]
                positions[int(tile.value) - 1] = str(self.position_conversion(next_tile))
                node = Node(positions, self.temp_node.get_depth() + 1, self.temp_node, tile.value)
                self.temp_node.add_child(node)
                node.parent = self.temp_node

                #copy heuristics
                node.heuristic = [h[:] for h in self.temp_node.heuristic]
                node.heuristic[int(tile.value) - 1][0] = h_cost

                temp_node = node.parent
                prev_costs = 0
                while temp_node.parent is not None:
                    prev_costs += temp_node.played_cost
                    temp_node = temp_node.parent

                heuristic_cost = sum(heuristic[0] for heuristic in node.heuristic)
                node_cost = step_cost + heuristic_cost + prev_costs

                moves.append((node, total_cost, step_cost, node_cost))

        for move in moves:
            self.fringe[tile.value - 1].append(move)

        return len(moves), tile.value

    def moving_tiles_astar(self):
        tile_order = [1, 2, 3]
        visited_positions = {1: set(), 2: set(), 3: set()}  # Track visited positions for each tile
        visited_states = set()  # Track the entire board state to avoid revisiting
        progress_made = False

        #expanding the initial state
        self.expansion_order.append(self.temp_node)
        print("\n-------Expansion " + str(self.current_step + 1) + "-------\n")
        print("Initial Node Expanded:")
        Board.print_board(self.board, "current")
        self.current_step += 1

        if self.is_initial_goal(self.initial_state, self.goal_state):
            print("\nThe initial board state is the goal state!")
            print("Total cost --> 0")
        else:
            while self.current_step < self.max_step:

                for tile_number in tile_order:
                    if self.current_step >= self.max_step:
                        break

                    tile = self.board.tiles[tile_number - 1]

                    #skip tile if it's already in its goal position
                    if tile.initial_position == tile.goal_position:
                        if tile_number == 3 :
                            self.temp_node.current_played_tile = 3
                        else:
                            self.temp_node.current_played_tile = tile_number
                        continue

                    if self.current_step > 2:
                        if tile_number == 1 and self.temp_node.current_played_tile != 3:
                            continue
                        elif tile_number == 2 and self.temp_node.current_played_tile != 1:
                            continue
                        elif tile_number == 3 and self.temp_node.current_played_tile != 2:
                            continue

                    #getting possible moves
                    possible_move, tile_value = self.possible_moves(tile)

                    if possible_move > 0:
                        print("\n-------Expansion "+str(self.current_step+1)+"-------\n")
                        least_cost_path = min((move for sublist in self.fringe for move in sublist),key=lambda x: x[3])
                        new_position = least_cost_path[0].state[least_cost_path[0].current_played_tile - 1]
                        if not least_cost_path[0] in self.temp_node.children:
                            print("Going back for moving with a least cost path...\n")
                            print(f"Tile #{least_cost_path[0].current_played_tile} is moving to position {new_position}")
                        else:
                            print(f"Tile #{tile_value} is moving to position {new_position}")
                        self.fringe[int(least_cost_path[0].current_played_tile)-1].remove(least_cost_path)
                        self.temp_node = least_cost_path[0]
                        self.temp_node.played_cost = least_cost_path[2]

                        state_tuple = tuple(least_cost_path[0].state)

                        #check if the position or state has already been visited
                        if state_tuple in visited_states:
                            continue  #skip already visited states

                        visited_states.add(state_tuple)  #add the new state to visited states
                        visited_positions[least_cost_path[0].current_played_tile].add(new_position)  #track the position of the tile

                        #update tile's position
                        tile.initial_position = self.matrix_conversion(new_position)

                        print(f"Current path cost for played tile is --> {least_cost_path[2]}")
                        print(f"Current cost(heuristic and position cost) of the tile is --> {least_cost_path[1]}")
                        heuristic_sum = sum(heuristic[0] for heuristic in self.temp_node.heuristic)
                        print(f"Current heuristic for this state is --> {heuristic_sum}")
                        self.expansion_order.append(least_cost_path[0])
                        print("\nExpanded Node:")
                        self.print_expanded_node(least_cost_path[0])
                        self.set_state(least_cost_path[0].state)

                        tile_number = least_cost_path[0].current_played_tile

                        progress_made = True
                    else:
                        print(f"Tile #{tile.value} cannot make any moves at the moment.\nGame over:/")
                        break

                    #check if the board is in the goal state
                    if self.board.is_goal_state():
                        print("\nGoal state reached!\n")
                        print(":Expansion Order:")
                        self.show_expansions()
                        return True

                    self.current_step += 1

                #if no progress is made, break the loop
                if not progress_made:
                    break
            print("\nGoal state not reached within 10 steps.")
            return False