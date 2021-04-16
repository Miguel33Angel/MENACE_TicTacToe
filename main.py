# TicTacToe implementation of different AI
# There's 3 of them

import random


def one_game(menace1, player1, player2):
    first_menace_turn = 0
    if player2 == "Menace":
        first_menace_turn = 1

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = 0
    max_turns = len(board)
    found_winner = False

    show_board(board)

    # For MENACE only
    list_moves = []
    list_indbox = []

    while not found_winner and turn < max_turns:
        if turn % 2 == 0:
            if player1 == "Human":
                move = get_human_turn(board)
            elif player1 == "Perfect":
                print("Let perfect pick.....")
                move, _ = predict(board, turn)
            elif player1 == "Random":
                print("Let random pick.....")
                move = random_guess(board)
            else:  # MENACE
                print("Let MENACE pick.....")
                ind_box, move = learned_prediction(board, menace1, turn)
                list_indbox.append(ind_box)
                list_moves.append(move)

            do_this_move(board, move, 1)

        else:
            if player2 == "Human":
                move = get_human_turn(board)
            elif player2 == "Perfect":
                print("Let perfect pick.....")
                move, _ = predict(board, turn)
            elif player2 == "Random":
                print("Let random pick.....")
                move = random_guess(board)
            else:  # MENACE
                print("Let MENACE pick.....")
                ind_box, move = learned_prediction(board, menace1, turn)
                list_indbox.append(ind_box)
                list_moves.append(move)

            do_this_move(board, move, 2)

        turn += 1
        show_board(board)
        found_winner = is_there_winner(board)

    if not found_winner:
        print("********************  Draw!")
    elif turn % 2 != 0:
        print("-------------------- Winner is " + player1 + "!")
        if player1 == "Menace":
            update_moves(menace1, list_moves, list_indbox, first_menace_turn, turn, +3)
        elif player2 == "Menace":
            update_moves(menace1, list_moves, list_indbox, first_menace_turn, turn, -1)
    elif turn % 2 == 0:
        print("-------------------- Winner is " + player2 + "!")
        if player2 == "Menace":
            update_moves(menace1, list_moves, list_indbox, first_menace_turn, turn, +3)
        elif player1 == "Menace":
            update_moves(menace1, list_moves, list_indbox, first_menace_turn, turn, -1)
    else:
        print("Error!")

    return


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------GENERIC FUNCTIONS----------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def is_there_winner(board):
    winning_state = board[0] == board[1] == board[2] != 0 or board[3] == board[4] == board[5] != 0 or \
                    board[6] == board[7] == board[8] != 0 or board[0] == board[3] == board[6] != 0 or \
                    board[1] == board[4] == board[7] != 0 or board[2] == board[5] == board[8] != 0 or \
                    board[0] == board[4] == board[8] != 0 or board[6] == board[4] == board[2] != 0

    return winning_state


def show_board(board):
    for i in range(3):
        r = ""
        for j in range(3):
            r = r + str(board[i * 3 + j]) + " "
        print(r)
    return


def get_human_turn(board):
    move_str = input("Pick move [1 - 9] -> ")
    move = int(move_str) - 1
    while board[move] != 0:
        move_str = input("Pick again [1 - 9] -> ")
        move = int(move_str) - 1
    return move


def do_this_move(board, move, nplayer):
    board[move] = nplayer
    return board


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------PERFECT AGENT DEF----------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


def predict(board, turn):
    possible_moves = []
    p_value = 0  # In case you don't know, you guess Draw
    p_move = 4  # In case you don't know, you guess Center

    n_possible_moves = board.count(0)
    game_ended = n_possible_moves == 0

    if is_there_winner(board):
        if turn % 2 == 0:
            # it's human turn, so get min reward
            p_value = -10
        else:
            # it's AI turn, so get max reward
            p_value = +10
    elif game_ended:
        p_value = 0
        #  print("I noticed a draw")
    else:
        ind_move = 0
        possible_moves = []
        possible_values = []
        for element in board:
            if element == 0:
                # if it's a possible move
                # Create copy, but not reference to the other array
                copy_board = board.copy()
                if turn % 2 == 0:
                    copy_board[ind_move] = 1  # Try what Human will do
                else:
                    copy_board[ind_move] = 2
                this_predicted_move, this_predicted_value = predict(copy_board, turn + 1)
                possible_moves.append(ind_move)
                possible_values.append(this_predicted_value)
            ind_move += 1

        if turn % 2 == 1:
            # it's human turn, so get minimum
            p_value = min(possible_values)
            p_move = possible_moves[possible_values.index(p_value)]
        else:
            # it's AI turn, so get max
            # print("Debug :")
            # print(possible_values)
            # print(possible_moves)

            p_value = max(possible_values)
            p_move = possible_moves[possible_values.index(p_value)]

    return p_move, p_value


