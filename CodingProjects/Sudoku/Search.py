import random


class SearchProblem(object):
    """
    Will be the general Object describing search problems like Search and n-Queen puzzles
    """
    def __init__(self, initial_state, goal=None):
        self.initial = initial_state
        self.goal = goal

    def actions(self, state):
        """
        Need to return the set of actions available from given state

        :param state: the current state you wish to find possible actions for
        :return: the list (probably, depends on specific case) of possible actions from state
        """
        raise NotImplementedError

    def result(self, state, action):
        """
        Returns the resulting state after an action is performed on the given state.

        :param state: current state
        :param action: the action performed on current state
        :return: the resulting state
        """
        raise NotImplementedError

    def is_goal(self, state):
        """
        Is current state in the goal state?

        :param state: current state to check if it is in goal state
        :return: Boolean; true for in goal, otherwise not in goal state
        """
        raise NotImplementedError


class Node:
    """
    A Node in search tree contains pointer to the parent (Node with 1 less action)
    The Node keeps state stored, action that occurred to result this Node, stores depth (number of parents)
    """

    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action    # may not be needed
        self.depth = 0
        if parent is not None:
            self.depth = parent.depth + 1

    """
    Returns the list of new nodes reachable from the current state
    """
    def expand(self, search_problem):
        return [self.child_node(search_problem, action)
                for action in search_problem.actions(self.state)]

    """
    This returns a next, reachable node within the search problem state space 
    """
    def child_node(self, search_problem, action):
        new_state = search_problem.result(self.state, action)
        new_node = Node(state=new_state, action=action, parent=self)
        return new_node


# The constraint for Search (neighbors must be different values)
def different_values(A, a, B, b):
    return a != b


