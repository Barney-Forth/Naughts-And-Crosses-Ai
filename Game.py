import pygame
import Graphics


class Board:
    def __init__(self):
        self._board = [[" ", " ", " "],
                       [" ", " ", " "],
                       [" ", " ", " "]]

    def __str__(self):
        spacer_row = "+---+---+---+---+"
        rows = [spacer_row, "|   | 1 | 2 | 3 |", spacer_row]
        for i in range(3):
            rows.append(
                f"| {i + 1} | {self._board[i][0]} | {self._board[i][1]} | {self._board[i][2]} |")
            rows.append(spacer_row)

        return "\n".join(rows)

    def get_space_value(self, row: int, col: int) -> str:
        if type(row) != int or type(col) != int:
            raise TypeError("Both row and col hould be integers.")

        if row < 0 or row > 2 or col < 0 or col > 2:
            raise ValueError("Both row and col should be in the range 0-2.")

        return self._board[row][col]

    def update_board(self, row: int, col: int, player: str):
        if self.get_space_value(row, col) == " ":
            self._board[row][col] = player

    def is_three_in_row(self) -> bool:
        for row_index in range(3):
            row = self._board[row_index]
            if len(set(row)) == 1 and " " not in row:
                return True

        for col_index in range(3):
            col = [row[col_index] for row in self._board]
            if len(set(col)) == 1 and " " not in col:
                return True

        down_diagonal = [self._board[x][x] for x in range(3)]
        up_diagonal = [self._board[x][2 - x] for x in range(3)]

        return (len(set(down_diagonal)) == 1 and " " not in down_diagonal) or (len(set(up_diagonal)) == 1 and " " not in up_diagonal)

    def is_board_full(self) -> bool:
        for row in self._board:
            if " " in row:
                return False

        return True


PROGRAM_NAME = "Naughts and Crosses"

SCREEN_WIDTH = 192
SCREEN_HIGHT = 192

BUTTON_SCALE = 4

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set_caption(PROGRAM_NAME)

empty_space_image = pygame.image.load("Blank_Space.png").convert_alpha()
naught_space_image = pygame.image.load("Naught_Space.png").convert_alpha()
cross_space_image = pygame.image.load("Cross_Space.png").convert_alpha()

PLAYERS = (("O", naught_space_image), ("X", cross_space_image))
buttons = [[Graphics.Button(empty_space_image, 64 * x, 64 * y, BUTTON_SCALE)
            for x in range(3)] for y in range(3)]

board = Board()
player = 0

running = True
while running:
    for row in range(3):
        for col in range(3):
            buttons[row][col].draw(screen)
            if buttons[row][col].is_clicked():
                board.update_board(row, col, PLAYERS[player][0])
                buttons[row][col].image = PLAYERS[player][1]
                if board.is_three_in_row():
                    # display win text
                    Graphics.display_text(
                        f"{PLAYERS[player][0]} wins!", screen)
                    # stop playing
                    pass
                elif board.is_board_full():
                    # dsplay draw text
                    Graphics.display_text("Draw.", screen)
                    # stop playing
                    pass
                else:
                    player = (player + 1) % 2

    screen.fill("#000000")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
