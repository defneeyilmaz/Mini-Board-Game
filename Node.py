class Node:

    def __init__(self, state, _depth, parent, current_played_node):
        self.state = state
        self.depth = _depth
        self.cost = [[0] for _ in range(3)]
        self.heuristic = [[0] for _ in range(3)]
        self.total_cost = [[0] for _ in range(3)]
        self.children = []
        self.parent = parent
        self.current_played_tile = current_played_node

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_cost(self, tile):
        return self.cost[tile]

    def get_depth(self):
        return self.depth

    def get_children(self):
        return self.children

    def get_current_played_tile(self):
        return self.current_played_tile