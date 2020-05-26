import pygame
from pygame.locals import *
import sys
import time
import math

# tic-tac-toe ai with Minimax Algorithm + alpha-beta pruning

# Global Variables
# Game board
board = [[None]*3,
         [None]*3,
         [None]*3]
# Players
human = 'X'
ai = 'O'
# Starting player
current_player = human
# If the game is still going
game_going = True
winner = None

width = 400
height = 400
line_color = (255, 255, 255)

# Initializing pygame window
pygame.init()
CLOCK = pygame.time.Clock()
# Initializing the display
screen = pygame.display.set_mode((width, height+100))
pygame.display.set_caption("tic-tac-toe against alphatoe")

x_img = pygame.image.load('x.png').convert_alpha()
o_img = pygame.image.load('o.png').convert_alpha()
# Resizing images
x_img = pygame.transform.scale(x_img, (80,80))
o_img = pygame.transform.scale(o_img, (80,80))
# Transparency

# Switches turn to next player
def flip_player():
    global current_player
    if current_player == human:
        current_player = ai
    else:
        current_player = human


def draw_move(row, col):
    global current_player
    # print(row, col)
    if row == 1:
        posx = 30
    if row == 2:
        posx = width/3 + 30
    if row == 3:
        posx = width/3*2 + 30
    if col == 1:
        posy = 30
    if col == 2:
        posy = height/3 + 30
    if col == 3:
        posy = height/3*2 + 30
    board[row-1][col-1] = current_player
    if current_player == human:
        screen.blit(x_img, (posy, posx))
        current_player = ai;
        # flip_player()
    else:
        screen.blit(o_img, (posy, posx))
        current_player = human;
        # flip_player()
    pygame.display.update()


def minimax(board, depth, alpha, beta, max_player):
    global winner
    result = check_winner()
    if result == ai:
        winner = None
        return 10
    if result == human:
        winner = None
        return -10
    if result == 'tie':
        winner = None
        return 0

    if max_player:
        max_val = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    board[i][j] = ai
                    cur_eval = minimax(board, depth+1, alpha, beta, False)
                    # Call minimax recursively and get max value
                    max_val = max(max_val, cur_eval)
                    board[i][j] = None
                    # Pruning
                    alpha = max(alpha, cur_eval)
                    if beta <= alpha:
                        break
        return max_val
    else:
        min_val = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    board[i][j] = human
                    # Call minimax recursively
                    cur_eval = minimax(board, depth+1, alpha, beta, True)
                    # Get min value
                    min_val = min(min_val, cur_eval)
                    board[i][j] = None
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
            if board[i][j] == None:
                # Make move
                board[i][j] = ai
                # Calculate value of that move
                move_val = minimax(board, 0, -math.inf, math.inf, False)
                # Undo move
                board[i][j] = None
                winner = None
                # If the current move is better than best move
                # then update current move to best move
                if best_val is None:
                    best_val = move_val
                    best_move = [i, j]
                elif move_val > best_val:
                    best_val = move_val
                    best_move = [i, j]
    # Make the best move
    # board[best_move[0]][best_move[1]] = ai
    draw_move(best_move[0]+1, best_move[1]+1)


def reset_board():
    global game_going, board, winner
    board = [[None]*3,
            [None]*3,
            [None]*3]
    game_going = True
    winner = None


def reset_game():
    global current_player, winner
    # time.sleep(1)
    current_player = human
    reset_board()
    game_opening()


def equals3(a, b, c):
    return a == b and b == c and a != None


# Checks for winner
# returns None if no winner, returns 'tie' if tie
def check_winner():
    global winner
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
            if item == None:
                open_spots += 1

    if winner is None and open_spots == 0:
        return 'tie'
    else:
        return winner


# Checks for winner and signals winner
def draw_win():
    # Check horizontal
    for i in range(3):
        if equals3(board[i][0], board[i][1], board[i][2]):
            pygame.draw.line(screen, (250,0,0), (0, (i + 1)*height/3 - height/6), (width, (i + 1)*height/3 - height/6 ), 4)
            break
    # Check vertical
    for i in range(3):
        if equals3(board[0][i], board[1][i], board[2][i]):
            pygame.draw.line (screen, (250,0,0), ((i + 1)* width/3 - width/6, 0), ((i + 1)* width/3 - width/6, height), 4)
            break
    # Check diagonal
    if equals3(board[0][0], board[1][1], board[2][2]):
        pygame.draw.line (screen, (250,70,70), (50, 50), (350, 350), 4)
    if equals3(board[2][0], board[1][1], board[0][2]):
        pygame.draw.line (screen, (250,70,70), (350, 50), (50, 350), 4)

def game_status():
    global winner, game_going, current_player
    winner = check_winner()
    game_going = True
    if winner is None:
        msg = current_player + "'s turn."
    elif winner == 'tie':
        msg = "The game was a tie."
        game_going = False
    else:
        msg = winner + " won!"
        game_going = False
    font = pygame.font.Font(None, 30)
    text = font.render(msg, 1, (255,255,255))
    # Display msg on the screen
    screen.fill((0,0,0), (0,400,500,100))
    text_rect = text.get_rect(center=(round(width/2), 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()
    draw_win()
    if game_going == False:
        reset_game()


def user_click():
    x, y = pygame.mouse.get_pos()
    if x < width/3:
        col = 1
    elif x < width/3*2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None
    if y < height/3:
        row = 1
    elif y < height/3*2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None    
    if (row and col and board[row-1][col-1] is None):
        draw_move(row, col)

# Check if game is still going
def check_game_over():
    result = check_winner()
    # If there is no result of winner or tie return True to continue the game
    if result is None:
        return True
    else: # Game is over, there is a winner or a tie
        return False


def game_opening():
    pygame.display.update()
    time.sleep(1)
    screen.fill((0,0,0))
    # Drawing vertical lines
    pygame.draw.line(screen, line_color, (round(width/3), 0), (round(width/3), height), 7)
    pygame.draw.line(screen, line_color, (round(width/3*2), 0), (round(width/3*2), height), 7)
    # Drawing horizontal lines
    pygame.draw.line(screen, line_color, (0, round(height/3)), (width, round(height/3)), 7)
    pygame.draw.line(screen, line_color, (0, round(height/3*2)), (width, round(height/3*2)), 7)
    game_status()


def play_game():
    global game_going, winner, current_player
    game_opening()
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if current_player == human:
                if event.type is MOUSEBUTTONDOWN:
                    user_click()
                    game_status()
            else:
                find_best_move()
                game_status()
        pygame.display.update()
        CLOCK.tick(30)

if __name__ == '__main__':
    play_game()