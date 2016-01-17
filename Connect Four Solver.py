from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    if board.count_pieces() == board.num_rows * board.num_cols:
        return True
    else:
        sizes = [len(chain) for chain in board.get_all_chains()]
        if len(sizes) == 0:
            return False
        elif max(sizes) == 4:
            return True
        else:
            return False


def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    moves = []
    for x in range(board.num_cols):
        if board.is_column_full(x) == False:
            new_board = board.add_piece(x)
            moves.append(new_board)
    return moves


def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""

    player1max = max([len(chain) for chain in board.get_all_chains(False)])

    if player1max == 4:
        if is_current_player_maximizer:
            return -1000
        else:
            return 1000
    else:
        if is_current_player_maximizer:
            return 1000
        else:
            return -1000


    raise NotImplementedError

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""

    player1max = max([len(chain) for chain in board.get_all_chains(False)])

    score = 1000 * (board.num_rows * board.num_cols - board.count_pieces())

    if player1max == 4:
        if is_current_player_maximizer:
            return -score
        else:
            return score
    else:
        if is_current_player_maximizer:
            return score
        else:
            return -score


def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""


    scores_1 = sum([pow(len(chain),2) for chain in board.get_all_chains(True)])
    scores_2 = sum([pow(len(chain),2) for chain in board.get_all_chains(False)])

    if is_current_player_maximizer:
        return scores_1 - scores_2
    else :
        return scores_2 - scores_1


# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################


def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""

    ret = []

    if state.is_game_over():
        ret.append([state])
        ret.append(state.get_endgame_score(False))
        ret.append(1)
        return ret

    agenda = [[state]]

    current_best = 0
    tests = 0


    while not agenda == []:

        new_states = agenda[0][-1].generate_next_states()

        temp_new_states = new_states[:]
        for new_state in temp_new_states:
            if new_state.is_game_over():
                poss_max = abs(new_state.get_endgame_score())
                tests += 1
                if poss_max > current_best:
                    current_best = poss_max
                    #print 'Adding', new_state, 'to', agenda[0]
                    ret = [agenda[0] + [new_state], current_best]

                else:
                    new_states.remove(new_state)

        temp_new_states = new_states[:]
        new_states = []
        for new_state in temp_new_states:
            new_states.append(agenda[0] + [new_state])

        #print 'Final addition', new_states

        agenda = agenda[1:]
        agenda = new_states + agenda
        #print 'Final agenda', agenda
    ret.append(tests)

    return ret

state_done = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

#pretty_print_dfs_type(dfs_maximizing(state_done))

def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""

    if(state.is_game_over()):
        return [[state], state.get_endgame_score(True), 1]
    elif maximize:
        next_level = [minimax_endgame_search(test_state, False) for test_state in state.generate_next_states()]
        calls = sum([el[2] for el in next_level])
        return_case = max(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case
    else:
        next_level = [minimax_endgame_search(test_state, True) for test_state in state.generate_next_states()]
        calls = sum([el[2] for el in next_level])
        return_case = min(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case



'''
def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."


    if(state.is_game_over()):
       return [[state], state.get_endgame_score(True), 1]
    elif depth_limit ==  0:
        #print  'Limit reached'
        return [[state], heuristic_fn(state.get_snapshot(), True), 1]
    elif maximize:
        next_level = [minimax_search(test_state, heuristic_fn, depth_limit-1, False) for test_state in state.generate_next_states()]
        calls = sum([el[2] for el in next_level])
        return_case = max(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case
    else:
        next_level = [minimax_search(test_state, heuristic_fn, depth_limit-1, True) for test_state in state.generate_next_states()]
        calls = sum([el[2] for el in next_level])
        return_case = min(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case
'''

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."

    if(state.is_game_over()):
       return [[state], state.get_endgame_score(True), 1]
    elif depth_limit ==  0:
        #print  'Limit reached'
        return [[state], heuristic_fn(state.get_snapshot(), True), 1]
    elif maximize:
        next_states = state.generate_next_states()
        next_level = []
        for test_state in next_states:
            new_result = minimax_search(test_state, heuristic_fn, depth_limit-1, False)
            next_level.append(new_result)
        calls = sum([el[2] for el in next_level])
        return_case = max(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case
    else:
        next_states = state.generate_next_states()
        next_level = []
        for test_state in next_states:
            new_result = minimax_search(test_state, heuristic_fn, depth_limit-1, True)
            next_level.append(new_result)
        calls = sum([el[2] for el in next_level])
        return_case = min(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    #print 'Called with', depth_limit
    if(state.is_game_over()):
        return [[state], state.get_endgame_score(maximize), 1]
    elif depth_limit ==  0:
        #print  'Limit reached'
        return [[state], heuristic_fn(state.get_snapshot(), maximize), 1]
    elif maximize:
        next_states = state.generate_next_states()
        next_level = []
        for test_state in next_states:
            new_result = minimax_search_alphabeta(test_state, alpha, beta, heuristic_fn, depth_limit-1, False)
            alpha = max(alpha, new_result[1])
            next_level.append(new_result)
            if alpha >= beta:
                break
        calls = sum([el[2] for el in next_level])
        return_case = max(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case
    else:
        next_states = state.generate_next_states()
        next_level = []
        for test_state in next_states:
            new_result = minimax_search_alphabeta(test_state, alpha, beta, heuristic_fn, depth_limit-1, True)
            beta = min(beta, new_result[1])
            next_level.append(new_result)
            if alpha >= beta:
                break

        calls = sum([el[2] for el in next_level])
        return_case = min(next_level, key = lambda case: case[1])
        return_case[2] = calls
        return_case[0] = [state] + return_case[0]
        return return_case



def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.

    current_depth = 1

    if depth_limit == INF:
        anytime_value.set_value(minimax_search_alphabeta(state, -INF, INF, heuristic_fn, depth_limit, maximize))
        return anytime_value

    while current_depth <= depth_limit :
        #print 'Calling with no', current_depth
        anytime_value.set_value(minimax_search_alphabeta(state, -INF, INF, heuristic_fn, current_depth, maximize))
        current_depth += 1

    return anytime_value