# ---------------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------PERFECT AGENT DEF----------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#

def random_guess(board):
    piece = 1
    move = 0
    while piece != 0:
        move = random.randint(0, len(board) - 1)
        piece = board[move]

    return move


# ---------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------MENACE DEF--------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
# Menace HTF works
# It's basically a matrix, that updates itself to learn. It has inside an array that is just the probabilities of doing
# every move for every state.


# ...............................INDEXING .........................
# It's 5D disguised as 4D, so it can be quite strange to understand. But it's 4D, just because objects can't be done
# easily on C. So, the best option is to, just give a name to every dimension, so every time you want to access
# for example turn 1, you just do menace[1] cause first index is turn.

# Menace has [turn] [ind_box] [this board or values] [cell aka next move]

# So for ex  [1] [2] [0] [3]
# means turn 1, in the box 2 (ex last turn human did center piece), in the board we are before the move the piece,
# in the place 3 which is in the middle (4th position)

# So for ex  [1] [2] [1] [3]
# means turn 1, in the box 2 (ex last turn human did center piece), in the board we are before the move the prob
# to do the move, in the place 3 which is in the middle (4th position)

# index box is a number inside menace that link the actual state of the board with the data menace has about it.
# Like a ID)


def learned_prediction(board, this_menace, turn):
    # It has to return the index box where it has all information about this state, and a move.
    # If no previous record of this state exist (MENACE has never visited it), just add it with guess values for next
    # moves to Menace
    # If it exist, the move will be decided based of the values learned for this state, defined by the board and turn.

    # MAKE THIS GLOBAL IN C
    # How this matrix works, is that it contains the possible order of indexes for each rotation
    # So, rotations[0] is a rotation. The rotation is how each cell ends after rotation.
    # First rotation is no rotation at all

    # For any board or list of values doing board[rotations[ind_rot][ind_cell]] will give you
    # the value of the cell (ind_cell) on the board after rotating (with ind_rot)

    # TODO
    # Create example of rotation working, cause it's complicated

    rotations = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 3, 6, 1, 4, 7, 2, 5, 8],
        [6, 3, 0, 7, 4, 1, 8, 5, 2],
        [6, 7, 8, 3, 4, 5, 0, 1, 2],
        [8, 7, 6, 5, 4, 3, 2, 1, 0],
        [8, 5, 2, 7, 4, 1, 6, 3, 0],
        [2, 5, 8, 1, 4, 7, 0, 3, 6],
        [2, 1, 0, 5, 4, 3, 8, 7, 6]
    ]

    # Just get the boxes of this turn, we don't care yet of the others
    list_boxes = this_menace[turn]

    # Let's see if this state has been visited by Menace before
    # Also we can get the ind_box now
    found = False
    ind_box = 0
    ind_rot = 0
    this_box = []
    while not found and ind_box < len(list_boxes):
        this_box = list_boxes[ind_box]
        found, ind_rot = box_has_rotated_board(this_box, board, rotations)
        ind_box += 1

    # Not found -> never been visited. Let's add it
    if not found:
        # So we need to explore the state, and make MENACE get a guess of the probabilities,
        # even if the guess is bad, it will improve over time
        board_initial_values = get_initial_values_this_board(board)
        # New box create:
        new_box = [board, board_initial_values]
        # Box add:
        add_box_to_menace(this_menace, new_box, turn)

        # The index box will be the last of this turn, as it's the last explored state, hence we now know ind_box
        ind_box = len(list_boxes) - 1
        this_box = list_boxes[ind_box]

    this_values = this_box[1]

    # If found it or not, it doesn't matter now, just chose a move

    # We want to choose the move based on the values (values -> probability of choosing that move)
    sum_elements = 0
    for i in range(9):
        # in list boxes, the box, the values, the element
        sum_elements += this_values[i]

    # Rotate the board with values before using it!
    rot_values = apply_rotation(this_values, rotations[ind_rot])

    # Now get a random number
    # Range goes from [0, 100] so 101 numbers, for example, we want only 100.
    rand_int = random.randint(0, sum_elements - 1)

    # How we make all moves to have a probability proportional to the value?
    # Imagine a simpler case. 3 choices with values 30, 20 and 50.
    # So probability is 100 * (value/sum_values)   ->      30, 20, 50 %
    # If we have a random number n from 1 to 100,
    # the p ->     p(     n <= 30 ) = 0.3
    # The p ->     p(30 < n <= 50 ) = 0.2
    # The p ->     p(50 < n <= 100 ) = 0.5

    # In general form, n -> [0, sum_values)
    # For a p_wanted, the first condition will be ->    n<wanted

    ind_move = 0
    sum_not_chosen = 0
    chosen = sum_not_chosen > rand_int
    while ind_move < len(this_values) and not chosen:
        sum_not_chosen += rot_values[ind_move]
        chosen = sum_not_chosen > rand_int
        ind_move += 1
    ind_move -= 1

    move = rotations[ind_rot][ind_move]  # So this doesn't work huh

    return ind_box, move


