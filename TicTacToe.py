import pygame
import sys

# Start pygame
pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // BOARD_COLS
CIRCLE_WIDTH = 30
CROSS_WIDTH = 40
SPACE = SQUARE_SIZE // 8

#Define colors
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
MAROON = pygame.Color('orangered4')
GOLD = pygame.Color('gold2')

# Setup Screen & Board
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Functions
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, BLACK, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

#Called at the end of the loop for each turn, adds sign to each box
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, MAROON, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, MAROON, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, GOLD, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

#Function returns if the given player has won, and returns that along with how they won
def check_win(player):
    # check rows
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return [True, 'row']
        
    # Check columns
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return [True, 'column']
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or \
            all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)]):
        return [True, 'diagonal']
    return [False, None]

#Reset all boxes
def restart():
    screen.fill(WHITE)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

def draw_diagonal_line(row, col, color):
    if row == col and board[0][0] == board[1][1]:
        pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 5)
    else:
        pygame.draw.line(screen, color, (WIDTH - 15, 15), (15, HEIGHT - 15), 5)

def draw_vertical_line(col, color):
    pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 15),
                     (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 15), 5)

def draw_horizontal_line(row, color):
    pygame.draw.line(screen, color, (15, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                     (WIDTH - 15, row * SQUARE_SIZE + SQUARE_SIZE // 2), 5)

#Main loop handles the game with game events, marking squares, and checking the win conditions
def main():
    turn = 0
    game_over = False
    draw_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                #calculate which box was clicked
                mouseX = event.pos[0]  # x
                mouseY = event.pos[1]  # y
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                #Mark boxes with correct player
                if available_square(clicked_row, clicked_col):
                    if turn == 0:
                        mark_square(clicked_row, clicked_col, 'X')
                        turn = 1

                        #Check if player has won
                        win_condition = check_win('X')
                        if win_condition[0]:
                            game_over = True
                            print("X wins!")
                            if win_condition[1] == 'row':
                                draw_horizontal_line(clicked_row, MAROON)
                            elif win_condition[1] == 'column':
                                draw_vertical_line(clicked_col, MAROON)
                            else:
                                draw_diagonal_line(clicked_row, clicked_col, MAROON)
                        elif is_board_full():
                            game_over = True
                            print("It's a tie!")
                    else:
                        mark_square(clicked_row, clicked_col, 'O')
                        turn = 0

                        #Check if player has won
                        win_condition = check_win('O')
                        if win_condition[0]:
                            game_over = True
                            print("O wins!")
                            if win_condition[1] == 'row':
                                draw_horizontal_line(clicked_row, GOLD)
                            elif win_condition[1] == 'column':
                                draw_vertical_line(clicked_col, GOLD)
                            else:
                                draw_diagonal_line(clicked_row, clicked_col, GOLD)
                        elif is_board_full():
                            game_over = True
                            print("It's a tie!")

                draw_figures()

            #Handle restarting the game
            if event.type == pygame.KEYDOWN and game_over:
                print("Restarting...")
                if event.key == pygame.K_r:
                    restart()
                    game_over = False
                    turn = 0

        pygame.display.update()

if __name__ == "__main__":
    main()
