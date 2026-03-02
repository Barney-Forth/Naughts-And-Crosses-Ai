import random
from Game import Board, PLAYERS
from NeuralNet import Network


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
                        neuron.weights[i] += random.gauss(0, 0.1)
                if random.random() < mutation_rate:
                    neuron.bias += random.gauss(0, 0.1)
        return child_net

    def train(self, num_of_rounds: int, mutation_rate: float):
        """Train the network for a specified number of generations.

        Args:
            num_of_rounds: The number of training rounds (generations) to run.
            mutation_rate: Probability (0-1) that each weight/bias is mutated.
        """
        for i in range(num_of_rounds):
            child_net = self._create_child_net(mutation_rate)
            if self._play_nets(self._net, child_net) == child_net:
                self._net = child_net

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
                        print(
                            f"Player {player} ({PLAYERS[player]}) moves to {move}")
                    else:
                        print("NOT WORKING1")
                except (TypeError, ValueError):
                    print("NOT WORKING")

            board.update_board(move, PLAYERS[player])

            if board.is_three_in_row():
                print(board)
                return net1 if player == 0 else net2

            player = (player + 1) % 2

        print(board)
        return None


if __name__ == "__main__":
    trainer = Trainer("best_net")
    trainer.train(1000, 0.1)
    print("Training complete.")
