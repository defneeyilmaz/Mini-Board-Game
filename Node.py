class Node:

    def __init__(self, state, _depth, parent, current_played_node):
        self.state = state
        self.depth = _depth
        self.cost = 0
        self.heuristic = [[0] for _ in range(3)]
        self.children = []
        self.played_cost = 0
        self.parent = parent
        self.current_played_tile = current_played_node

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_depth(self):
        return self.depth