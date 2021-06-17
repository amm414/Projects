import random
import itertools
from math import sqrt
import time

########    Search Class Methods and Object     ########
# Some miscellanous methods needed for Search
# Used to divide the board up by rows, columns, and boxes for Search
def flatten(seqs):
    return sum(seqs, [])


class Sudoku():

    def __init__(self, grid, y, x):
        """
        :param grid: initial state of board
        :param y: the y length of box of Sudoku
        :param x: the x width of box of Sudoku

        self.domains: dict; Var: List of values variable can take
        self.neighbors: dict; Var: List of Vars that are Neighbors
        self.y_size: int of size of 1 dimension of box in sudoku
        self.x_size: int of size of 1 dimension of box in sudoku
        self.largest_domain: largest value in domain (max sudoku value)


        """
        self.nassigns = 0 # number of assignments made
        self.domain_var_value_pairs_removed = None
        self.y_size = y
        self.x_size = x
        self.grid = grid
        self.largest_domain = int(x * y)
        self.domains = {}
        self.variables = list(range(0, self.y_size*self.y_size*self.x_size*self.x_size))

        # initialize based on parameter "n"
        # largely used for neighbor dictionary creation
        range_x = list(range(self.x_size))
        range_y = list(range(self.y_size))
        self.Cell = itertools.count().__next__
        bgrid = [[[[self.Cell() for x in range_x] for y in range_y] for bx in range_y] for by in range_x]
        boxes = flatten([list(map(flatten, brow)) for brow in bgrid])
        self.rows = flatten([list(map(flatten, zip(*brow))) for brow in bgrid])
        cols = list(zip(*self.rows))

        # get the neighbor variables (elements of sudoku which cannot be same value)
        self.neighbors = {v: set() for v in flatten(self.rows)}
        for unit in map(set, boxes + self.rows + cols):
            for v in unit:
                self.neighbors[v].update(unit - {v})

        # get the domains which are lists (set either to any possible value or initial value)
        for index, variable in enumerate(flatten(self.rows), start=0):
            if grid[int(index / self.largest_domain)][int(index % self.largest_domain)] is not None and grid[int(index / self.largest_domain)][int(index % self.largest_domain)] != 0:
                self.domains[variable] = [grid[int(index / self.largest_domain)][int(index % self.largest_domain)]]
            else:
                self.domains[variable] = list(range(1, (self.largest_domain + 1)))

        # set teh initial assignment
        self.initial = self.set_initial_state()
        if self.initial is None:
            raise ValueError("The initial board is impossible.")

        # infer from the initial state; remove domain values from variables that
        # are not possible with initial information.
        while self.infer_from_initial():
            pass

    def nconflicts(self, variable, value, assignment):
        """
        Calculate the Total Number of conflicts for the Var: Val pair within Assignment
        :param variable: Variable that is attempted being assigned
        :param value: Value being assigned to variable (var)
        :param assignment: the current assignment to test against neighbors
        :return: number of conflicts encountered
        """
        return sum([1 for neighbor in self.neighbors[variable] if neighbor in assignment and assignment[neighbor] == value])

    def assign(self, variable, value, assignment):
        """
        Assign the Value to Variable for current Assignment
        :param variable: variable being assigned
        :param value: value being assigned to variable
        :param assignment: current assignment being updated
        :return:
        """
        assignment[variable] = value
        self.nassigns += 1

    def unassign(self, variable, assignment):
        """
        Takes the variable to unassign and removes it from assignment

        :param variable: the variable to unassign by deleting the variable from the state/assignment.
        :param assignment: the current state of the CSP
        :return: no returns as the assignment passed is altered
        """
        if variable in assignment:
            del assignment[variable]

    def is_goal(self, assignment):
        """
        Determine if in goal state
        :param assignment: current assignemnt being tested for being in goal state
        :return: True (IS in goal state) or False (NOT in goal state)
        """
        assignment = dict(assignment)
        if len(assignment.keys()) == self.x_size * self.y_size * self.x_size * self.y_size:
            for var in self.variables:
                for neighbor in self.neighbors[var]:
                    if assignment[var] == assignment[neighbor]:
                        return False
            return True
        return False

    def set_initial_state(self):
        """
        Cycles through the domains of all variables and assigns any variable with
        only 1 possibility because it is a given from the initial board.

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

    def infer_from_initial(self):
        altered = False
        for variable in self.variables:
            if len(self.domains[variable]) == 1:
                for neighbor in self.neighbors[variable]:
                    for neighbor_val in self.domains[neighbor][:]:
                        if self.domains[variable][0] == neighbor_val:
                            self.domains[neighbor].remove(self.domains[variable][0])
                            altered = True
                        if len(self.domains[neighbor]) == 0:
                            raise ValueError("The domains should be minimum length of 1")
        return altered

    def add_back_inferenced_domains_removed(self, inference_pairs_removed):
        for (var, val) in inference_pairs_removed:
            self.domains[var].append(val)

    def infer_assignment(self, variable, value):
        inferenced_removed = []
        for v in self.domains[variable]:
            if v != value:
                inferenced_removed.append((variable, v))
        self.domains[variable] = [value]
        return inferenced_removed

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

    def partial_solution(self, assignment, default_null=None, percent_int=50):
        puzzle = self.puzzle_to_array_repr(assignment)
        row, col = list(range(self.y_size * self.x_size)), list(range(self.y_size * self.x_size))
        random.shuffle(row)
        random.shuffle(col)
        col_app, row_app = 0, 0
        partial_puzzle = []
        for i, row in enumerate(puzzle):
            new_row = []
            for j, elem in enumerate(row):
                if col[i] == j:
                    col_app += 1
                    new_row.append(elem)
                elif row[j] == i:
                    row_app += 1
                    new_row.append(elem)
                elif random.randint(1,100) > percent_int:
                    new_row.append(default_null)
                else:
                    new_row.append(elem)
            partial_puzzle.append(new_row)
        return partial_puzzle


# for reading a list of values into board
# returns grid
def format_string_board(board, w, h):
    new_board = []
    for i in range(w*h):
        row = []
        for j in range(w*h):
            row.append(int(board[(i*(w*h)) + j]))
        new_board.append(row)
    return new_board


def minimum_remaining_values(sudoku, assignment):
    """
    Given the potential, partial solution to the CSP in csp through assignment,
    find the variable that is ***MOST*** constrained. This means the variable that has the
    smallest number of values possible depending on the current assignment.

    :param sudoku: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :return: the variable that is MOST constrained
    """
    mrv = {"var": None, "legal_moves": None}
    for variable in sudoku.variables:
        if variable not in assignment:
            number_of_legal_moves = len(sudoku.domains[variable])
            if number_of_legal_moves <= 1:
                return variable
            if mrv["legal_moves"] is None or number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": variable, "legal_moves": number_of_legal_moves}
    return mrv['var']


def minimum_remaining_values_random(sudoku, assignment):
    """
    FOR GENERATING PUZZLES!!!


    Given the potential, partial solution to the CSP in csp through assignment,
    find the variable that is ***MOST*** constrained. This means the variable that has the
    smallest number of values possible depending on the current assignment.

    :param sudoku: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :return: the variable that is MOST constrained
    """
    mrv = {"var": None, "legal_moves": None}
    for variable in sudoku.variables:
        if variable not in assignment:
            number_of_legal_moves = len(sudoku.domains[variable])
            if mrv["legal_moves"] is None or number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": [variable], "legal_moves": number_of_legal_moves}
            if number_of_legal_moves == mrv['legal_moves']:
                mrv['var'].append(variable)
            elif number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": [variable], "legal_moves": number_of_legal_moves}
    return random.choice(mrv['var'])


def least_constraining_values(sudoku, assignment, variable):
    """
    Given the next variable to assign within the current potential, partial solution given by assignment,
    find the value for said variable that is *LEAST* constraining.

    :param sudoku: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :param variable: the variable to assign next
    :return: the value of the variable that is LEAST constraining on problem
    """
    return sorted(sudoku.domains[variable],
                  key=lambda val: sudoku.nconflicts(variable, val, assignment))


def least_constraining_values_random(sudoku, assignment, variable):
    """
    FOR GENERATING PUZZLE

    Given the next variable to assign within the current potential, partial solution given by assignment,
    find the value for said variable that is *LEAST* constraining.

    :param sudoku: The Sudoku Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :param variable: the variable to assign next
    :return: the value of the variable that is LEAST constraining on problem
    """
    nconflict_dict = {}
    for val in sudoku.domains[variable]:
        num_conflicts = sudoku.nconflicts(variable, val, assignment)
        if num_conflicts in nconflict_dict.keys():
            nconflict_dict[num_conflicts].append(val)
        else:
            nconflict_dict[num_conflicts] = [val]

    returning_list = []
    for val in sorted(nconflict_dict.keys()):
        random.shuffle(nconflict_dict[val])
        returning_list.extend(nconflict_dict[val])
    return returning_list


def forward_checking(sudoku, variable, value, assignment, inference_pairs_removed):
    for neighbor in sudoku.neighbors[variable]:
        if neighbor not in assignment:
            for neighbor_val in sudoku.domains[neighbor][:]:
                if neighbor_val == value:
                    sudoku.domains[neighbor].remove(neighbor_val)
                    inference_pairs_removed.append((neighbor, neighbor_val))
            if len(sudoku.domains[neighbor]) == 0:
                return False
    return True


def backtracking(sudoku):
    """
    This is the backtracking algorithm designed to utilize heuristics to solve constraint
    satisfaction problems.

    :param sudoku: the sudoku class that defines the problem to be solved
    :return: The state that is in the Goal State OR None to represent no solution found
    """

    def backtrack(assignment):
        """
        Method that utilizes recursion to slowly try all legal possibilities.
        1: Find the variable that has the MOST restrictions on it (fewest possible values to assign).
        2: Try to assign that variable with the value that is LEAST constraining on all other variables
        3: Ensure this Variable-Value pair is legal
        4: Assign and Backtrack again with updated assignment
        5: If not Legal, then return None and finish all other Backtracks

        :param assignment: current state to either assign new variable or return as goal state
        :return: the assignment that solves sudoku; OR None to represent failure
        """
        if sudoku.is_goal(assignment):
            return assignment

        # need to select the most constrained variable (MRV) and least constraining value (LCV)
        variable = minimum_remaining_values(sudoku, assignment)  # select the variable
        for value in least_constraining_values(sudoku, assignment, variable):
            if sudoku.nconflicts(variable, value, assignment) == 0:
                sudoku.assign(variable=variable, value=value, assignment=assignment)
                if sudoku.nassigns > 100_000:
                    raise RuntimeError("Too many nassigns")
                removed_inferred_domains = sudoku.infer_assignment(variable, value)
                if forward_checking(sudoku, variable, value, assignment, removed_inferred_domains):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                sudoku.add_back_inferenced_domains_removed(removed_inferred_domains)
        sudoku.unassign(variable=variable, assignment=assignment)
        return None

    initial_state = sudoku.initial
    result = backtrack(dict(initial_state))
    return result


def generate_bactracking(sudoku):
    def backtrack_generate(assignment):
        """
        Method that utilizes recursion to slowly try all legal possibilities.
        1: Find the variable that has the MOST restrictions on it (fewest possible values to assign).
        2: Try to assign that variable with the value that is LEAST constraining on all other variables
        3: Ensure this Variable-Value pair is legal
        4: Assign and Backtrack again with updated assignment
        5: If not Legal, then return None and finish all other Backtracks

        :param assignment: current state to either assign new variable or return as goal state
        :return: the assignment that solves sudoku; OR None to represent failure
        """
        if sudoku.is_goal(assignment):
            return assignment

        # need to select the most constrained variable (MRV) and least constraining value (LCV)
        variable = minimum_remaining_values_random(sudoku, assignment)  # select the variable
        for value in least_constraining_values_random(sudoku, assignment, variable):
            # this verifies this value for the variable is allowed
            if sudoku.nconflicts(variable, value, assignment) == 0:
                sudoku.assign(variable=variable, value=value, assignment=assignment)
                if sudoku.nassigns > 5_000:
                    raise RuntimeError("Too many nassigns GENERATE")
                removed_inferred_domains = sudoku.infer_assignment(variable, value)
                if forward_checking(sudoku, variable, value, assignment, removed_inferred_domains):
                    result = backtrack_generate(assignment)
                    if result is not None:
                        return result
                sudoku.add_back_inferenced_domains_removed(removed_inferred_domains)
        sudoku.unassign(variable=variable, assignment=assignment)
        return None

    initial_state = {}
    result = backtrack_generate(dict(initial_state))
    return result


""" DRIVER SECTION """


def create_empty_board(x, y):
    grid = []
    for i in range(x*y):
        new_row = []
        for j in range(x*y):
            new_row.append(0)
        grid.append(new_row)
    return grid


def display_grid(grid, x, y, test=False):
    puzzle = Sudoku(grid, x, y)
    sol = generate_bactracking(puzzle)
    if not test:
        puzzle.display(sol)
    sol_array = puzzle.partial_solution(sol, 0, 40)
    percent_zeros = sum([row.count(0) for row in sol_array])

    if not test:
        for row in sol_array:
            print(row)

    puzzle2 = Sudoku(sol_array, x, y)
    sol = backtracking(puzzle2)
    if not test:
        puzzle2.display(sol)
    print(puzzle2.nassigns)
    return puzzle2.nassigns, percent_zeros


def custom_test():
    data = {}
    crashes = {}

    for i in range(3_000):
        x, y = random.choice([(2, 6), (2, 7), (2, 8), (3, 5), (2, 6), (2, 7), (2, 8), (3, 5), (3, 4), (4, 4)])
        print("\n\n" + str(i) + ": " + str((x, y)))
        start_time = time.time()
        grid = create_empty_board(x, y)
        end_time1 = time.time()
        try:
            nassigns, percent_zeros = display_grid(grid, x, y, True)
            end_time2 = time.time()
            if (x, y) in data.keys():
                data[(x, y)]['nassigns'].append(nassigns)
                data[(x, y)]['percent_zeros'].append(percent_zeros)
                data[(x, y)]['time_puzzle'].append(end_time1 - start_time)
                data[(x, y)]['time_solution'].append(end_time2 - end_time1)
            else:
                data[(x, y)] = {"nassigns": [nassigns], "percent_zeros": [percent_zeros],
                                "time_puzzle": [end_time1 - start_time], "time_solution": [end_time2 - end_time1]}
        except RuntimeError:
            if (x, y) in crashes:
                crashes[(x, y)] += 1
            else:
                crashes[(x, y)] = 1

    print("\n\n\n\n\nDONE!!!\n\n\n")

    for k, v in data.items():
        print(str(k) + ".... number of occurrences " + str(len(v['nassigns'])))
        print("Nassigns......................." + str(v['nassigns']))
        print("Mean Nassigns.................." + str(sum(v['nassigns']) / len(v['nassigns'])))
        print("Max Nassigns..................." + str(max(v['nassigns'])) + "\n")

        print("Percent Zero..................." + str(v['percent_zeros']))
        print("Mean Percent Zero.............." + str(sum(v['percent_zeros']) / len(v['percent_zeros'])))
        print("Max Percent Zero..............." + str(max(v['percent_zeros'])) + "\n")

        print("Time Puzzle Creation..........." + str(v['time_puzzle']))
        print("Mean Time Puzzle Creation......" + str(sum(v['time_puzzle']) / len(v['time_puzzle'])))
        print("Max Time Puzzle Creation......." + str(max(v['time_puzzle'])) + "\n")

        print("Time Puzzle Solution..........." + str(v['time_solution']))
        print("Mean Time Puzzle Solution......" + str(sum(v['time_solution']) / len(v['time_solution'])))
        print("Max Time Puzzle Solution......." + str(max(v['time_solution'])) + "\n")

    for k, v in crashes.items():
        print(str(k) + ": " + str(v))

