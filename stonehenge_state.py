"""
An implementation of a state for Stonehenge
"""
from typing import Any, List
from game_state import GameState


class StonehengeState(GameState):
    """
    The state of the Stonehenge game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, side_length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.

        >>> s1 = StonehengeState(True, 1)
        >>> s1.ley_line
        {1: [1, 2], 2: [4], 3: [2], 4: [1, 4], 5: [1], 6: [2, 4]}
        >>> s1.side_length
        1
        >>> s1.p1_turn
        True
        """
        super().__init__(is_p1_turn)
        self.side_length = side_length
        self.ley_line = {}
        self.is_done = False
        self.ley_line_state = {}
        self.cells = {}
        self.ley_line_count = {}
        amount_cells = (self.side_length**2 + 5*self.side_length)//2
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(amount_cells):
            if i >= amount_cells - self.side_length and self.side_length < 5:
                self.cells['c' + str(i + 2)] = alphabet[i]
            else:
                self.cells['c' + str(i + 1)] = alphabet[i]
        for i in range(1, 3*(self.side_length+1)+1):
            self.ley_line_state[i] = '@'
            self.ley_line_count[i] = [0, 0]

        lst_diaglines = [[1, 3, 6, 10, 15], [2, 4, 7, 11, 16, 21],
                         [5, 8, 12, 17, 22], [9, 13, 18, 23],
                         [14, 19, 24], [20, 25]]
        lst_straight_lines = [[1, 2], [3, 4, 5], [6, 7, 8, 9],
                              [10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20],
                              [21, 22, 23, 24, 25]]
        lst_diag_up_left = [[2, 5, 9, 14, 20], [1, 4, 8, 13, 19, 25],
                            [3, 7, 12, 18, 24], [6, 11, 17, 23],
                            [10, 16, 22], [15, 21]]
