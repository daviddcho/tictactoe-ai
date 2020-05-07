import math

# TIC-TAC-TOE AI with Minimax Algorithm + alpha-beta pruning

# Global Variables
# Game board
board = [["-", "-", "-"],
         ["-", "-", "-"],
         ["-", "-", "-"]]
# Players
human = 'X'
ai = 'O'
# Starting player
current_player = human
# If the game is still going
game_going = True
# If player wants to play another game
play_again = True


def display_board():
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for count, row in enumerate(board)]))


def reset_board(winner):
    global game_going
    for i in range(3):
        for j in range(3):
            board[i][j] = '-'
    game_going = True
    winner = None


def equals3(a, b, c):
    return a == b and b == c and a != '-'


# Checks for winner
# returns None if no winner, returns 'tie' if tie
def check_winner():
    winner = None
    # Check horizontal
    for i in range(3):
        if equals3(board[i][0], board[i][1], board[i][2]):
            winner = board[i][0]
    # Check vertical
    for i in range(3):
        if equals3(board[0][i], board[1][i], board[2][i]):
            winner = board[0][i]
    # Check diagonal
    if equals3(board[0][0], board[1][1], board[2][2]):
        winner = board[0][0]
    if equals3(board[2][0], board[1][1], board[0][2]):
        winner = board[2][0]
    # Check for a tie
    open_spots = 0
    for row in board:
        for item in row:
            if item == '-':
                open_spots += 1

    if winner is None and open_spots == 0:
        return 'tie'
    else:
        return winner


# Check if game is still going
def check_game_over():
    result = check_winner()
    # If there is no result of winner or tie return True to continue the game
    if result is None:
        return True
    else:
        return False


# Checks if user input is valid - between 9-1 or if position is already taken
def valid_input(pos):
    if pos in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
        x, y = board_pos(pos)
        if board[y][x] != '-':
            return False
        return True
    else:
        return False


# Returns board position in 2d array with user input
def board_pos(pos):
    pos = int(pos)
    y = pos / 3
    x = pos % 3
    if x != 0:
        x -= 1
    else:
        x = 2
        y -= 1
    return x, int(y)


# Makes current player's turn
def handle_turn(player):
    while True:
        print(player + "'s turn.")
        pos = input("Choose a position from 1-9: ")
        if not valid_input(pos):
            print("This is an invalid move.")
        else:
            x, y = board_pos(pos)
            board[y][x] = player
            break


# Switches turn to next player
def flip_player():
    global current_player
    if current_player == human:
        current_player = ai
    else:
        current_player = human


def minimax(board, depth, alpha, beta, max_player):
    result = check_winner()
    if result == ai:
        return 10
    if result == human:
        return -10
    if result == 'tie':
        return 0

    if max_player:
        max_val = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = ai
                    cur_eval = minimax(board, depth+1, alpha, beta, False)
                    # Call minimax recursively and get max value
                    max_val = max(max_val, cur_eval)
                    board[i][j] = '-'
                    # Pruning
                    alpha = max(alpha, cur_eval)
                    if beta <= alpha:
                        break
        return max_val
    else:
        min_val = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    board[i][j] = human
                    # Call minimax recursively
                    cur_eval = minimax(board, depth+1, alpha, beta, True)
                    # Get min value
                    min_val = min(min_val, cur_eval)
                    board[i][j] = '-'
                    beta = min(beta, cur_eval)
                    if beta <= alpha:
                        break
        return min_val


def find_best_move():
    print(current_player + "'s turn")
    best_val = None
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '-':
                # Make move
                board[i][j] = ai
                # Calculate value of that move
                move_val = minimax(board, 0, -math.inf, math.inf, False)
                # Undo move
                board[i][j] = '-'
                # If the current move is better than best move
                # then update current move to best move
                if best_val is None:
                    best_val = move_val
                    best_move = [i, j]
                elif move_val > best_val:
                    best_val = move_val
                    best_move = [i, j]
    # Make the best move
    board[best_move[0]][best_move[1]] = ai


def play_game():
    global game_going, play_again
    # While player wants to play game
    while play_again:
        # Display starting board
        display_board()
        print("1   2   3")
        print("4   5   6")
        print("7   8   9")
        while game_going:
            # Handles turn of current player
            if current_player == human:
                handle_turn(current_player)
            else:
                find_best_move()
            # Checks if game ended
            game_going = check_game_over()
            # Switches to next player turn
            flip_player()
            # Displays board
            display_board()
        # Game ended
        winner = check_winner()
        if winner == 'tie':
            print("The game was a tie.")
        else:
            print(winner + " won.")
        # Ask player if they want to continue playing
        cont = input("Do you want to play again? (YES/NO) ")
        if cont == 'YES':
            reset_board(winner)
        else:
            exit()


play_game()
