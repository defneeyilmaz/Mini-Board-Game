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

    