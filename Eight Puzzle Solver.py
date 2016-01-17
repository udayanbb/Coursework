'''
Puzzle data structure for the 8-puzzle.
'''

class Puzzle:
    def __init__(self, starting_state):
        self.initial_state = starting_state
        self.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    def next_states(self, s):
        ans = []
        t = []
        s = list(s)
        #Corner States
        if s[0] == 0:
            t = s[:]
            t[0] = t[1]
            t[1] = 0
            ans.append(tuple(t))
            t = s[:]
            t[0] = t[3]
            t[3] = 0
            ans.append(tuple(t))
        if s[2] == 0:
            t = s[:]
            t[2] = t[1]
            t[1] = 0
            ans.append(tuple(t))
            t = s[:]
            t[2] = t[5]
            t[5] = 0
            ans.append(tuple(t))
        if s[6] == 0:
            t = s[:]
            t[6] = t[3]
            t[3] = 0
            ans.append(tuple(t))
            t = s[:]
            t[6] = t[7]
            t[7] = 0
            ans.append(tuple(t))
        if s[8] == 0:
            t = s[:]
            t[8] = t[5]
            t[5] = 0
            ans.append(tuple(t))
            t = s[:]
            t[8] = t[7]
            t[7] = 0
            ans.append(tuple(t))

        #Centre Edge States
        if s[1] == 0:
            t = s[:]
            t[1] = t[0]
            t[0] = 0
            ans.append(tuple(t))
            t = s[:]
            t[1] = t[2]
            t[2] = 0
            ans.append(tuple(t))
            t = s[:]
            t[1] = t[4]
            t[4] = 0
            ans.append(tuple(t))
        if s[3] == 0:
            t = s[:]
            t[3] = t[0]
            t[0] = 0
            ans.append(tuple(t))
            t = s[:]
            t[3] = t[4]
            t[4] = 0
            ans.append(tuple(t))
            t = s[:]
            t[3] = t[6]
            t[6] = 0
            ans.append(tuple(t))
        if s[5] == 0:
            t = s[:]
            t[5] = t[2]
            t[2] = 0
            ans.append(tuple(t))
            t = s[:]
            t[5] = t[4]
            t[4] = 0
            ans.append(tuple(t))
            t = s[:]
            t[5] = t[8]
            t[8] = 0
            ans.append(tuple(t))
        if s[7] == 0:
            t = s[:]
            t[7] = t[6]
            t[6] = 0
            ans.append(tuple(t))
            t = s[:]
            t[7] = t[4]
            t[4] = 0
            ans.append(tuple(t))
            t = s[:]
            t[7] = t[8]
            t[8] = 0
            ans.append(tuple(t))

        if s[4] == 0:
            t = s[:]
            t[4] = t[1]
            t[1] = 0
            ans.append(tuple(t))
            t = s[:]
            t[4] = t[3]
            t[3] = 0
            ans.append(tuple(t))
            t = s[:]
            t[4] = t[5]
            t[5] = 0
            ans.append(tuple(t))
            t = s[:]
            t[4] = t[7]
            t[7] = 0
            ans.append(tuple(t))
        s = tuple(s)
        return ans

'''
solve_puzzle(P): given an 8-puzzle data structure, returns the shortest sequence
of states that can be used to solve the puzzle
ARGS:
  P - the 8-puzzle, with initial_state, goal_state, and next_states(s) defined
RETURN:
  the sequence of states used to solve the puzzle in the fewest moves (as a
  list); if there are no possible solutions, return the empty list, and if the
  starting state equals the ending state, return a list containing only the
  ending state
'''
def solve_puzzle(P):
    agenda = []
    agenda.append([P.initial_state])

    seen = set()
    seen.add(str(P.initial_state))

    while not agenda == []:
        current_state = agenda.pop(0)

        if(current_state[-1]) == P.goal_state:
            return current_state

        new_states = P.next_states(current_state[-1])
        for state in new_states:
            if not state in seen:
                new_state = current_state[:]
                new_state.append(state)
                agenda.append(new_state)
                seen.add(state)


    return []

'''
# Some examples (be sure to comment them out before submitting)

# Part (a)
s = (1, 2, 3, 4, 0, 6, 7, 5, 8)
P = Puzzle(s)
print P.initial_state
# (1, 2, 3, 4, 0, 6, 7, 5, 8)

print P.goal_state
# (1, 2, 3, 4, 5, 6, 7, 8, 0)
next = P.next_states(s)
for state in next:
    print state


# (1, 0, 3, 4, 2, 6, 7, 5, 8)
# (1, 2, 3, 0, 4, 6, 7, 5, 8)
# (1, 2, 3, 4, 6, 0, 7, 5, 8)
# (1, 2, 3, 4, 5, 6, 7, 0, 8)


# Part (b)
solution = solve_puzzle(P)
for state in solution:
    print state
# (1, 2, 3, 4, 0, 6, 7, 5, 8)
# (1, 2, 3, 4, 5, 6, 7, 0, 8)
# (1, 2, 3, 4, 5, 6, 7, 8, 0)

'''
