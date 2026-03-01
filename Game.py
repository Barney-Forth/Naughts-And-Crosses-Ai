import NeuralNet


PLAYERS = ("O", "X")


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

    def _get_space_value(self, position: tuple[int, int]) -> str:
        row, col = position
        if type(row) != int or type(col) != int:
            raise TypeError("Both row and col hould be integers.")

        if row < 0 or row > 2 or col < 0 or col > 2:
            raise ValueError("Both row and col should be in the range 0-2.")

        return self._board[row][col]

    def update_board(self, position: tuple[int, int], player: str):
        if self._get_space_value(position) == " ":
            row, col = position
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
        if len(set(down_diagonal)) == 1 and " " not in down_diagonal:
            return True

        up_diagonal = [self._board[x][2 - x] for x in range(3)]

        return (len(set(up_diagonal)) == 1 and " " not in up_diagonal)

    def is_full(self) -> bool:
        for row in self._board:
            if " " in row:
                return False

        return True

    def flatten(self) -> list[str]:
        return [self._board[row][col] for row in range(3) for col in range(3)]

    def get_move(self) -> tuple[int, int]:
        valid = False
        while not valid:
            move = input("Suitable promt: ")

            row = -1
            col = -1

            for char in move:
                if char.isdigit():
                    if col == -1:
                        col = int(char) - 1
                    elif row == -1:
                        row = int(char) - 1
                    else:
                        pass

            try:
                if self._get_space_value(row, col) == " ":
                    valid = True
            except TypeError:
                print("ERROR MESSAGE")
            except ValueError:
                print("ERROR MESSAGE")

        return (row, col)


def play_2_players():
    board = Board()
    player = 0

    while not board.is_full() and not board.is_three_in_row():
        print(board)

        move = board.get_move()

        print()

        board.update_board(move, PLAYERS[player])

        if board.is_three_in_row():
            print(board)
            print(f"{PLAYERS[player]} wins!")
        elif board.is_full():
            print(board)
            print("Draw.")
        else:
            player = (player + 1) % 2


def play_1_player():
    board = Board()
    player = 0
    network = NeuralNet.Network()
    network.load_net_values("best_net")

    while not board.is_full() and not board.is_three_in_row():
        print(board)

        if player == 0:
            move = board.get_move()
        else:
            move = network.get_output(board.flatten(), player)

        print()

        board.update_board(move, PLAYERS[player])

        if board.is_three_in_row():
            print(board)
            print(f"{PLAYERS[player]} wins!")
        elif board.is_full():
            print(board)
            print("Draw.")
        else:
            player = (player + 1) % 2
