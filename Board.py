from Tile import Tile

class Board:
    def __init__(self):
        self.tiles = [
            Tile(1, (0, 0),(0,0)),
            Tile(2, (0, 0),(0,0)),
            Tile(3, (0, 0),(0,0))
        ]

    def set_initial_tile_position(self, tile_value, new_position):
        for tile in self.tiles:
            if tile.value == tile_value:
                tile.initial_position = new_position
                break

    def set_goal_tile_position(self, tile_value, new_position):
        for tile in self.tiles:
            if tile.value == tile_value:
                tile.goal_position = new_position
                break

    def print_board(self):
        print()
        board = [['_' for _ in range(3)] for _ in range(3)]

        for tile in self.tiles:
            row, col = tile.initial_position
            board[row][col] = str(tile.value)

        for row in board:
            print(" ".join(row))
        print()

    #def is_goal_state_for_tile(self, tile):
    #    if tile.initial_position[0] == tile.goal_position[0] and tile.initial_position[1] == tile.goal_position[1]:
    #        return True
    #    else : return False

    def is_goal_state(self):
        count = 0
        for x in range(0, 3, 1):
            if self.tiles[x].initial_position == self.tiles[x].goal_position:
                count += 1
        if count == 3:
            return True
        else:
            return False