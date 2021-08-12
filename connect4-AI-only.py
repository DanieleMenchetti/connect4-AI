import sys

rows = 6
columns = 7

# Get input data
def get_input_data(filepath):

    # Getting player turn, tree depth, actual board from input file
    global player_turn
    global tree_depth
    global board
    global opponent

    try:
        f = open(filepath, 'r')
        lines = [x[:-1] for x in f.readlines()]
    except:
        print("E\nFile {0}: not found or unreadable".format(filepath), file=sys.stderr)
        quit()

    try:
        player_turn = lines[0][0]
        tree_depth = int(lines[1][0])

        board = []
        tmp_v = []
        for i in range(2, 8, 1):
            if len(lines[i]) != 14:
                raise Exception()
            for j, c in enumerate(lines[i]):
                if j % 2 == 0:
                    if c != '.' and c != 'X' and c != 'O':
                        raise Exception()
                    else:
                        tmp_v.append(c)
                else:
                    if c != '|':
                        raise Exception()

            board.append(tmp_v)
            tmp_v = []


    except:
        print("E\nFile {0}: bad format".format(filepath), file=sys.stderr)
        quit()


    # Get opponent
    opponent = 'X' if player_turn == 'O' else 'O'


# Given a choosen column to put a token ('X' or 'O')
# it return the row where the token will land
def get_row_from_col(c):
    r = 0
    for br in range((rows-1), -1, -1):
        if board[br][c] == '.':
            r = br
            break

    return r

# Heuristic to get actual board score according to a specific player
def h(player):

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
    for c in range(0, columns):
        for r in range(0, rows):
            position[board[r][c]] += str(r) + '|'

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
    for r in range(0, rows):
        for c in range(0, columns):
            position[board[r][c]] += str(c) + '|'

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

        while r1 >= 0 and c1 >= 0 and c1 < columns and r1 < rows:
            position[board[r1][c1]] += str(j) + '|'
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
    r = rows - 1
    c = 3

    for i in range(0, 6):
        j = 0

        r1 = r
        c1 = c

        while r1 >= 0 and c1 >= 0 and c1 < columns and r1 < rows:
            position[board[r1][c1]] += str(j) + '|'
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
        if (r == rows-1 and tmp_c == 0) or r < rows - 1:
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
def is_end():
    # Check if someone has won
    for r in range(0, rows):
        for c in range(0, columns):
            if board[r][c] != '.':

                # Vertical win
                adjacents = 0
                for v in range(-3, 4):
                    if r+v >= 0 and r+v < rows:
                        if board[r+v][c] == board[r][c]:
                            adjacents += 1
                        else:
                            adjacents = 0
                if adjacents == 4:
                    return board[r][c]


                # Horizontal win
                adjacents = 0
                for v in range(-3, 4):
                    if c+v >= 0 and c+v < columns:
                        if board[r][c+v] == board[r][c]:
                            adjacents += 1
                        else:
                            adjacents = 0
                if adjacents == 4:
                    return board[r][c]

                # Main diagonal win
                adjacents = 0
                for v in range(-3, 4):
                    if c+v >= 0 and r+v >= 0 and c+v < columns and r+v < rows:
                        if board[r+v][c+v] == board[r][c]:
                            adjacents += 1
                        else:
                            adjacents = 0
                if adjacents == 4:
                    return board[r][c]


                # Second diagonal win
                adjacents = 0
                for v in range(-3, 4):
                    if c+v >= 0 and r-v >= 0 and c+v < columns and r-v < rows:
                        if board[r-v][c+v] == board[r][c]:
                            adjacents += 1
                        else:
                            adjacents = 0
                if adjacents == 4:
                    return board[r][c]


    # Is whole board full?
    for r in range(0, rows):
        for c in range(0, columns):
            # There's an empty field, we continue the game
            if (board[r][c] == '.'):
                return None

    # It's a tie!
    return '.'

def max(current_depth):

    # Possible values for maxv are:
    # -1 - loss
    # 0  - a tie
    # 1  - win

    # We're initially setting it to -2 as worse than the worst case:
    maxv = -2

    px = None

    result = is_end()

    # If the game came to an end, the function needs to return
    # the evaluation function of the end. That can be:
    # -1 - loss
    # 0  - a tie
    # 1  - win
    if result == opponent:
        return (-1, 0)
    elif result == player_turn:
        return (1, 0)
    elif result == '.':
        return (0, 0)

    for c in range(0, columns):
        r = get_row_from_col(c)

        if board[r][c] == '.':
            # On the empty field player player_turn makes a move and calls Min
            # That's one branch of the game tree.
            board[r][c] = player_turn
            if (current_depth < tree_depth):
                current_depth += 1
                (m, _) = min(current_depth)
            else:

                result = is_end()

                m = None
                if result == opponent:
                    m = -1
                elif result == player_turn:
                    m = 1
                elif result == '.':
                    m = 0

                if m == None:
                    m = h(player_turn)


            # Fixing the maxv value if needed
            if m > maxv:
                maxv = m
                px = c
                
            # Setting back the field to empty
            board[r][c] = '.'

    return (maxv, px)

def min(current_depth):

    # Possible values for minv are:
    # -1 - win
    # 0  - a tie
    # 1  - loss

    # We're initially setting it to 2 as worse than the worst case:
    minv = 2

    qx = None

    result = is_end()

    if result == opponent:
        return (-1, 0)
    elif result == player_turn:
        return (1, 0)
    elif result == '.':
        return (0, 0)

    for c in range(0, columns):
        r = get_row_from_col(c)

        if board[r][c] == '.':
            board[r][c] = opponent
            if (current_depth < tree_depth):
                current_depth += 1
                (m, _) = max(current_depth)
            else:

                result = is_end()

                m = None
                if result == opponent:
                    m = -1
                elif result == player_turn:
                    m = 1
                elif result == '.':
                    m = 0

                if m == None:
                    m = h(player_turn)

            if m < minv:
                minv = m
                qx = c

            board[r][c] = '.'

    return (minv, qx)


if __name__ == "__main__":

    get_input_data('input.txt')

    result = is_end()

    if result != None:
        if result == 'X':
            print('X')
        elif result == 'O':
            print('O')
        elif result == '.':
            print('.')
    else:
        current_depth = 0
        (m, px) = max(current_depth)
        print(px)