class CSP(SearchProblem):
    """
    Constraint Satisfaction Problem (inherits the SearchProblem class)
    """

    def __init__(self, domains, neighbors, constraints=different_values):
        """

        :param domains: holds the variables within the keys() of the dict.
                        specifies what values are allowed for each variable in problem.
        :param neighbors: this specifies which variables conflict with another
        :param constraints: this specifies the function to judge if there is a conflict
        """
        self.variables = list(domains.keys())
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.nassigns = 0
        self.initial = ()

    def assign(self, variable, value, assignment):
        """
        Takes the variable and assigns it the value in the given assignment.

        :param variable: the variable to be assigned
        :param value: The value to be assigned to the variable in current assignment
        :param assignment: the current state of the CSP
        :return: no returns as the assignment passed is altered
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

    def nconflicts(self, variable, value, assignment):
        """
        Counts the number of conflicts of given variable and assignment of said variable with neighbors

        :param variable: the variable that is being assigned a value to see number of conflicts
        :param value: the value the variable will take on
        :param assignment: the state the CSP is in currently (only assigned variables)
        :return: integer representing the number of conflicts the current variable and value pair have
        """
        # May not need this :param in_assignment: This is for the edge case where the assignment dict is not in memory yet
        nconflicts = 0
        for neighbor in self.neighbors[variable]:
            if neighbor in assignment and not self.constraints(variable, value, neighbor, assignment[neighbor]):
                nconflicts += 1
        return nconflicts

    def actions(self, state):
        """
        Get the list of action possible from the given state.

        :param state: dictionary of variables -> domains; tracks what each variable can take on
        :return: list of actions
        """

        if len(state) == len(self.variables):
            return []  # no actions to take here
        else:
            # find the action with the lowest nconflict amount
            assignment = dict(state)  # ensure it is dictionary
            # take the first available variable that has NOT been assigned yet
            variable = [var for var in self.variables if var not in assignment].pop(0)
            actions = []
            for action in self.domains[variable]:
                if self.nconflicts(variable=variable, value=action, assignment=assignment) == 0:
                    actions.extend([(variable, action)])
            return actions

    def result(self, state, action):
        """
        Takes current state and the action taken to resolve in the new state (add new assignment)

        :param state: tracks the current order of assignments for the CSP
        :param action: The action selected, a tuple of (variable to assign, value of variable)
        :return: new state with the added assignment
        """
        (var, val) = action
        return state + ((var, val), )

    def is_goal(self, state):
        """
        Tests to see if state is in the goal state.

        :param state: the state to check if it is within the goal state.
        :return: Boolean; True if IN goal state, False if NOT in goal stat
        """

        current_assignment = dict(state)
        if len(current_assignment) == len(self.variables):
            for variable in self.variables:
                if not self.nconflicts(variable, current_assignment[variable], current_assignment) == 0:
                    return False
            return True
        return False


# Heuristics
def minimum_remaining_values(csp, assignment):
    """
    Given the potential, partial solution to the CSP in csp through assignment,
    find the variable that is ***MOST*** constrained. This means the variable that has the
    smallest number of values possible depending on the current assignment.

    :param csp: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :return: the variable that is MOST constrained
    """
    mrv = {"var": None, "legal_moves": None}
    for variable in csp.variables:
        if variable not in assignment:
            number_of_legal_moves = 0
            for value in csp.domains[variable]:
                if csp.nconflicts(variable, value, assignment) == 0:
                    number_of_legal_moves += 1
            if number_of_legal_moves == 1 or number_of_legal_moves == 0:
                return variable
            if mrv["legal_moves"] is None or number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": variable, "legal_moves": number_of_legal_moves}
    return mrv['var']


def minimum_remaining_values_random(csp, assignment):
    """
    FOR GENERATING PUZZLES!!!


    Given the potential, partial solution to the CSP in csp through assignment,
    find the variable that is ***MOST*** constrained. This means the variable that has the
    smallest number of values possible depending on the current assignment.

    :param csp: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :return: the variable that is MOST constrained
    """
    mrv = {"var": None, "legal_moves": None}
    for variable in csp.variables:
        if variable not in assignment:
            number_of_legal_moves = 0
            for value in csp.domains[variable]:
                if csp.nconflicts(variable, value, assignment) == 0:
                    number_of_legal_moves += 1
            if mrv["legal_moves"] is None or number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": [variable], "legal_moves": number_of_legal_moves}
            if number_of_legal_moves == mrv['legal_moves']:
                mrv['var'].append(variable)
            elif number_of_legal_moves < mrv['legal_moves']:
                mrv = {"var": [variable], "legal_moves": number_of_legal_moves}
    return random.choice(mrv['var'])


def least_constraining_values(csp, assignment, variable):
    """
    Given the next variable to assign within the current potential, partial solution given by assignment,
    find the value for said variable that is *LEAST* constraining.

    :param csp: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :param variable: the variable to assign next
    :return: the value of the variable that is LEAST constraining on problem
    """
    return sorted(csp.domains[variable],
                  key=lambda val: csp.nconflicts(variable, val, assignment))


def least_constraining_values_random(csp, assignment, variable):
    """
    FOR GENERATING PUZZLE

    Given the next variable to assign within the current potential, partial solution given by assignment,
    find the value for said variable that is *LEAST* constraining.

    :param csp: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :param variable: the variable to assign next
    :return: the value of the variable that is LEAST constraining on problem
    """
    nconflict_dict = {}
    for val in csp.domains[variable]:
        num_conflicts = csp.nconflicts(variable, val, assignment)
        if num_conflicts in nconflict_dict.keys():
            nconflict_dict[num_conflicts].append(val)
        else:
            nconflict_dict[num_conflicts] = [val]

    returning_list = []
    for val in sorted(nconflict_dict.keys()):
        random.shuffle(nconflict_dict[val])
        returning_list.extend(nconflict_dict[val])
    return returning_list


def most_constraining_values(csp, assignment, variable):
    """
    Given the next variable to assign within the current potential, partial solution given by assignment,
    find the value for said variable that is *LEAST* constraining.

    :param csp: The CSP Object where the problem is defined
    :param assignment: the current assignment of the problem (what is currently being used as partial soln)
    :param variable: the variable to assign next
    :return: the value of the variable that is LEAST constraining on problem
    """
    return sorted(csp.domains[variable],
                  key=lambda val: csp.nconflicts(variable, val, assignment), reverse=True)


# Backtracking utilizing heuristics
def backtracking(csp, initial_state=None, is_generate=False):
    """
    This is the backtracking algorithm designed to utilize heuristics to solve constraint
    satisfaction problems.

    :param csp: the CSP class that defines the problem to be solved
    :param initial_state: this is an optional parameter that is designed to quickly assign
                            all variables to values whose domain is length 1 (given via the problem).
                            This helps to minimize the number of assignments initially.
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
        :return: the assignment that solves CSP; OR None to represent failure
        """
        if csp.is_goal(assignment):
            return assignment

        # need to select the most constrained variable (MRV) and least constraining value (LCV)
        variable = minimum_remaining_values(csp, assignment)  # select the variable
        for value in least_constraining_values(csp, assignment, variable):
            # this verifies this value for the variable is allowed
            if csp.nconflicts(variable, value, assignment) == 0:
                csp.assign(variable=variable, value=value, assignment=assignment)
                result = backtrack(assignment)
                if result is not None:
                    return result

        csp.unassign(variable=variable, assignment=assignment)
        return None


    def backtrack_generate(assignment):
        """
        Method that utilizes recursion to slowly try all legal possibilities.
        1: Find the variable that has the MOST restrictions on it (fewest possible values to assign).
        2: Try to assign that variable with the value that is LEAST constraining on all other variables
        3: Ensure this Variable-Value pair is legal
        4: Assign and Backtrack again with updated assignment
        5: If not Legal, then return None and finish all other Backtracks

        :param assignment: current state to either assign new variable or return as goal state
        :return: the assignment that solves CSP; OR None to represent failure
        """
        if csp.is_goal(assignment):
            return assignment

        # need to select the most constrained variable (MRV) and least constraining value (LCV)
        variable = minimum_remaining_values_random(csp, assignment)  # select the variable
        for value in least_constraining_values_random(csp, assignment, variable):
            # this verifies this value for the variable is allowed
            if csp.nconflicts(variable, value, assignment) == 0:
                csp.assign(variable=variable, value=value, assignment=assignment)
                result = backtrack_generate(assignment)
                if result is not None:
                    return result

        csp.unassign(variable=variable, assignment=assignment)
        return None

    if is_generate:
        initial_state = {}
        result = backtrack_generate(dict(initial_state))
    else:
        initial_state = {} if initial_state is None else initial_state
        result = backtrack(dict(initial_state))
    return result


def modified_backtracking(csp):
    def backtrack(state):
        if csp.is_goal(state):
            return state

        variable = minimum_remaining_values(csp, state)  # select the variable
        for value in least_constraining_values(csp, state, variable):
            if csp.nconflicts(variable, value, state) == 0:
                csp.assign(variable=variable, value=value, assignment=state)
                result = backtrack(state)
                if result is not None:
                    return result
        csp.unassign(variable=variable, assignment=state)
        return None

    result = backtrack({})
    return result


