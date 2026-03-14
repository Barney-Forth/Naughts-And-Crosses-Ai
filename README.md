# Naughts-and-Crosses AI

Naughts-and-Crosses is a personal learning Python project I used to learn the basics of neural networks, and evolutionary machine learning algorithms.

Development has stopped for now but plan to return to the project in the future to work on features outlined in the roadmap.

## Requirements

The numpy library is required to run the project. It can be installed by the command bellow
```console
pip install numpy
```

## Usage

To train an AI model run Trainer.py. To edit the parameters of training edit the constants at the top of the script listed below.
```python
# Change these values to change the properties of training
TRAINING_NET = "best_net" # String of the name of the net to train
TRAINING_CYCLES = 100000 # int of the number of training cycles
MUTATION_RATE = 0.7 # float between 0 and 1 defining the mutation rate
```

To play against a AI in the terminal run Game.py. To change the model change the name at the top os the script as shown bellow.
```python
# Change this to change the net to play against
PLAYING_NET = "best_net"
```

To play against a person or an AI with a GUI run GUI.py. To change the model change the name at the top os the script as shown bellow.
```python
# Change this to change the net to play against
PLAYING_NET = "best_net"
```

## Roadmap

- Add running all nodes in a layer in parallel
- Creating multiple children per generation of training
- Add a user interface for training a new model
