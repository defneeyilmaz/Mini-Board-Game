from Board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.initial_state = None
        self.goal_state = None

    def begins(self):
        print("\nWelcome to the mini board game!")
        print("You need to set the initial and goal states to start the game.\n")
        print("Set the initial state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)

    def invalid_message(self):
        print("Please enter valid positions.\n")

    def check_position(self, position):
        while not self.check_state(position):
            self.invalid_message()
            position = [input(), input(), input()]
        return position

    def check_state(self, positions):
        if not len(positions) == 3: return False
        if not len(set(positions)) == len(positions): return False
        for x in positions:
            if 1 <= int(x) <= 9: return True
            else: return False

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

    def goal_state_info(self):
        print("Now, set the goal state by selecting one by one, the positions of tiles "
              "1, 2, and 3 in order from the numbers on the board.\n")
        possible_positions = "1 2 3,4 5 6,7 8 9"
        possible_positions = possible_positions.split(",")
        for x in possible_positions:
            print(x)