#       Following lines handle linking cell number to specific leylines
#       (down left, up left, straigth)
        j = 0
        k = 0
        m = 0
        for i in range(1, len(self.ley_line_state)+1):
            if i > len(self.ley_line_state)-(self.side_length+1):
                self.ley_line[i] = [x for x in lst_diaglines[j] if
                                    'c' + str(x) in self.cells]
                j += 1
            if i <= self.side_length + 1:
                self.ley_line[i] = [x for x in lst_straight_lines[k] if
                                    'c' + str(x) in self.cells]
                k += 1
            if self.side_length + 1 < i <= \
                    len(self.ley_line_state) - (self.side_length + 1):

                self.ley_line[i] = [x for x in lst_diag_up_left[m]
                                    if 'c' + str(x) in self.cells]
                m += 1

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.

        >>> s1= StonehengeState(True,2)
        >>> print(s1)
                  @   @
                 /   /
            @ - A - B   @
               / \\ / \\ /
         @  - C - D - E
               \\ / \\ / \\
            @ - F - G   @
                 \\   \\
                  @   @
        """
        board = '            '
        if self.side_length == 1:
            board = ("      {}   ".format(self.ley_line_state[5]) +
                     "{}\n    ".format(self.ley_line_state[6]) +
                     " /   /\n{} - {} - ".format(self.ley_line_state[1],
                                                 self.cells['c1']) +
                     "{}\n     \\ / \\\n {}  ".format(self.cells['c2'],
                                                      self.ley_line_state[2]) +
                     "- {}   {}\n   ".format(self.cells['c4'],
                                             self.ley_line_state[3]) +
                     "    \\\n        {}".format(self.ley_line_state[4]))
        elif self.side_length == 2:
            board = "          {}   ".format(self.ley_line_state[7]) + \
                    "{}\n    ".format(self.ley_line_state[8]) + \
                    "     /   /\n    {} - ".format(self.ley_line_state[1]) +\
                    "{} - ".format(self.cells['c1']) + \
                    "{}   {}\n       ".format(self.cells['c2'],
                                              self.ley_line_state[9]) +\
                    "/ \\ / \\ /\n " \
                    "{} ".format(self.ley_line_state[2]) + \
                    " - {} - {} - ".format(self.cells['c3'],
                                           self.cells['c4']) +\
                    "{}\n   ".format(self.cells['c5']) + \
                    "    \\ / \\ / \\\n   " +\
                    " {} - {} -".format(self.ley_line_state[3],
                                        self.cells['c7']) +\
                    " {}   {}".format(self.cells['c8'],
                                      self.ley_line_state[4]) +\
                    "\n         \\   \\" +\
                    "\n          {}   ".format(self.ley_line_state[6]) + \
                    "{}".format(self.ley_line_state[5])
        elif self.side_length == 3:
            board = "          {}   ".format(self.ley_line_state[9]) + \
                    "{}\n    ".format(self.ley_line_state[10]) + \
                    "     /   /\n    {} - ".format(self.ley_line_state[1]) + \
                    "{} - ".format(self.cells['c1']) + \
                    "{}   {}\n       ".format(self.cells['c2'],
                                              self.ley_line_state[11]) + \
                    "/ \\ / \\ / \n " \
                    "{} ".format(self.ley_line_state[2]) + \
                    " - {} - {} - ".format(self.cells['c3'],
                                           self.cells['c4']) + \
                    "{}   {}\n   ".format(self.cells['c5'],
                                          self.ley_line_state[12]) + \
                    "  / \\ / \\ / \\ / \n" + \
                    "{} - {} - {} - {} - {}".format(self.ley_line_state[3],
                                                    self.cells['c6'],
                                                    self.cells['c7'],
                                                    self.cells['c8'],
                                                    self.cells['c9']) + \
                    "\n     \\ / \\ / \\ / \\" +\
                    "\n  {} - {} - {} - {}   {}".format(self.ley_line_state[4],
                                                        self.cells['c11'],
                                                        self.cells['c12'],
                                                        self.cells['c13'],
                                                        self.ley_line_state[5])\
                    + \
                    "\n       \\   \\   \\\n" +\
                    "        {}   {}   {}".format(self.ley_line_state[8],
                                                  self.ley_line_state[7],
                                                  self.ley_line_state[6])

        elif self.side_length == 4:
            board = "            {}   ".format(self.ley_line_state[11]) + \
                    "{}\n   ".format(self.ley_line_state[12]) + \
                    "        /   /\n      {} - ".format(
                        self.ley_line_state[1]) + \
                    "{} - ".format(self.cells['c1']) + \
                    "{}   {}\n       ".format(self.cells['c2'],
                                              self.ley_line_state[13]) + \
                    "  / \\ / \\ / \n " \
                    "   {} ".format(self.ley_line_state[2]) + \
                    "- {} - {} -".format(self.cells['c3'],
                                         self.cells['c4']) + \
                    " {}   {}\n   ".format(self.cells['c5'],
                                           self.ley_line_state[14]) + \
                    "    / \\ / \\ / \\ / \n" + \
                    "  {} - {} - {} - {} - {}   {}".format(
                        self.ley_line_state[3], self.cells['c6'],
                        self.cells['c7'], self.cells['c8'],
                        self.cells['c9'], self.ley_line_state[15]) + \
                    "\n     / \\ / \\ / \\ / \\ /" +\
                    "\n{} - {} - {} - {} - {} - {}".format(
                        self.ley_line_state[4], self.cells['c10'],
                        self.cells['c11'], self.cells['c12'],
                        self.cells['c13'], self.cells['c14']) +\
                    "\n     \\ / \\ / \\ / \\ / \\\n" +\
                    "  {} - {} - {} - {} - {}   {}\n".format(
                        self.ley_line_state[5], self.cells['c16'],
                        self.cells['c17'], self.cells['c18'],
                        self.cells['c19'], self.ley_line_state[6]) + \
                    "       \\   \\   \\   \\ \n" + \
                    "        {}   {}   {}   {}".format(self.ley_line_state[10],
                                                       self.ley_line_state[9],
                                                       self.ley_line_state[8],
                                                       self.ley_line_state[7])
        elif self.side_length == 5:
            board = "              {}   ".format(self.ley_line_state[13]) + \
                    "{}\n     ".format(self.ley_line_state[14]) + \
                    "        /   /\n        {} - ".format(
                        self.ley_line_state[1]) + \
                    "{} - ".format(self.cells['c1']) + \
                    "{}   {}\n         ".format(self.cells['c2'],
                                                self.ley_line_state[15]) + \
                    "  / \\ / \\ / \n   " \
                    "   {} ".format(self.ley_line_state[2]) + \
                    "- {} - {} -".format(self.cells['c3'],
                                         self.cells['c4']) + \
                    " {}   {}\n   ".format(self.cells['c5'],
                                           self.ley_line_state[16]) + \
                    "      / \\ / \\ / \\ / \n" + \
                    "    {} - {} - {} - {} - {}   {}".format(
                        self.ley_line_state[3], self.cells['c6'],
                        self.cells['c7'], self.cells['c8'],
                        self.cells['c9'], self.ley_line_state[17]) + \
                    "\n       / \\ / \\ / \\ / \\ /" + \
                    "\n  {} - {} - {} - {} - {} - {}   {}".format(
                        self.ley_line_state[4], self.cells['c10'],
                        self.cells['c11'], self.cells['c12'],
                        self.cells['c13'], self.cells['c14'],
                        self.ley_line_state[18]) + \
                    "\n     / \\ / \\ / \\ / \\ / \\ / \n" + \
                    "{} - {} - {} - {} - {} - {} - {} \n".format(
                        self.ley_line_state[5], self.cells['c15'],
                        self.cells['c16'],
                        self.cells['c17'], self.cells['c18'],
                        self.cells['c19'], self.cells['c20']) + \
                    "     \\ / \\ / \\ / \\ / \\ / \\ \n" + \
                    "  {} - {} - {} - {} - {} - {}   {}\n".format(
                        self.ley_line_state[6], self.cells['c21'],
                        self.cells['c22'], self.cells['c23'],
                        self.cells['c24'], self.cells['c25'],
                        self.ley_line_state[7]) + \
                    "       \\   \\   \\   \\   \\ \n" + \
                    "        {}   {}   {}   {}   {}".format(
                        self.ley_line_state[12], self.ley_line_state[11],
                        self.ley_line_state[10], self.ley_line_state[9],
                        self.ley_line_state[8])
        return board

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.

        >>> s1 = StonehengeState(True, 3)
        >>> s1.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        >>> s2 = s1.make_move('A')
        >>> s2.get_possible_moves()
        ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        """
        moves = []
        count_claimed_p2 = 0
        count_claimed_p1 = 0
        even_amount = len(self.ley_line_state) % 2 == 0
        for leyline in self.ley_line_state:
            if self.ley_line_state[leyline] == 1:
                count_claimed_p1 += 1
            elif self.ley_line_state[leyline] == 2:
                count_claimed_p2 += 1
        if (count_claimed_p1 >= len(self.ley_line_state) // 2 or
                count_claimed_p2 >= len(self.ley_line_state) // 2) and \
                even_amount:
            self.is_done = True
        elif (count_claimed_p1 > len(self.ley_line_state) // 2 or
              count_claimed_p2 > len(self.ley_line_state) // 2) and \
                not even_amount:
            self.is_done = True
        if not self.is_done:
            moves.extend([self.cells[c] for c in self.cells
                          if self.cells[c] != 1 and self.cells[c] != 2])
        return moves

    def make_move(self, move: Any) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.

        >>> s1 = StonehengeState(True, 3)
        >>> s1
        P1\'s Turn: True
        Leyline\'s captured by p1: 0 - Leyline\'s captured by p2: 0
        >>> s2 = s1.make_move('K')
        >>> s3 = s2.make_move('A')
        >>> s3 == s1
        False
        >>> s3 != s2
        True
        >>> s3
        P1\'s Turn: True
        Leyline\'s captured by p1: 0 - Leyline\'s captured by p2: 1
        """
        if not self.is_valid_move(move):
            return self
        move_equiv = ''
        new_state = StonehengeState(not self.p1_turn, self.side_length)
        for cell in self.cells:
            new_state.cells[cell] = self.cells[cell]
            if move == self.cells[cell]:
                new_state.cells[cell] = 1 if self.p1_turn else 2
                move_equiv = int(cell[1:])
        for leyline in self.ley_line:
            new_state.ley_line[leyline] = self.ley_line[leyline]
#           Add old count of cells in leyline captured to new_state's count
            for i in range(len(self.ley_line_count[leyline])):
                new_state.ley_line_count[leyline][i] += \
                    self.ley_line_count[leyline][i]
            new_state.ley_line_state[leyline] = self.ley_line_state[leyline]
#           increments amount of cells in leyline captured by player
            if move_equiv in self.ley_line[leyline] and self.p1_turn:
                new_state.ley_line_count[leyline][0] += 1
            elif move_equiv in self.ley_line[leyline] and not self.p1_turn:
                new_state.ley_line_count[leyline][1] += 1
        for leyline in self.ley_line:
            even_leyline = len(new_state.ley_line[leyline]) % 2 == 0
            amount_leyline_to_capture = len(new_state.ley_line[leyline]) // 2
            check_unclaimed = new_state.ley_line_state[leyline] == '@'
            # if the amount of captured cells in leyline are greater than
            # its length change its state
            for count in new_state.ley_line_count[leyline]:
                if count > 0 and count >= \
                        amount_leyline_to_capture and \
                        even_leyline and check_unclaimed:
                    new_state.ley_line_state[leyline] = \
                        new_state.ley_line_count[leyline].index(count) + 1
                elif count > 0 and count > \
                        amount_leyline_to_capture and \
                        not even_leyline and check_unclaimed:
                    new_state.ley_line_state[leyline] = \
                        new_state.ley_line_count[leyline].index(count) + 1
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).

        >>> s1 = StonehengeState(True, 2)
        >>> s1
        P1\'s Turn: True
        Leyline\'s captured by p1: 0 - Leyline\'s captured by p2: 0
        >>> s2 = s1.make_move('A')
        >>> s2
        P1\'s Turn: False
        Leyline\'s captured by p1: 2 - Leyline\'s captured by p2: 0
        """
        leylines_cap_p1 = [self.ley_line_state[leyline] for leyline in
                           self.ley_line_state].count(1)
        leylines_cap_p2 = [self.ley_line_state[leyline] for leyline in
                           self.ley_line_state].count(2)
        string = "P1\'s Turn: {}\n".format(str(self.p1_turn)) + \
                 "Leyline\'s captured by p1: {} - Leyline\'s captured by p2: " \
                 "{}".format(str(leylines_cap_p1), str(leylines_cap_p2))
        return string

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.

        >>> s1 = StonehengeState(True, 2)
        >>> s2 = s1.make_move('A')
        >>> s3 = s2.make_move('C')
        >>> s3 = s3.make_move('D')
        >>> s3.rough_outcome()
        -1
        """
        moves_lst = self.get_possible_moves()
        starting_player = self.get_current_player_name()
        if moves_lst == []:
            return self.LOSE
        score_lst = sum([check_state(self, move, starting_player)
                         for move in moves_lst], [])
        return max(score_lst)


def check_state(state: 'StonehengeState', move: Any, starting_player: str)\
        -> List[int]:
    """ Return best possible score from state and from move
    looking two states ahead

    >>> s1 = StonehengeState(True, 1)
    >>> check_state(s1, 'A', 'p1')
    [1]
    """
    state1 = state.make_move(move)
    moves_lst = state1.get_possible_moves()
    outcome_lst = []
    if moves_lst == []:
        return [state.WIN]
    for new_move in moves_lst:
        state2 = state1.make_move(new_move)
        new_lst = state2.get_possible_moves()
        if new_lst == []:
            return [state.LOSE]
        count_claimed_p1 = 0
        count_claimed_p2 = 0
        for leyline in state2.ley_line_state:
            if state2.ley_line_state[leyline] == 1:
                count_claimed_p1 += 1
            elif state2.ley_line_state[leyline] == 2:
                count_claimed_p2 += 1
        if starting_player == 'p1':
            outcome_lst.append(count_claimed_p1 / len(state2.ley_line))
        else:
            outcome_lst.append(count_claimed_p2 / len(state2.ley_line))

    return outcome_lst


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a2_pyta.txt")
