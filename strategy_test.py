"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, List, Optional
from copy import deepcopy
from stonehenge_game import StonehengeGame
from subtract_square_game import SubtractSquareGame
from subtract_square_state import SubtractSquareState



def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def minimax_rec(game: Any) -> Any:
    """
    Return a best move possible for computer resulting
    in the lowest score for opponent
    """
    old_state = game.current_state
    moves_lst = game.current_state.get_possible_moves()
    if moves_lst == []:
        return 0
    score_lst = [get_move_score(game, move) for move in moves_lst]
    game.current_state = old_state
    print(score_lst)
    max_score = max(score_lst)
    return moves_lst[score_lst.index(max_score)]


def get_move_score(game: Any, move: Any) -> int:
    """ Return score of move on the state depending on the starting player
    """
    new_game1 = deepcopy(game)
    old_state = new_game1.current_state
    current_player = old_state.get_current_player_name()
    current_state = new_game1.current_state.make_move(move)

    new_game1.current_state = current_state
    new_moves_lst = new_game1.current_state.get_possible_moves()

    # new_game.current_state = state
    other_player = ''
    if current_player == "p1":
        other_player = "p2"
    elif current_player == "p2":
        other_player = "p1"
    if new_game1.current_state.get_possible_moves() == []:
        if new_game1.is_winner(current_player):
            return current_state.WIN
        elif new_game1.is_winner(other_player):
            return current_state.LOSE
        return current_state.DRAW

    return -1 * max([get_move_score(new_game1, new_move)
                     for new_move in new_moves_lst])


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def iterative_strategy(game: Any):
    """
    Return a best move possible for computer resulting
    in the lowest score for opponent
    """
    stack, lst_states = [], []
    stack.append(Tree(1, None, game.current_state, None))
    old_state = game.current_state
    i = 2
    while stack != []:
        top_item = stack.pop()
        if top_item.value.get_current_player_name() == 'p1':
            other_player = 'p2'
        else:
            other_player = "p1"
        game.current_state = top_item.value
        # print(game.current_state.get_current_player_name())
        if top_item.value.get_possible_moves() == []:
            game.current_state = top_item.value
            if game.is_winner(top_item.value.get_current_player_name()):
                top_item.score = top_item.value.LOSE
            elif game.is_winner(other_player):
                top_item.score = top_item.value.WIN
            else:
                top_item.score = top_item.value.DRAW
        elif top_item.children == [] or top_item.children is None:
            stack.append(top_item)
            for move in top_item.value.get_possible_moves():
                new_state = top_item.value.make_move(move)
                new_item = Tree(i, move, new_state, None)
                stack.append(new_item)
                top_item.children.append(new_item)
                i += 1
        elif top_item.children is not None:
            top_item.score = -1 * max([child.score for child in
                                       top_item.children])
            lst_states.append(top_item)
    print([child.score for child in lst_states[-1].children])
    if lst_states == []:
        return 0
    best_score = max([child.score for child in lst_states[-1].children])
    get_index_best_state = [child.score for child in
                            lst_states[-1].children].index(best_score)
    move_to_make = lst_states[-1].children[get_index_best_state].move_made
    shortest_len = 100000000000000  # Temporary will change
    for item in lst_states[-1].children:
        if item.score == best_score:
            if len(item.children) < shortest_len:
                shortest_len = len(item.children)
                move_to_make = item.move_made
    game.current_state = old_state
    return move_to_make


class Tree:
    """
    A bare-bones Tree ADT that identifies the root with the entire tree.
    === Attributes ===
    value: value of root node
    children: child nodes
    score: score of tree
    id: id of tree
    """
    children: list
    value: object
    score: int
    id: int
    move_made: Any

    def __init__(self, identifier: int, move_made: Any = None,
                 value=None, children=None):
        """
        Create Tree self with content value and 0 or more children and
        score related to it and with an id

        """
        self.value = value
        # copy children if not None
        # NEVER have a mutable default parameter...
        self.children = children[:] if children is not None else []
        self.score = 0
        self.identifier = identifier
        self.move_made = move_made

    def __repr__(self):
        """
        String representation of Tree object
        :return:
        :rtype:
        """
        return "ID: {}, Value: {}, Children: {}, Score: {}".format(
            self.identifier, self.value, self.children, self.score)


if __name__ == "__main__":
    # game = StonehengeGame(True)
    #
    # print(iterative_strategy(game))
    # print(minimax_rec(game))
    game = StonehengeGame(True)
    #
    # print(game.current_state)
    # print(game.current_state.get_current_player_name())
    # moves_lst = game.current_state.get_possible_moves()
    # print(moves_lst)
    gs = game.current_state
    gs = gs.make_move(game.str_to_move('B'))
    gs = gs.make_move(game.str_to_move('G'))
    gs = gs.make_move(game.str_to_move('D'))
    game.current_state = gs
    print(game.current_state.get_current_player_name())
    print(game.current_state)
    print(minimax_rec(game))
    print(iterative_strategy(game))
    # while not game.is_over(game.current_state):
    #     game.current_state = game.current_state.make_move(minimax_rec(game))
    #     print(game.current_state)
    #     game.current_state = game.current_state.make_move(minimax_rec(game))
    #     print(game.current_state)
    #

    from python_ta import check_all
    check_all(config="a2_pyta.txt")