def add_box_to_menace(menace, box, turn):
    menace[turn].append(box)
    return


def box_has_rotated_board(box, board, rotations):
    box_board = box[0]
    is_same = False
    i = 0
    while not is_same and i < len(rotations):
        rot_board = apply_rotation(box_board, rotations[i])
        is_same = same_boards(board, rot_board)
        i += 1
    i -= 1

    return is_same, i


def apply_rotation(board, rot):
    rot_board = []
    for i in range(len(board)):
        rot_board.append(board[rot[i]])

    return rot_board


def same_boards(board1, board2):
    is_same = True
    i = 0
    while is_same and i < len(board1):
        is_same = board1[i] == board2[i]
        i += 1
    return is_same


def get_initial_values_this_board(board):
    # Basic example. It just makes a bad initial guess, shouldn't matter for the initial part
    # TODO
    # Change possibilities for symmetric boards

    # Also you need to take into account that if every cell is same probability in symmetric boards, the result
    # won't be fair. Ex: First turn, you have 1/9 in all positions, but center has 1/9 and one corner has 4/9.
    # Change.org

    board_initial_values = []
    for i in range(len(board)):
        if board[i] == 0:
            i_value = 10
        else:
            i_value = 0
        board_initial_values.append(i_value)

    return board_initial_values


def update_moves(menace, list_moves, list_indbox, first_menace_turn, last_turn, reward):
    # Updates all boxes of menace used in this game, to make it learn.
    # If it wins give +1, if it loses give -1. That amount is send by reward.
    # So just do probability of some move in some state += reward

    # Remember:
    # Menace has [turn] [ind_box] [this board or values] [cell/next move]

    n_turn = first_menace_turn
    i = 0
    while n_turn < last_turn:
        ind_box = list_indbox[i]
        ind_move = list_moves[i]
        menace[n_turn][ind_box][1][ind_move] += reward
        # That 1 is for saying that we want to check the value, not the board (board would be 0)
        n_turn += 2  # Skip opponent turn
        i += 1

    print("Menace has learned with " + str(reward))
    return


def save_menace(menace):
    # Remember:
    # [turn] [ind_box] [this board or values] [cell aka next move]
    # (9) (depends on turn) (2) (9)
    # So the way is get number of things and then after those things. Each time a [ is seen is a different level.
    with open('menace_save.txt', 'w') as f:
        f.write(str(menace))
    return


def extract_menace():
    menace = [[], [], [], [], [], [], [], [], []]
    with open('menace_save.txt', 'r') as f:
        for line in f:
            print(line)
    return menace


def run_tests():
    # Only for MENACE

    rotations = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 3, 6, 1, 4, 7, 2, 5, 8],
        [6, 3, 0, 7, 4, 1, 8, 5, 2],
        [6, 7, 8, 3, 4, 5, 0, 1, 2],
        [8, 7, 6, 5, 4, 3, 2, 1, 0],
        [8, 5, 2, 7, 4, 1, 6, 3, 0],
        [2, 5, 8, 1, 4, 7, 0, 3, 6],
        [2, 1, 0, 5, 4, 3, 8, 7, 6]
    ]

    board1 = [1, 0, 1, 0, 0, 1, 0, 1, 0]
    board2 = [1, 0, 1, 0, 0, 1, 0, 1, 0]

    same = same_boards(board1, board2)

    rot = rotations[4]
    board3 = apply_rotation(board1, rot)
    board4 = [0, 1, 0, 1, 0, 0, 1, 0, 1]
    rot_ok = same_boards(board3, board4)

    board5 = apply_rotation(board1, rotations[1])
    box = [board5, [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    check_rotations, rot_ind = box_has_rotated_board(box, board1, rotations)

    print(same and rot_ok and check_rotations)
    print(rot_ind)
    return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menace1 = [[], [], [], [], [], [], [], [], []]  # More than 304 boxes

    # Define how to train
    record_bits = []
    n_trains = 2

    # It doesn't work with both menace
    player1 = "Menace"
    player2 = "Random"

    for i in range(n_trains):
        one_game(menace1, player1, player2)
        sum_bits = 0
        for box in menace1[0]:
            for value in box[1]:
                sum_bits += value
        record_bits.append(sum_bits)

    print(menace1)
    save_menace(menace1)
    extract_menace()

    # for element in record_bits:
    # print(element)

    # TODO
    # Check if punishments and rewards are done correctly
    # Create function to check first box number of choices.
    # Create in choice selection a part where if every box is 0 MENACE resigns.
    # Train it against perfect
    # Save the state of menace and use it again, so a non training version could exist
