# Naughts-and-Crosses Ai
Naughts-and-Crosses is a personal learning Python project I used to learn the baisics of neural networks, and evolutionary machine learning algorithms.
Development has stopped for now but plan to return to the project in the future to work on feturs outlined in the roadmap.

## Usage
To train an Ai model run Trainer.py. To eddid the perameters of training edit the constants at the top of the script listed below.
```python
# Change these values to change the properites of training
TRAINING_NET = "best_net" # String of the name of the net to train
TRAINING_CYCLES = 100000 # int of the number of training cycles
MUTATION_RATE = 0.7 # float between 0 and 1 defining the mutation rate
```

To play against a Ai in the terminal run Game.py. To change the model change the name at the top os the script as shown bellow.
```python
# Change this to chage the net to play against
PLAYING_NET = "best_net"
```

To play against a person or an Ai with a GUI run GUI.py. To change the model change the name at the top os the script as shown bellow.
```python
# Change this to chage the net to play against
PLAYING_NET = "best_net"
```

## Roadmap
- Add running all nodes in a layer in parallel
- Creating multiple children per generation of training
- Add a userinterface for training a new model
