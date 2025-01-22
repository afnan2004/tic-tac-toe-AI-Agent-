import pygame
import sys
import math

pygame.init()

# Screen settings
WIDTH, HEIGHT = 650, 650  
LINE_WIDTH = 15
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
WIN_LINE_COLOR = (50, 205, 50)  
HIGHLIGHT_COLOR = (173, 255, 47)
TEXT_COLOR = (255, 255, 255)
LOSE_COLOR = (255, 0, 0)  
TIE_COLOR = (255, 255, 0)  

# Board settings
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Fonts
FONT = pygame.font.Font(None, 80)
LABEL_FONT = pygame.font.Font(None, 50)  # Font for the label text

# Board
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Players
HUMAN = "X"
AI = "O"
current_player = HUMAN

# Load sound effects
lose_sound = pygame.mixer.Sound("WhatsApp Audio 2025-01-05 at 12.25.13_5bb41ca6.mp3")
tie_sound = pygame.mixer.Sound("WhatsApp Audio 2025-01-05 at 13.51.25_4ab68ecb.mp3")
start_sound = pygame.mixer.Sound("WhatsApp Audio 2025-01-05 at 13.38.19_509a2d0c.mp3")

# Draw grid
def draw_lines():
    SCREEN.fill(BG_COLOR)
    for row in range(1, ROWS):
        pygame.draw.line(SCREEN, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, COLS):
        pygame.draw.line(SCREEN, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "O":
                pygame.draw.circle(SCREEN, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(SCREEN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(SCREEN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

def draw_winning_line(start, end):
    pygame.draw.line(SCREEN, WIN_LINE_COLOR, start, end, LINE_WIDTH)

# Check for a winner
def check_winner():
    for row in range(ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            highlight_winning_cells([(row, 0), (row, 1), (row, 2)])
            draw_winning_line((0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2))
            return board[row][0]
    for col in range(COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            highlight_winning_cells([(0, col), (1, col), (2, col)])
            draw_winning_line((col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 50))
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        highlight_winning_cells([(0, 0), (1, 1), (2, 2)])
        draw_winning_line((0, 0), (WIDTH, HEIGHT - 50))
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        highlight_winning_cells([(0, 2), (1, 1), (2, 0)])
        draw_winning_line((WIDTH, 0), (0, HEIGHT - 50))
        return board[0][2]
    return None

# Highlight winning cells
def highlight_winning_cells(cells):
    for row, col in cells:
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, HIGHLIGHT_COLOR, rect)

# Check if the board is full
def is_board_full():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is None:
                return False
    return True

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == AI:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] is None:
                    board[row][col] = AI
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] is None:
                    board[row][col] = HUMAN
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is None:
                board[row][col] = AI
                score = minimax(board, 0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = AI

# Restart the game
def restart():
    global board, current_player
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    current_player = HUMAN

# Display endgame message
def show_message_on_board(message, is_win=True):
    color = WIN_LINE_COLOR if is_win else LOSE_COLOR
    pygame.draw.rect(SCREEN, color, (0, HEIGHT // 2 - 50, WIDTH, 100))
    text = FONT.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.update()

# Display "HUMAN vs AI" label
def draw_label():
    # Render "HUMAN" in black
    human_text = LABEL_FONT.render("HUMAN", True, (0, 0, 0))  # Black color
    human_width = human_text.get_width()

    # Render "vs" in red
    vs_text = LABEL_FONT.render("vs", True, LOSE_COLOR)  # Red color
    vs_width = vs_text.get_width()

    # Render "AI" in white
    ai_text = LABEL_FONT.render("AI", True, TEXT_COLOR)  # White color
    ai_width = ai_text.get_width()

    # Calculate total width and center position
    total_width = human_width + vs_width + ai_width + 20  # Adding 20px spacing between components
    start_x = (WIDTH - total_width) // 2

    # Render "HUMAN"
    SCREEN.blit(human_text, (start_x, HEIGHT - 50))

    # Render "vs"
    SCREEN.blit(vs_text, (start_x + human_width + 10, HEIGHT - 50))  # 10px spacing after "HUMAN"

    # Render "AI"
    SCREEN.blit(ai_text, (start_x + human_width + vs_width + 20, HEIGHT - 50))  # 20px spacing after "vs"

# Display a "Game Start" message
def show_start_message():
    SCREEN.fill(BG_COLOR)
    message = "Press Enter to Start"
    text = FONT.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.update()

# Main loop
run = True
game_started = False

# Show the start message
show_start_message()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Start the game when Enter is pressed
        if not game_started and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_sound.play()  # Play sound when game starts
                game_started = True
                draw_lines()

        # Handle gameplay events if the game has started
        if game_started:
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == HUMAN:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                if board[clicked_row][clicked_col] is None:
                    board[clicked_row][clicked_col] = HUMAN
                    if not check_winner() and not is_board_full():
                        current_player = AI
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()

    if game_started:
        if current_player == AI and not check_winner() and not is_board_full():
            ai_move()
            current_player = HUMAN

        draw_lines()
        draw_figures()
        draw_label()
        pygame.display.update()

        winner = check_winner()
        if winner or is_board_full():
            if winner == HUMAN:
                show_message_on_board("You Win!")
            elif winner == AI:
                show_message_on_board("You Lose!", is_win=False)
                lose_sound.play()
            else:
                show_message_on_board("It's a Tie!")
                tie_sound.play() 

            pygame.time.wait(1500)
            restart()

pygame.quit()
sys.exit()
 