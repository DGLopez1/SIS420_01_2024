import numpy as np
import matplotlib.pyplot as plt

class Tablero:
    def __init__(self):
        # Inicializa un tablero de 2x3 con los números del 1 al 5 y una 'X'
        self.rows = 2
        self.cols = 3
        self.state = np.array(['1', '2', '3', '4', '5', 'X']).reshape(self.rows, self.cols)
        np.random.shuffle(self.state.flat)  # Mezcla los elementos del tablero

    def reset(self):
        # Reinicia el tablero mezclando sus elementos
        np.random.shuffle(self.state.flat)
        return self.state

    def find_X(self):
        # Encuentra la posición de la 'X' en el tablero
        return np.argwhere(self.state == 'X')[0]

    def step(self, action):
        # Realiza un movimiento en el tablero según la acción dada
        row, col = self.find_X()
        # Mueve la 'X' en la dirección especificada si es posible
        if action == 0 and row > 0:  # Arriba
            self.state[row, col], self.state[row-1, col] = self.state[row-1, col], self.state[row, col]
        elif action == 1 and row < self.rows - 1:  # Abajo
            self.state[row, col], self.state[row+1, col] = self.state[row+1, col], self.state[row, col]
        elif action == 2 and col > 0:  # Izquierda
            self.state[row, col], self.state[row, col-1] = self.state[row, col-1], self.state[row, col]
        elif action == 3 and col < self.cols - 1:  # Derecha
            self.state[row, col], self.state[row, col+1] = self.state[row, col+1], self.state[row, col]

        done = self.is_solved()  # Verifica si el tablero está en estado objetivo
        reward = -1 if not done else 0  # Recompensa: -1 si no está resuelto, 0 si está resuelto
        return self.state, reward, done

    def is_solved(self):
        # Verifica si el tablero está en el estado objetivo
        return np.array_equal(self.state, np.array(['1', '2', '3', '4', '5', 'X']).reshape(self.rows, self.cols))

    def get_state(self):
        # Devuelve el estado actual del tablero
        return self.state


def train_agent(episodes, epsilon, alpha, gamma, max_steps_per_episode):
    # Entrena un agente para resolver el tablero
    q_table = np.zeros((6, 4))  # Tabla Q: 6 posiciones para 'X', 4 acciones posibles
    rewards = []  # Almacena las recompensas totales por episodio

    for episode in range(episodes):
        env = Tablero()  # Crea una instancia del tablero
        print("Estado inicial del tablero:")
        print(env.get_state())
        total_rewards = 0
        done = False
        steps = 0

        while not done and steps < max_steps_per_episode:
            state = env.find_X()[0]  # Estado actual basado en la posición de 'X'
            if np.random.uniform(0, 1) < epsilon:
                action = np.random.choice(4)  # Exploración: elige una acción aleatoria
            else:
                action = np.argmax(q_table[state])  # Explotación: elige la mejor acción según Q-table

            _, reward, done = env.step(action)  # Realiza la acción y recibe la nueva recompensa y estado
            total_rewards += reward

            new_state = env.find_X()[0]  # Nuevo estado después de realizar la acción
            # Actualiza Q-table usando la ecuación de Bellman
            q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[new_state]) - q_table[state, action])

            steps += 1

        rewards.append(total_rewards)  # Almacena la recompensa total del episodio

    return q_table, rewards

# Hiperparámetros para el entrenamiento
episodes = 1000  # Número de episodios para entrenar
epsilon = 0.1  # Coeficiente de exploración
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
max = 100  # Número máximo de pasos por episodio

q_table, rewards = train_agent(episodes, epsilon, alpha, gamma , max)  # Entrena el agente

print("Tabla Q final:")
print(q_table)  # Muestra la tabla Q final después del entrenamiento