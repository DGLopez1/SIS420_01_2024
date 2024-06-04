import numpy as np

class Board():
    def __init__(self):
        self.state = np.zeros((4,4))  # Cambiado a 4x4

    def valid_moves(self):
        return [(i, j) for j in range(4) for i in range(4) if self.state[i, j] == 0]  # Cambiado a 4

    def update(self, symbol, row, col):
        if self.state[row, col] == 0:
            self.state[row, col] = symbol
        else:
            raise ValueError("movimiento invalido !")

    def is_game_over(self):
        # comprobar filas y columnas
        if (self.state.sum(axis=0) == 4).sum() >= 1 or (self.state.sum(axis=1) == 4).sum() >= 1:  # Cambiado a 4
            return 1
        if (self.state.sum(axis=0) == -4).sum() >= 1 or (self.state.sum(axis=1) == -4).sum() >= 1:  # Cambiado a 4
            return -1 
        # comprobar diagonales
        diag_sums = [
            sum([self.state[i, i] for i in range(4)]),  # Cambiado a 4
            sum([self.state[i, 4 - i - 1] for i in range(4)]),  # Cambiado a 4
        ]
        if diag_sums[0] == 4 or diag_sums[1] == 4:  # Cambiado a 4
            return 1
        if diag_sums[0] == -4 or diag_sums[1] == -4:  # Cambiado a 4
            return -1        
        # empate
        if len(self.valid_moves()) == 0:
            return 0
        # seguir jugando
        return None

    def reset(self):
        self.state = np.zeros((4,4))  # Cambiado a 4x4