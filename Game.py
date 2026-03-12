from NeuralNet import Network

# Change this to chage the net to play against
PLAYING_NET = "best_net"


PLAYERS = ("O", "X")


class Board:
    """Represents a 3x3 Naughts and Crosses game board."""

    def __init__(self):
        """Initialize an empty 3x3 board."""
        self._board = [[" ", " ", " "],
                       [" ", " ", " "],
                       [" ", " ", " "]]

    def __str__(self):
        """Return a formatted string representation of the board."""
        spacer_row = "+---+---+---+---+"
        rows = [spacer_row, "|   | 1 | 2 | 3 |", spacer_row]
        for i in range(3):
            rows.append(
                f"| {i + 1} | {self._board[i][0]} | {self._board[i][1]} | {self._board[i][2]} |")
            rows.append(spacer_row)

        return "\n".join(rows)

    def get_space_value(self, position: tuple[int, int]) -> str:
        """Get the value at a specific board position.

        Args:
            position: A tuple of (row, col) where both are 0-2.

        Returns:
            The value at the position: 'X', 'O', or ' ' (empty).

        Raises:
            TypeError: If row or col are not integers.
            ValueError: If row or col are outside the range 0-2.
        """
        row, col = position
        if type(row) != int or type(col) != int:
            raise TypeError("Both row and col hould be integers.")

        if row < 0 or row > 2 or col < 0 or col > 2:
            raise ValueError("Both row and col should be in the range 0-2.")

        return self._board[row][col]

    def update_board(self, position: tuple[int, int], player: str):
        """Place a player's mark at the specified position if it's empty.

        Args:
            position: A tuple of (row, col) where both are 0-2.
            player: The player's mark ('X' or 'O').
        """
        if self.get_space_value(position) == " ":
            row, col = position
            self._board[row][col] = player

    def is_three_in_row(self) -> bool:
        """Check if there's a winning condition (three in a row).

        Checks rows, columns, and both diagonals.

        Returns:
            True if a player has three marks in a row, False otherwise.
        """
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
        """Check if the board is completely filled.

        Returns:
            True if all spaces are occupied, False otherwise.
        """
        for row in self._board:
            if " " in row:
                return False

        return True

    def flatten(self) -> list[str]:
        """Flatten the 2D board into a 1D list.

        Returns:
            A list of 9 elements representing the board in row-major order.
        """
        return [self._board[row][col] for row in range(3) for col in range(3)]

    def get_move(self) -> tuple[int, int]:
        """Get a valid move from the player.

        Prompts the user for input until a valid, unoccupied space is selected.

        Returns:
            A tuple of (row, col) for the chosen position.
        """
        valid = False
        while not valid:
            move = input("Where to move in col, row format (e.g., 1,2): ")

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
                if self.get_space_value((row, col)) == " ":
                    valid = True
                else:
                    print("That space is already occupied.")
            except TypeError:
                print("Should give two digits separated by a comma.")
            except ValueError:
                print("Both row and col should be in the range 1-3.")

        return (row, col)


def play_2_players():
    """Run a two-player Tic-Tac-Toe game in the console.

    Alternates between two human players taking turns until there's a winner or draw.
    """
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
    """Run a one-player Tic-Tac-Toe game against a neural network AI.

    The human player is 'O' and the AI (neural network) is 'X'. The game continues
    until there's a winner or draw.
    """
    board = Board()
    player = 0
    network = Network(PLAYING_NET)

    while not board.is_full() and not board.is_three_in_row():
        print(board)

        if player == 0:
            move = board.get_move()
        else:
            print("AI is thinking...")
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


if __name__ == "__main__":
    play_1_player()
