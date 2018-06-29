"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any, Union, List
from copy import deepcopy


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
    starting_player = game.current_state.get_current_player_name()
    if moves_lst == []:
        return 0
    score_lst = [get_move_score(game, move, starting_player)
                 for move in moves_lst]
    game.current_state = old_state
    max_score = max(score_lst)
    return moves_lst[score_lst.index(max_score)]


def get_move_score(game: Any, move: Any, starting_player: str) -> int:
    """ Return score of move on the state depending on the starting player
    """
    new_game1 = deepcopy(game)
    old_state = new_game1.current_state
    current_player = old_state.get_current_player_name()
    current_state = new_game1.current_state.make_move(move)

    new_game1.current_state = current_state
    new_moves_lst = new_game1.current_state.get_possible_moves()
    other_player = ''
    if current_player == "p1":
        other_player = "p2"
    elif current_player == "p2":
        other_player = "p1"
    if new_game1.current_state.get_possible_moves() == []:
        if new_game1.is_winner(current_player):
            return new_game1.current_state.WIN
        elif new_game1.is_winner(other_player):
            return new_game1.current_state.LOSE
        return new_game1.current_state.DRAW

    return -1 * max([get_move_score(new_game1, new_move, starting_player)
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


def iterative_strategy(game: Any) -> Any:
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
        if top_item.state.get_current_player_name() == 'p1':
            other_player = 'p2'
        else:
            other_player = "p1"
        game.current_state = top_item.state
        if top_item.state.get_possible_moves() == []:
            if game.is_winner(top_item.state.get_current_player_name()):
                top_item.score = top_item.state.LOSE
            elif game.is_winner(other_player):
                top_item.score = top_item.state.WIN
            else:
                top_item.score = top_item.state.DRAW
        elif top_item.children == [] or top_item.children is None:
            stack.append(top_item)
            for move in top_item.state.get_possible_moves():
                new_state = top_item.state.make_move(move)
                new_item = Tree(i, move, new_state, None)
                stack.append(new_item)
                top_item.children.append(new_item)
                i += 1
        elif top_item.children is not None:
            top_item.score = -1 * max([child.score for child in
                                       top_item.children])
            lst_states.append(top_item)
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
    Tree ADT that holds the score of the given state and the childrne and move
    made to get to the said state
    Attributes:
    - state: GameState of given game
    - children: child nodes
    - score: score of tree
    - id: id of tree
    """
    children: list
    state: object
    score: int
    id: int
    move_made: Any

    def __init__(self, identifier: int, move_made: Any = None,
                 state: Any = None,
                 children: List[Union['Tree', None]] = None):
        """
        Create Tree with a value of state and 0 or more children and
        score related to it and with an id

        """
        self.state = state
        self.children = children[:] if children is not None else []
        self.score = 0
        self.identifier = identifier
        self.move_made = move_made

    def __repr__(self):
        """
        Return string representation of Tree object
        """
        return "ID: {}, State: {}, Children: {}, Score: {}".format(
            self.identifier, self.state, self.children, self.score)


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
