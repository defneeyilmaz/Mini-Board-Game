class Tile:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def __repr__(self):
        return str(self.value)