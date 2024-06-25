import numpy as np
import matplotlib.pyplot as plt

class Tablero:
    def __init__(self):
        self.rows = 2
        self.cols = 3
        self.state = np.array(['1', '2', '3', '4', '5', 'X']).reshape(self.rows, self.cols)
        np.random.shuffle(self.state.flat)

    def reset(self):
        np.random.shuffle(self.state.flat)
        return self.state

    def find_X(self):
        return np.argwhere(self.state == 'X')[0]

    def step(self, action):
        row, col = self.find_X()
        if action == 0 and row > 0:
            self.state[row, col], self.state[row-1, col] = self.state[row-1, col], self.state[row, col]
        elif action == 1 and row < self.rows - 1:
            self.state[row, col], self.state[row+1, col] = self.state[row+1, col], self.state[row, col]
        elif action == 2 and col > 0:
            self.state[row, col], self.state[row, col-1] = self.state[row, col-1], self.state[row, col]
        elif action == 3 and col < self.cols - 1:
            self.state[row, col], self.state[row, col+1] = self.state[row, col+1], self.state[row, col]

        done = self.is_solved()
        # Recompensa: -1 si no está resuelto, 0 si está resuelto
        reward = -1 if not done else 0
        return self.state, reward, done

    def is_solved(self):
        return np.array_equal(self.state, np.array(['1', '2', '3', '4', '5', 'X']).reshape(self.rows, self.cols))

    def get_state(self):
        return self.state


def train_agent(episodes, epsilon, alpha, gamma, max_steps_per_episode):
    q_table = np.zeros((6, 4))  # Simplificación: 6 posiciones para 'X', 4 acciones
    rewards = []

    for episode in range(episodes):
        env = Tablero()
        print("Estado inicial del tablero:")
        print(env.get_state())
        total_rewards = 0
        done = False
        steps = 0

        while not done and steps < max_steps_per_episode:
            state = env.find_X()[0]  # Simplificación: estado basado en la posición de 'X'
            if np.random.uniform(0, 1) < epsilon:
                action = np.random.choice(4)  # Explorar: acción aleatoria
            else:
                action = np.argmax(q_table[state])  # Explotar: mejor acción basada en q_table

            _, reward, done = env.step(action)
            total_rewards += reward

            new_state = env.find_X()[0]
            q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[new_state]) - q_table[state, action])

            steps += 1

        rewards.append(total_rewards)

    return q_table, rewards
# Hiperparámetros
episodes = 1000
# Coeficiente de Aprendizaje 
epsilon = 0.1
# Tasa de Aprendizaje
alpha = 0.1
# Factor de Descuento
gamma = 0.9
# Número máximo de pasos por episodio
max = 100

q_table, rewards = train_agent(episodes, epsilon, alpha, gamma , max)

print("Tabla Q final:")
print(q_table)
