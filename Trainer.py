import random
from Game import Board, PLAYERS
from NeuralNet import Network
import time

# Change these values to change the properites of training
TRAINING_NET = "best_net"  # String of the name of the net to train
TRAINING_CYCLES = 100000  # int of the number of training cycles
MUTATION_RATE = 0.7  # float between 0 and 1 defining the mutation rate


class Trainer:
    """Trains a neural network using evolutionary algorithms.

    Creates child networks with mutations and evaluates them against the parent
    network. Keeps the child if it wins more games.
    """

    def __init__(self, net_name: str):
        """Initialize the trainer with a network to train.

        Args:
            net_name: The name/identifier of the network to train or load.
        """
        self._net = Network(net_name)

    def _create_child_net(self, mutation_rate: float) -> Network:
        """Create a mutated copy of the current network.

        Args:
            mutation_rate: Probability (0-1) that each weight/bias is mutated.

        Returns:
            A new Network with mutated weights and biases.
        """
        child_net = Network(self._net.name)
        for layer in child_net._layers:
            for neuron in layer.neurons:
                for i in range(len(neuron.weights)):
                    if random.random() < mutation_rate:
                        neuron.weights[i] += random.gauss(0, 1.0)
                if random.random() < mutation_rate:
                    neuron.bias += random.gauss(0, 1.0)
        return child_net

    def train(self, num_of_rounds: int, mutation_rate: float):
        """Train the network for a specified number of generations.

        Args:
            num_of_rounds: The number of training rounds (generations) to run.
            mutation_rate: Probability (0-1) that each weight/bias is mutated.
        """
        start_time = time.time()

        for i in range(num_of_rounds):
            child_net = self._create_child_net(mutation_rate)

            # Best of three: play 3 games
            child_wins = 0
            parent_wins = 0

            for game in range(3):
                winner = self._play_nets(self._net, child_net)
                if winner == child_net:
                    child_wins += 1
                elif winner == self._net:
                    parent_wins += 1

            # If child wins majority (2+ out of 3), replace parent
            if child_wins > parent_wins:
                self._net = child_net

            # Print progress every 10 rounds
            if (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                rounds_per_sec = (i + 1) / elapsed
                remaining_rounds = num_of_rounds - (i + 1)
                time_remaining = remaining_rounds / rounds_per_sec

                print(f"Round {i + 1}/{num_of_rounds} - "
                      f"Elapsed: {elapsed:.1f}s - "
                      f"Est. remaining: {time_remaining:.1f}s")

        self._net.save_net_values()

    def _play_nets(self, net1: Network, net2: Network) -> Network:
        """Simulate a game between two networks.

        Args:
            net1: The first network (plays as player 0).
            net2: The second network (plays as player 1).

        Returns:
            The winning network, or None if the game ends in a draw.
        """
        board = Board()
        player = 0

        while not board.is_full() and not board.is_three_in_row():
            valid = False
            while not valid:
                if player == 0:
                    move = net1.get_output(board.flatten(), player)
                else:
                    move = net2.get_output(board.flatten(), player)

                try:
                    if board.get_space_value(move) == " ":
                        valid = True
                        # print(
                        # f"Player {player} ({PLAYERS[player]}) moves to {move}")
                    else:
                        print("NOT WORKING1")
                except (TypeError, ValueError):
                    print("NOT WORKING")

            board.update_board(move, PLAYERS[player])

            if board.is_three_in_row():
                # print(board)
                return net1 if player == 0 else net2

            player = (player + 1) % 2

        # print(board)
        return None


if __name__ == "__main__":
    trainer = Trainer(TRAINING_NET)
    trainer.train(TRAINING_CYCLES, MUTATION_RATE)
    print("Training complete.")
