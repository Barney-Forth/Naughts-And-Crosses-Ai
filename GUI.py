import tkinter as tk
import threading
from Game import Board, PLAYERS
from NeuralNet import Network


class TicTacToeGUI:
    """A tkinter GUI for playing Naughts and Crosses (Tic-Tac-Toe) against the AI."""

    def __init__(self, root):
        """Initialize the GUI.

        Args:
            root: The tkinter root window.
        """
        self.root = root
        self.root.title("Naughts and Crosses")
        self.root.resizable(False, False)

        # Game state
        self.board = None
        self.network = Network("best_net")
        self.human_player = None  # 0 = 'O', 1 = 'X'
        self.ai_player = None
        self.current_player = 0
        self.game_over = False
        self.game_mode = None  # "single_o", "single_x", or "two_player"

        # Create main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
        self.main_frame.pack()

        # Create mode selection screen
        self.setup_mode_selection()

    def setup_mode_selection(self):
        """Set up the mode selection screen."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Naughts and Crosses",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))

        # Mode selection label
        mode_label = tk.Label(
            self.main_frame,
            text="Select Game Mode",
            font=("Arial", 18),
            bg="#f0f0f0"
        )
        mode_label.pack(pady=(0, 20))

        # Button frame
        button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Single player as O button
        single_o_btn = tk.Button(
            button_frame,
            text="Single Player (You as O)",
            font=("Arial", 12),
            command=lambda: self.start_game("single_o"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            width=25
        )
        single_o_btn.pack(pady=5)

        # Single player as X button
        single_x_btn = tk.Button(
            button_frame,
            text="Single Player (You as X)",
            font=("Arial", 12),
            command=lambda: self.start_game("single_x"),
            bg="#FF9800",
            fg="white",
            padx=20,
            pady=10,
            width=25
        )
        single_x_btn.pack(pady=5)

        # Two player button
        two_player_btn = tk.Button(
            button_frame,
            text="Two Player",
            font=("Arial", 12),
            command=lambda: self.start_game("two_player"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            width=25
        )
        two_player_btn.pack(pady=5)

        # Quit button
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            font=("Arial", 12),
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10,
            width=25
        )
        quit_btn.pack(pady=5)

    def start_game(self, mode):
        """Start a game with the selected mode.

        Args:
            mode: The game mode ("single_o", "single_x", or "two_player").
        """
        self.game_mode = mode

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Set up game state based on mode
        self.board = Board()
        self.game_over = False

        if mode == "single_o":
            self.human_player = 0  # Player O (goes first)
            self.ai_player = 1
        elif mode == "single_x":
            self.human_player = 1  # Player X (goes second)
            self.ai_player = 0
        else:  # two_player
            self.human_player = None
            self.ai_player = None

        # Set up game UI
        self.setup_game_ui()

        # If single player mode with AI going first
        if mode == "single_x":
            threading.Thread(target=self.ai_move, daemon=True).start()

    def setup_game_ui(self):
        """Set up the game UI after mode selection."""
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Naughts and Crosses",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 10))

        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="Your turn (O)" if self.game_mode == "single_o" else "Your turn (X)" if self.game_mode == "single_x" else "Player O's turn",
            font=("Arial", 14),
            bg="#f0f0f0"
        )
        self.status_label.pack(pady=(0, 10))

        # Error label
        self.error_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 12),
            bg="#f0f0f0",
            fg="red"
        )
        self.error_label.pack(pady=(0, 10))

        # Game board frame
        board_frame = tk.Frame(
            self.main_frame, bg="#333333", highlightthickness=2)
        board_frame.pack(pady=10)

        # Create 3x3 buttons
        self.buttons = []
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    width=6,
                    height=3,
                    font=("Arial", 20, "bold"),
                    command=lambda r=row, c=col: self.on_button_click(r, c),
                    bg="#ffffff",
                    fg="#000000"
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                button_row.append(button)
            self.buttons.append(button_row)

        # Control frame
        control_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        control_frame.pack(pady=10)

        # New Game button
        new_game_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 12),
            command=self.new_game,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Quit button
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            font=("Arial", 12),
            command=self.root.quit,
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10
        )
        quit_button.pack(side=tk.LEFT, padx=5)

        self.update_display()

    def on_button_click(self, row, col):
        """Handle button click on the board.

        Args:
            row: The row of the clicked button (0-2).
            col: The column of the clicked button (0-2).
        """
        if self.game_over:
            return

        # For single player modes, check if it's the human's turn
        if self.game_mode in ["single_o", "single_x"]:
            if self.current_player != self.human_player:
                self.show_error("Not your turn! It's the AI's turn.")
                return

        # For two player mode, allow any human to click (no AI)
        # Check if space is empty
        if self.board.get_space_value((row, col)) != " ":
            self.show_error("Invalid Move - That space is already occupied!")
            return

        # Make the move
        current_symbol = PLAYERS[self.current_player]
        self.board.update_board((row, col), current_symbol)
        self.current_player = (self.current_player + 1) % 2
        self.update_display()

        # Check win/draw after move
        if self.board.is_three_in_row():
            self.end_game(f"{current_symbol} wins!")
            return
        if self.board.is_full():
            self.end_game("Draw!")
            return

        # If single player mode, AI's turn (run in a separate thread)
        if self.game_mode in ["single_o", "single_x"]:
            threading.Thread(target=self.ai_move, daemon=True).start()

    def ai_move(self):
        """Make the AI's move."""
        import time
        time.sleep(0.5)  # Add a small delay for better UX

        # Get AI move
        move = self.network.get_output(
            self.board.flatten(), self.current_player)

        self.board.update_board(move, PLAYERS[self.current_player])
        ai_symbol = PLAYERS[self.current_player]
        self.current_player = (self.current_player + 1) % 2

        # Update display
        self.root.after(0, self.update_display)

        # Check win/draw after AI move
        if self.board.is_three_in_row():
            self.root.after(0, lambda: self.end_game(f"{ai_symbol} wins!"))
            return
        if self.board.is_full():
            self.root.after(0, lambda: self.end_game("Draw!"))

    def update_display(self):
        """Update the button display based on the board state."""
        for row in range(3):
            for col in range(3):
                value = self.board.get_space_value((row, col))
                self.buttons[row][col].config(text=value)

                # Color the buttons
                if value == " ":
                    self.buttons[row][col].config(bg="#ffffff", fg="#000000")
                elif value == "X":
                    self.buttons[row][col].config(bg="#e3f2fd", fg="#1976d2")
                elif value == "O":
                    self.buttons[row][col].config(bg="#f3e5f5", fg="#c2185b")

        # Update status label
        if self.game_over:
            pass  # Status already set
        elif self.game_mode == "two_player":
            current_symbol = PLAYERS[self.current_player]
            self.status_label.config(text=f"Player {current_symbol}'s turn")
        else:  # single_o or single_x
            if self.current_player == self.human_player:
                current_symbol = PLAYERS[self.current_player]
                self.status_label.config(text=f"Your turn ({current_symbol})")
            else:
                ai_symbol = PLAYERS[self.current_player]
                self.status_label.config(text=f"AI's turn ({ai_symbol})")

    def end_game(self, message):
        """End the game and display the result.

        Args:
            message: The message to display (e.g., 'X wins!', 'Draw!').
        """
        self.game_over = True
        self.status_label.config(
            text=message, fg="green" if "wins" in message else "blue", font=("Arial", 14, "bold"))

    def show_error(self, message):
        """Display an error message for 2 seconds then clear it.

        Args:
            message: The error message to display.
        """
        self.error_label.config(text=message, fg="red")
        self.root.after(2000, lambda: self.error_label.config(text=""))

    def new_game(self):
        """Return to the mode selection screen to start a new game."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Reset game state
        self.board = None
        self.human_player = None
        self.ai_player = None
        self.current_player = 0
        self.game_over = False
        self.game_mode = None
        self.buttons = []

        # Show mode selection screen
        self.setup_mode_selection()


def main():
    """Start the GUI."""
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
