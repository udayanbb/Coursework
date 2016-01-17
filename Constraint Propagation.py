from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    vars = csp.get_all_variables()
    for var in vars:
        if csp.get_domain(var) == []:
            return True
    return False

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""

    assigned_vars = [var for var in csp.get_all_variables() if not csp.get_assigned_value(var) == None]

    for var in assigned_vars:
            constraints = csp.constraints_between(var, None)
            for constraint in constraints:
                if not csp.get_assigned_value(constraint.var2) == None:
                    if constraint.check(csp.get_assigned_value(var), csp.get_assigned_value(constraint.var2)) == False:
                        return False
    return True



def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""

    agenda = [problem]
    extension_count = 0

    while not agenda == []:
        current_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(current_problem):
            continue
        if not check_all_constraints(current_problem):
            continue

        if current_problem.unassigned_vars == []:
            return (current_problem.assigned_values, extension_count)

        new_p = []
        next_var = current_problem.pop_next_unassigned_var()


        for next_val in current_problem.get_domain(next_var):
            current_problem_copy = current_problem.copy()
            current_problem_copy.set_assigned_value(next_var, next_val)
            new_p.append(current_problem_copy)

        agenda = new_p + agenda

    return (None, extension_count)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""

    unassigned_vars = csp.unassigned_vars[:]

    var_domain = csp.get_assigned_value(var)
    if var_domain == None:
        unassigned_vars.remove(var)
        var_domain = csp.get_domain(var)
    else:

        var_domain = [var_domain]

    #print 'Function called: Var %s with domain' % var, var_domain

    reduced_list = []
    for unassigned_var in unassigned_vars:
        #print '    Checking neighbour %s' % unassigned_var
        constraints = csp.constraints_between(var, unassigned_var)
        unassigned_var_domain = csp.get_domain(unassigned_var)
        num_vars = len(var_domain)
        temp_unassigned_var_domain = unassigned_var_domain[:]
        #print '    Test domain:', temp_unassigned_var_domain

        for poss_val in temp_unassigned_var_domain:
            #print '        -checking value %d' % poss_val
            violation_count = 0
            for val in var_domain:
                for constraint in constraints:
                    if constraint.check(val, poss_val) == False:
                        #print '        -violation found between %s: %d and %s: %d' %(var, val, unassigned_var, poss_val), constraint
                        violation_count += 1
                        break
            if violation_count == num_vars:
                #print '        %d violates constraints for all of vars domain' % poss_val
                unassigned_var_domain.remove(poss_val)
                if not unassigned_var in reduced_list:
                    reduced_list.append(unassigned_var)
        if len(unassigned_var_domain) == 0:
            return None
        if var in reduced_list:
            csp.set_domain(unassigned_var, unassigned_var_domain)
    return sorted(reduced_list)


def domain_reduction(csp, queue=None) :

    if queue == None:
        queue = csp.get_all_variables()
    dequeued = []
    while not queue == []:
        var = queue.pop(0)
        dequeued.append(var)
        reduced_domains = eliminate_from_neighbors(csp, var)
        if reduced_domains == None:
            return None
        for reduced_domain in reduced_domains:
            if not reduced_domain in queue:
                queue.append(reduced_domain)
    return dequeued





#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""

    agenda = [problem]
    extension_count = 0

    while not agenda == []:
        current_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(current_problem):
            continue
        if not check_all_constraints(current_problem):
            continue

        if current_problem.unassigned_vars == []:
            return (current_problem.assigned_values, extension_count)

        new_p = []
        next_var = current_problem.pop_next_unassigned_var()


        for next_val in current_problem.get_domain(next_var):
            current_problem_copy = current_problem.copy()
            current_problem_copy.set_assigned_value(next_var, next_val)
            domain_reduction(current_problem_copy, [next_var])
            new_p.append(current_problem_copy)

        agenda = new_p + agenda

    return (None, extension_count)




#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""

    if queue == None:
        queue = csp.get_all_variables()
    dequeued = []
    while not queue == []:
        var = queue.pop(0)
        dequeued.append(var)
        reduced_domains = eliminate_from_neighbors(csp, var)
        if reduced_domains == None:
            return None
        for reduced_domain in reduced_domains:
            if not reduced_domain in queue:
                if len(csp.get_domain(reduced_domain)) == 1 :
                    queue.append(reduced_domain)
    return dequeued

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""


    agenda = [problem]
    extension_count = 0

    while not agenda == []:
        current_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(current_problem):
            continue
        if not check_all_constraints(current_problem):
            continue

        if current_problem.unassigned_vars == []:
            return (current_problem.assigned_values, extension_count)

        new_p = []
        next_var = current_problem.pop_next_unassigned_var()

        for next_val in current_problem.get_domain(next_var):
            current_problem_copy = current_problem.copy()
            current_problem_copy.set_assigned_value(next_var, next_val)

            domain_reduction_singleton_domains(current_problem_copy, [next_var])
            new_p.append(current_problem_copy)

        agenda = new_p + agenda

    return (None, extension_count)



#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""

    if queue == None:
        queue = csp.get_all_variables()
    dequeued = []
    while not queue == []:
        var = queue.pop(0)
        dequeued.append(var)
        reduced_domains = eliminate_from_neighbors(csp, var)
        if reduced_domains == None:
            return None
        for reduced_domain in reduced_domains:
            if not reduced_domain in queue:
                if enqueue_condition_fn(csp, reduced_domain):
                #if len(csp.get_domain(reduced_domain)) == 1 :
                    queue.append(reduced_domain)
    return dequeued

def condition_domain_reduction(csp, var) :
    return True
    raise NotImplementedError

def condition_singleton(csp, var) :

    if len(csp.get_domain(var)) == 1:
        return True
    return False


def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""


    agenda = [problem]
    extension_count = 0

    while not agenda == []:
        current_problem = agenda.pop(0)
        extension_count += 1
        if has_empty_domains(current_problem):
            continue
        if not check_all_constraints(current_problem):
            continue

        if current_problem.unassigned_vars == []:
            return (current_problem.assigned_values, extension_count)

        new_p = []
        next_var = current_problem.pop_next_unassigned_var()

        for next_val in current_problem.get_domain(next_var):
            current_problem_copy = current_problem.copy()
            current_problem_copy.set_assigned_value(next_var, next_val)
            if not enqueue_condition == None:
                propagate(enqueue_condition, current_problem_copy, [next_var])
            new_p.append(current_problem_copy)

        agenda = new_p + agenda

    return (None, extension_count)


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""

    if abs (m-n) == 1:
        return True
    return False


def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""

    if abs (m-n) == 1:
        return False
    return True

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            constraints.append(Constraint(variables[i],variables[j], constraint_different))
    return constraints
