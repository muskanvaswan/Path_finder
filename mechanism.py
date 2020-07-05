import sys
from gui import output_image
import os

class Node():
    def __init__(self, state, action, parent):
        self.action = action
        self.state = state
        self.parent =  parent

class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        #check if frontier is empty
        if self.empty():
            raise Exception("underflow")
        #remove from the beggining
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

    def possible_action(self, state):
        return any(node.state == state for node in self.frontier)

    #checking if the frontier is Empty
    def empty(self):
        return len(self.frontier) == 0

class Maze():

    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        #convertinf it into a 2d array
        contents = contents.splitlines()


        #deducing width
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        #keeping track of walls by appending false for wall and true for path
        self.walls= []

        for i in range(self.height):
            #list of true or falls for every row
            rows = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        rows.append(True)

                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        rows.append(True)

                    elif contents[i][j] ==' ':
                        rows.append(True)

                    elif contents[i][j] == '#':
                        rows.append(False)
                except:
                    raise IndexError
            self.walls.append(rows)

        #initializing solution to be zero
        self.solution = None

    def graphic(self):

        solution = self.solution[1] if self.solution is not None else None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):


                if (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif col:
                    print(" ", end="")
                else:
                    print("█", end="")
            print()
        print()

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
            if 0 <= r < self.height and 0 <= c < self.width and self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
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

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.possible_action(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


if len(sys.argv) != 2:
    sys.exit("provide maze.")

maze = Maze(sys.argv[1])
print("Maze:")
maze.graphic()
print("solving")
maze.solve()
print("Path found: ")
maze.graphic()
output_image(maze=maze)
os.system("open maze.png")
