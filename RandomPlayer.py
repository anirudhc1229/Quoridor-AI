import numpy as np

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board, valid_moves):
        a = np.random.randint(len(valid_moves))
        return valid_moves[a]

