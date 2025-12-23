import pygame
import sys
import time

# ---------------- CONFIG ----------------
N = 8
SIZE = 640
CELL = SIZE // N
INFO = 80
HEIGHT = SIZE + INFO

BOX_ROWS = 2
BOX_COLS = 4

# ---------------- COLORS ----------------
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (180,180,180)
YELLOW = (255,255,200)
RED = (255,120,120)
GREEN = (0,180,0)

# ---------------- STATE ----------------
current = {"cell": None, "backtrack": False}

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
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)

    for r in range(N):
        for c in range(N):
            x, y = c * CELL, r * CELL

            if current["cell"] == (r, c):
                color = RED if current["backtrack"] else YELLOW
                pygame.draw.rect(screen, color, (x, y, CELL, CELL))

            pygame.draw.rect(screen, BLACK, (x, y, CELL, CELL), 1)

            if board[r][c] != 0:
                text = font.render(str(board[r][c]), True, GREEN)
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
                    if is_valid(board, r, c, num):
                        board[r][c] = num
                        current["cell"] = (r, c)
                        current["backtrack"] = False
                        draw(screen, board)
                        time.sleep(0.1)

                        if solve(board, screen):
                            return True

                        board[r][c] = 0
                        current["backtrack"] = True
                        draw(screen, board)
                        time.sleep(0.1)

                return False
    return True

# ---------------- MAIN ----------------
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SIZE, HEIGHT))
pygame.display.set_caption("8x8 Sudoku Solver – Empty Board (2x4 Subgrids)")

board = [[0]*N for _ in range(N)]

draw(screen, board)
time.sleep(1)

solve(board, screen)

# Keep window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
