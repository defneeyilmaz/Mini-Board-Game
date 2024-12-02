from Tile import Tile

class Board:
    def __init__(self):
        self.initial_tiles = [
            Tile(1, (0, 0)),
            Tile(2, (0, 0)),
            Tile(3, (0, 0))
        ]
        self.goal_position= [
            Tile(1, (0, 0)),
            Tile(2, (0, 0)),
            Tile(3, (0, 0))
        ]

    def set_initial_tile_position(self, tile_value, new_position):
        for tile in self.initial_tiles:
            if tile.value == tile_value:
                tile.position = new_position
                break

    def set_goal_tile_position(self, tile_value, new_position):
        for tile in self.goal_position:
            if tile.value == tile_value:
                tile.position = new_position
                break

    def print_board(self):
        print()
        board = [['_' for _ in range(3)] for _ in range(3)]

        for tile in self.initial_tiles:
            row, col = tile.position
            board[row][col] = str(tile.value)

        for row in board:
            print(" ".join(row))
        print()

    def is_goal_state(self, goal_state):
        count = 0
        for x in range(1, 3, 1):
            if self.initial_tiles[x].position == self.goal_position[x].position:
                count += 1
        if count == 3:
            return True
        else:
            return False