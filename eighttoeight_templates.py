import pygame
import sys
import time

# ---------------- CONFIG ----------------
N = 8
SIZE = 640
CELL = SIZE // N
INFO = 120
HEIGHT = SIZE + INFO

BOX_ROWS = 2
BOX_COLS = 4

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
LIGHT_GRAY = (230, 230, 230)
YELLOW = (255, 255, 150)
RED = (255, 100, 100)
GREEN = (50, 150, 50)
DARK_GRAY = (50, 50, 50)

# ---------------- STATE ----------------
current = {
    "cell": None,
    "backtrack": False,
    "attempts": 0,
    "backtracks": 0
}

# ---------------- PUZZLE TEMPLATES ----------------
PUZZLES = {
    "Easy": [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 0, 0, 0, 8],
    ],
    "Medium": [
        [5, 3, 0, 0, 7, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6],
        [8, 0, 0, 0, 6, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0],
        [7, 0, 0, 0, 2, 0, 0, 1],
        [0, 6, 0, 0, 0, 0, 2, 8],
        [0, 0, 0, 4, 1, 9, 0, 5],
    ],
    "Hard": [
        [0, 0, 5, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 1, 5, 0, 4],
        [4, 0, 0, 0, 0, 5, 3, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 5, 0],
        [0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    "Extreme": [
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
}

# Store original board for visualization
original_board = None

# ---------------- VALIDITY CHECK ----------------
def is_valid(board, r, c, num):
    # Row & Column
    for i in range(N):
        if board[r][i] == num or board[i][c] == num:
            return False

    # Subgrid (2x4)
    sr = (r // BOX_ROWS) * BOX_ROWS
    sc = (c // BOX_COLS) * BOX_COLS

    for i in range(sr, sr + BOX_ROWS):
        for j in range(sc, sc + BOX_COLS):
            if board[i][j] == num:
                return False

    return True

# ---------------- DRAW ----------------
def draw(screen, board):
    # Board background
    pygame.draw.rect(screen, WHITE, (0, 0, SIZE, SIZE))
    
    font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 16)

    # Draw cells
    for r in range(N):
        for c in range(N):
            x, y = c * CELL, r * CELL

            # Highlight current cell
            if current["cell"] == (r, c):
                color = RED if current["backtrack"] else YELLOW
                pygame.draw.rect(screen, color, (x, y, CELL, CELL))
            else:
                # Light background for given numbers
                if original_board and original_board[r][c] != 0:
                    pygame.draw.rect(screen, LIGHT_GRAY, (x, y, CELL, CELL))

            pygame.draw.rect(screen, BLACK, (x, y, CELL, CELL), 1)

            # Draw numbers
            if board[r][c] != 0:
                # Given numbers in dark gray, solved in green
                if original_board and original_board[r][c] != 0:
                    text_color = DARK_GRAY
                else:
                    text_color = GREEN
                
                text = font.render(str(board[r][c]), True, text_color)
                screen.blit(
                    text,
                    text.get_rect(center=(x + CELL//2, y + CELL//2))
                )

    # Thick subgrid lines
    for i in range(N + 1):
        thickness = 4 if i % BOX_ROWS == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i*CELL), (SIZE, i*CELL), thickness)

        thickness = 4 if i % BOX_COLS == 0 else 1
        pygame.draw.line(screen, BLACK, (i*CELL, 0), (i*CELL, SIZE), thickness)

    # Info panel
    pygame.draw.rect(screen, LIGHT_GRAY, (0, SIZE, SIZE, INFO))
    pygame.draw.line(screen, BLACK, (0, SIZE), (SIZE, SIZE), 2)

    info_text = [
        f"Attempts: {current['attempts']}  |  Backtracks: {current['backtracks']}",
    ]
    
    if current["cell"]:
        r, c = current["cell"]
        status = "BACKTRACKING" if current["backtrack"] else "Solving..."
        info_text.append(f"Cell [{r}][{c}]: {status}")
    else:
        info_text.append("PUZZLE SOLVED! ✓")

    for idx, text in enumerate(info_text):
        text_surface = info_font.render(text, True, BLACK)
        screen.blit(text_surface, (10, SIZE + 10 + idx * 25))

    pygame.display.update()

# ---------------- SOLVER ----------------
def solve(board, screen):
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                for num in range(1, N + 1):
                    current["attempts"] += 1
                    
                    if is_valid(board, r, c, num):
                        board[r][c] = num
                        current["cell"] = (r, c)
                        current["backtrack"] = False
                        draw(screen, board)
                        time.sleep(0.05)

                        if solve(board, screen):
                            return True

                        board[r][c] = 0
                        current["backtracks"] += 1
                        current["backtrack"] = True
                        draw(screen, board)
                        time.sleep(0.05)

                return False
    return True

# ---------------- MENU ----------------
def show_menu():
    pygame.init()
    pygame.font.init()
    
    menu_width = 400
    menu_height = 400
    screen = pygame.display.set_mode((menu_width, menu_height))
    pygame.display.set_caption("8x8 Sudoku Solver - Select Difficulty")
    
    font_title = pygame.font.Font(None, 48)
    font_option = pygame.font.Font(None, 36)
    
    puzzles_list = list(PUZZLES.keys())
    selected = 0
    
    while True:
        screen.fill(WHITE)
        
        # Title
        title = font_title.render("SELECT PUZZLE", True, BLACK)
        screen.blit(title, (menu_width//2 - title.get_width()//2, 30))
        
        # Options
        for i, name in enumerate(puzzles_list):
            color = GREEN if i == selected else BLACK
            text = font_option.render(f"> {name} <" if i == selected else name, True, color)
            screen.blit(text, (menu_width//2 - text.get_width()//2, 120 + i * 60))
        
        # Instructions
        inst_font = pygame.font.Font(None, 16)
        inst = inst_font.render("Use UP/DOWN arrows, press ENTER to select", True, GRAY)
        screen.blit(inst, (10, menu_height - 30))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(puzzles_list)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(puzzles_list)
                if event.key == pygame.K_RETURN:
                    return puzzles_list[selected]

# ---------------- MAIN ----------------
pygame.init()
pygame.font.init()

# Show menu and get puzzle selection
difficulty = show_menu()
puzzle = [row[:] for row in PUZZLES[difficulty]]
original_board = [row[:] for row in puzzle]

# Create game screen
screen = pygame.display.set_mode((SIZE, HEIGHT))
pygame.display.set_caption(f"8x8 Sudoku Solver – {difficulty} Level (2x4 Subgrids)")

print(f"\n{'='*50}")
print(f"Starting {difficulty} Puzzle")
print(f"{'='*50}")
print("\nInitial Puzzle:")
for row in original_board:
    print(row)

# Show initial puzzle
draw(screen, puzzle)
time.sleep(2)

# Solve
print("\nSolving...")
solve(puzzle, screen)

# Final display
current["cell"] = None
current["backtrack"] = False
draw(screen, puzzle)
time.sleep(1)

# Print results
print(f"\n{'='*50}")
print("PUZZLE SOLVED!")
print(f"{'='*50}")
print("\nSolved Puzzle:")
for row in puzzle:
    print(row)

print(f"\nStatistics:")
print(f"  Total Attempts: {current['attempts']}")
print(f"  Total Backtracks: {current['backtracks']}")
print(f"  Efficiency: {current['attempts'] - current['backtracks']} successful placements")
print(f"\nClose the window to exit...")
print(f"{'='*50}\n")

# Keep window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
