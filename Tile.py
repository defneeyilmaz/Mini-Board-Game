class Tile:
    def __init__(self, value, initial_position, goal_position):
        self.value = value
        self.initial_position = initial_position
        self.goal_position = goal_position
        self.cost = 0

    def __repr__(self):
        return str(self.value)