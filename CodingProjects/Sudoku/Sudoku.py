from Search import CSP, different_values
import itertools
from math import sqrt

########    Search Class Methods and Object     ########
# Some miscellanous methods needed for Search
# Used to divide the board up by rows, columns, and boxes for Search
def flatten(seqs):
    return sum(seqs, [])


class Sudoku(CSP):

    def __init__(self, grid, y=None, x=None):
        self.n = None if y is not None else int(sqrt(len(grid[0])))
        self.y_size = y if y is not None else self.n
        self.x_size = x if y is not None else self.n

        self.largest_domain = len(grid[0])
        # initialize based on parameter "n"
        range_x = list(range(self.x_size))
        range_y = list(range(self.y_size))
        self.Cell = itertools.count().__next__
        bgrid = [[[[self.Cell() for x in range_x] for y in range_y] for bx in range_y] for by in range_x]
        boxes = flatten([list(map(flatten, brow)) for brow in bgrid])
        self.rows = flatten([list(map(flatten, zip(*brow))) for brow in bgrid])
        cols = list(zip(*self.rows))

        self.neighbors = {v: set() for v in flatten(self.rows)}

        for unit in map(set, boxes + self.rows + cols):
            for v in unit:
                self.neighbors[v].update(unit - {v})

        self.grid = grid
        domains = {}
        self.variables = list(range(0, int((len(grid) * len(grid[0])))))
        for index, variable in enumerate(flatten(self.rows), start=0):
            if grid[int(index / self.largest_domain)][int(index % self.largest_domain)] != 0:
                domains[variable] = [grid[int(index / self.largest_domain)][int(index % self.largest_domain)]]
            else:
                domains[variable] = list(range(1, (self.largest_domain + 1)))
        CSP.__init__(self, domains=domains, neighbors=self.neighbors, constraints=different_values)
        self.initial = self.set_initial_state()
        if self.initial is None:
            raise ValueError("The initial board is impossible.")

    def set_initial_state(self):
        """
        Cycles through the domains of all variables and assigns any variable with
        only 1 possiblity because it is a given from the initial board.

        :return: the initial state where all given information is entered into the initial state
        """
        assignment = {}
        for variable in self.domains.keys():
            if len(self.domains[variable]) == 1:
                if self.nconflicts(variable=variable, value=self.domains[variable][0], assignment=assignment) == 0:
                    self.assign(variable=variable, value=self.domains[variable][0], assignment=assignment)
                else:
                    return None
        return assignment

    def display(self, assignment):
        """
        Prints the board based on the given assignment/state.

        :param assignment: current board
        :return: return the string printed
        """
        grid_state = dict(assignment)
        puzzle = ""
        rows = list(range(0, self.largest_domain*self.largest_domain, (self.largest_domain * self.y_size)))
        for index, variable in enumerate(flatten(self.rows), start=0):
            if variable in grid_state:
                puzzle += str(grid_state[variable]) + " "
            else:
                puzzle += '_ '
            if (1 + index) % (self.y_size * self.x_size) == 0:
                puzzle += "\n"
                if (1 + index) in rows:
                    puzzle += ("-" * (self.largest_domain*2 + self.y_size)) + "\n"
            elif (1 + index) % self.x_size == 0:
                puzzle += "| "
        print(puzzle)
        return puzzle

    def puzzle_to_array_repr(self, assignment):
        grid_state = dict(assignment)
        puzzle = []
        puzzle_row = []
        for index, variable in enumerate(flatten(self.rows), start=0):
            if variable in grid_state:
                puzzle_row.append(grid_state[variable])
            else:
                puzzle_row.append(None)

            if len(puzzle_row) == self.largest_domain:
                puzzle.append(puzzle_row)
                puzzle_row = []

        return puzzle


# grid = [
#      [0, 0, 1, 0],
#      [4, 0, 0, 0],
#     [0, 0, 0, 2],
#     [0, 3, 0, 0]
# ]
# puzzle = Sudoku(grid=grid)
# sol = backtracking(puzzle, puzzle.initial)
# puzzle.display(sol)
# print(puzzle.nassigns)