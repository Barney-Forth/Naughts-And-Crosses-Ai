import random
from copy import deepcopy
from Game import Board, PLAYERS
from NeuralNet import Network


class Trainer:
    def __init__(self, net_name: str):
        self._net = Network()
        self._net.load_net_values(net_name)

    def create_child_net(self, mutation_rate: float) -> Network:
        child_net = deepcopy(self._net)
        for layer in child_net._layers:
            for neuron in layer.neurons:
                for i in range(len(neuron.weights)):
                    if random.random() < mutation_rate:
                        neuron.weights[i] += random.gauss(0, 0.1)
                if random.random() < mutation_rate:
                    neuron.bias += random.gauss(0, 0.1)
        return child_net

    def train(self, num_of_rounds: int, mutation_rate: float):
        for i in range(num_of_rounds):
            child_net = self.create_child_net(mutation_rate)
            if self.play_nets(self._net, child_net) == child_net:
                self._net = child_net

        self._net.save_net_values()

    def play_nets(self, net1: Network, net2: Network) -> Network:
        board = Board()
        player = 0

        while not board.is_full() and not board.is_three_in_row():
            if player == 0:
                move = net1.get_output(board.flatten(), player)
            else:
                move = net2.get_output(board.flatten(), player)

            board.update_board(move, PLAYERS[player])

            if board.is_three_in_row():
                return net1 if player == 0 else net2

            player = (player + 1) % 2

        return None
