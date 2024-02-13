class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    # removing first element as queue is fifo(first in first out)
    def remove(self):
        if self.empty():
            raise Exception("the frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            content = file.read()

        # checking if a maze have exactly one starting and one final point
        if content.count("S") != 1:
            raise Exception("maze must have exactly one starting point!")
        if content.count("G") != 1:
            raise Exception("maze must have exactly one goal!")

        # setting the width and height of a maze
        content = content.splitlines()
        self.height = len(content)
        self.width = max(len(line) for line in content)

        # checking which points are the walls
        self.walls = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                if content[r][c] == "S":
                    row.append(False)
                    self.start = (r, c)
                elif content[r][c] == "G":
                    row.append(False)
                    self.goal = (r, c)
                elif content[r][c] == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)
        self.solution = None

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("S", end="")
                elif (i, j) == self.goal:
                    print("G", end="")
                elif solution is not None and (i, j) in solution:
                    print("+", end="")
                else:
                    print(" ", end="")
            print()

    def solve(self):
        self.num_explored = 0

        # initialize the frontier and set starting position
        start = Node(self.start, None, None)
        frontier = QueueFrontier()
        frontier.add(start)

        # initialize the explored_set
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("no solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    frontier.add(Node(state, node, action))


maze = Maze("maze1.txt")
maze.solve()
maze.print()
