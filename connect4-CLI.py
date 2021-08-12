import time

class Game:
    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        self.rows = 6
        self.columns = 7
        self.board = [['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.']]

        # Player X always plays first
        self.player_turn = 'X'

        # self.treeDepth can be set to higher or lower values
        self.tree_depth = 3
        
    def draw_board(self):
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                print('{}|'.format(self.board[r][c]), end=" ")
            print()
        print()

    # Determines if the made move is a legal move
    def is_valid(self, px):
        py = self.get_row_from_col(px)
        if px < 0 or px > (self.columns-1):
            return False
        elif self.board[0][px] != '.':
            return False
        else:
            return True

    # Given a choosen column to put a token ('X' or 'O')
    # it return the row where the token will land
    def get_row_from_col(self, c):
        r = 0
        for br in range((self.rows-1), -1, -1):
            if self.board[br][c] == '.':
                r = br
                break

        return r

    # Heuristic to get actual board score according to a specific player
    def h(self, player):
        opponent = 'X' if player == 'O' else 'O'
        position = {
            player: '',
            opponent: '',
            '.': ''
        }
        data = {
            'V': [],
            'H': [],
            'MD': [],
            'SD': []
        }

        # It's time to fill 'data' structure with board lines
        # (vertical lines, horizontal lines, main diagonal lines, second diagonal lines)

        # Vertical
        for c in range(0, self.columns):
            for r in range(0, self.rows):
                position[self.board[r][c]] += str(r) + '|'

            position[player] = position[player][:-1]
            position[opponent] = position[opponent][:-1]
            position['.'] = position['.'][:-1]

            data['V'].append(position)
            position = {
                player: '',
                opponent: '',
                '.': ''
            }

        # Horizontal
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                position[self.board[r][c]] += str(c) + '|'

            position[player] = position[player][:-1]
            position[opponent] = position[opponent][:-1]
            position['.'] = position['.'][:-1]

            data['H'].append(position)
            position = {
                player: '',
                opponent: '',
                '.': ''
            }

        # Main diagonal
        r = 2
        c = 0

        for i in range(0, 6):
            j = 0

            r1 = r
            c1 = c

            while r1 >= 0 and c1 >= 0 and c1 < self.columns and r1 < self.rows:
                position[self.board[r1][c1]] += str(j) + '|'
                r1 += 1
                c1 += 1
                j += 1



            position[player] = position[player][:-1]
            position[opponent] = position[opponent][:-1]
            position['.'] = position['.'][:-1]

            data['MD'].append(position)
            position = {
                player: '',
                opponent: '',
                '.': ''
            }

            tmp_r = r
            if tmp_r > 0:
                r -= 1
            if (c == 0 and tmp_r == 0) or c > 0:
                c += 1

        # Second diagonal
        r = self.rows - 1
        c = 3

        for i in range(0, 6):
            j = 0

            r1 = r
            c1 = c

            while r1 >= 0 and c1 >= 0 and c1 < self.columns and r1 < self.rows:
                position[self.board[r1][c1]] += str(j) + '|'
                r1 -= 1
                c1 += 1
                j += 1

            position[player] = position[player][:-1]
            position[opponent] = position[opponent][:-1]
            position['.'] = position['.'][:-1]

            data['SD'].append(position)
            position = {
                player: '',
                opponent: '',
                '.': ''
            }

            tmp_c = c
            if tmp_c > 0:
                c -= 1
            if (r == self.rows-1 and tmp_c == 0) or r < self.rows - 1:
                r -= 1

        # Data in desired form.

        # Now calculating board score from 0 to 1000 (the score won't never reach 1000)
        # and then normalizing it to get a value from 0 to 1 (but not 1 !!).

        #It's important to remember that:
        # 1 means a victory for current player
        # -1 means a defeat for current player
        # 0 means a tie

        # So, each board where the game is not over, can't reach a value of
        # -1 or 1 because they are the bounds of the board score that mean the game is over.
        # 1 is the best value (victory), -1 is the worst value (defeat).

        score = 0
        for k in data:
            for d in data[k]:
                if len(d[player]) != 0:
                    pos = [int(i) for i in d[player].split('|')]
                    tot = len(d[player].replace('|','')) + len(d[opponent].replace('|','')) + len(d['.'].replace('|',''))

                    for p in pos:

                        #Check left
                        partial_score = 0
                        counter_1 = 0
                        counter_2 = 0
                        for i in range(-3,0,1): #-3,-2,-1
                            adj = p + i
                            if adj >= 0 and adj < tot:
                                if str(adj) in d['.']:
                                    partial_score += 1
                                    counter_1 += 1
                                elif str(adj) in d[player]:
                                    partial_score += 2
                                    counter_1 += 1
                                else:
                                    partial_score -= 1
                                    counter_2 += 1

                        if counter_1 == 3:
                            score += partial_score
                        if counter_2 == 2:
                            score += 5

                        #Check right
                        partial_score = 0
                        counter_1 = 0
                        for i in range(1,4,1): #1,2,3
                            adj = p + i
                            if adj >= 0 and adj < tot:
                                if str(adj) in d['.']:
                                    partial_score += 1
                                    counter_1 += 1
                                elif str(adj) in d[player]:
                                    partial_score += 2
                                    counter_1 += 1
                                else:
                                    partial_score -= 1
                                    counter_2 += 1

                        if counter_1 == 3:
                            score += partial_score
                        if counter_2 == 2:
                            score += 5

                        if counter_2 >= 3:
                            score += 30



        return score / 1000


    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        # Check if someone has won
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                if self.board[r][c] != '.':

                    # Vertical win
                    adjacents = 0
                    for v in range(-3, 4):
                        if r+v >= 0 and r+v < self.rows:
                            if self.board[r+v][c] == self.board[r][c]:
                                adjacents += 1
                            else:
                                adjacents = 0
                    if adjacents == 4:
                        return self.board[r][c]


                    # Horizontal win
                    adjacents = 0
                    for v in range(-3, 4):
                        if c+v >= 0 and c+v < self.columns:
                            if self.board[r][c+v] == self.board[r][c]:
                                adjacents += 1
                            else:
                                adjacents = 0
                    if adjacents == 4:
                        return self.board[r][c]

                    # Main diagonal win
                    adjacents = 0
                    for v in range(-3, 4):
                        if c+v >= 0 and r+v >= 0 and c+v < self.columns and r+v < self.rows:
                            if self.board[r+v][c+v] == self.board[r][c]:
                                adjacents += 1
                            else:
                                adjacents = 0
                    if adjacents == 4:
                        return self.board[r][c]


                    # Second diagonal win
                    adjacents = 0
                    for v in range(-3, 4):
                        if c+v >= 0 and r-v >= 0 and c+v < self.columns and r-v < self.rows:
                            if self.board[r-v][c+v] == self.board[r][c]:
                                adjacents += 1
                            else:
                                adjacents = 0
                    if adjacents == 4:
                        return self.board[r][c]


        # Is whole board full?
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                # There's an empty field, we continue the game
                if (self.board[r][c] == '.'):
                    return None

        # It's a tie!
        return '.'

    # Player 'O' is max, in this case AI
    def max(self, current_depth):

        player = 'O'

        # Possible values for maxv are:
        # -1 - loss
        # 0  - a tie
        # 1  - win

        # We're initially setting it to -2 as worse than the worst case:
        maxv = -2

        px = None

        result = self.is_end()

        # If the game came to an end, the function needs to return
        # the evaluation function of the end. That can be:
        # -1 - loss
        # 0  - a tie
        # 1  - win
        if result == 'X':
            return (-1, 0)
        elif result == 'O':
            return (1, 0)
        elif result == '.':
            return (0, 0)

        for c in range(0, self.columns):
            r = self.get_row_from_col(c)

            if self.board[r][c] == '.':
                # On the empty field player 'O' makes a move and calls Min
                # That's one branch of the game tree.
                self.board[r][c] = player
                if (current_depth < self.tree_depth):
                    current_depth += 1
                    (m, _) = self.min(current_depth)
                else:
                    result = self.is_end()
                    m = None
                    if result == 'X':
                        m = -1
                    elif result == 'O':
                        m = 1
                    elif result == '.':
                        m = 0

                    if m == None:
                        m = self.h(player)

                    #if self.player_turn == 'O':
                    #    print('col: ' + str(c))
                    #    print('m: ' + str(m))
                    #    print()


                # Fixing the maxv value if needed
                if m > maxv:
                    maxv = m
                    px = c
                    
                # Setting back the field to empty
                self.board[r][c] = '.'

        return (maxv, px)

    # Player 'X' is min, in this case human
    def min(self, current_depth):

        player = 'X'

        # Possible values for minv are:
        # -1 - win
        # 0  - a tie
        # 1  - loss

        # We're initially setting it to 2 as worse than the worst case:
        minv = 2

        qx = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0)
        elif result == 'O':
            return (1, 0)
        elif result == '.':
            return (0, 0)

        for c in range(0, self.columns):
            r = self.get_row_from_col(c)

            if self.board[r][c] == '.':
                self.board[r][c] = player
                if (current_depth < self.tree_depth):
                    current_depth += 1
                    (m, _) = self.max(current_depth)
                else:
                    result = self.is_end()
                    m = None
                    if result == 'X':
                        m = -1
                    elif result == 'O':
                        m = 1
                    elif result == '.':
                        m = 0

                    if m == None:
                        m = self.h(player)

                if m < minv:
                    minv = m
                    qx = c

                self.board[r][c] = '.'

        return (minv, qx)

    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            # If it's player's turn
            if self.player_turn == 'X':

                while True:

                    start = time.time()
                    current_depth = 0
                    (m, qx) = self.min(current_depth)
                    end = time.time()

                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    print('Recommended move: Col = {}'.format(qx))

                    px = int(input('Choose your column (0-{}): '.format(self.columns-1)))


                    if self.is_valid(px):
                        py = self.get_row_from_col(px)
                        self.board[py][px] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('The move is not valid! Try again.')

            # If it's AI's turn
            else:
                current_depth = 0
                (m, px) = self.max(current_depth)
                py = self.get_row_from_col(px)
                self.board[py][px] = 'O'
                self.player_turn = 'X'

def main():
    g = Game()
    g.play()

if __name__ == "__main__":
    main()
