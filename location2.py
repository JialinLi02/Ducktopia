import numpy as np
import random
import pandas as pd
import time 

# Load the CSV file
csv_file = "/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/food_scores.csv"
data = pd.read_csv(csv_file)



# Create the grid dictionary from the CSV data
grid = dict(zip(data["Location"], data["Foodscore"]))

# Filter squares with scores >= 8
high_score_squares = {square: score for square, score in grid.items() if score >= 8}

# Function to calculate Manhattan distance between two squares
def manhattan_distance(square1, square2):
    row1 = ord(square1[0]) - ord('A')
    col1 = int(square1[1:]) - 1
    row2 = ord(square2[0]) - ord('A')
    col2 = int(square2[1:]) - 1
    return abs(row1 - row2) + abs(col1 - col2)

# Define the Q-learning environment
class GridEnvironment:
    def __init__(self, grid):
        self.grid = grid

    def reset(self, start_square):
        self.selected_squares = [start_square]
        self.remaining_squares = set(self.grid.keys()) - {start_square}
        return self.selected_squares

    def step(self, action):
        # Add the selected square to the list
        self.selected_squares.append(action)
        self.remaining_squares.remove(action)

        # Calculate reward: score of the square minus average distance penalty
        reward = self.grid[action]
        if len(self.selected_squares) > 1:
            avg_distance = np.mean([manhattan_distance(action, s) for s in self.selected_squares])
            reward -= 0.1 * avg_distance  # Adjust penalty weight as needed

        # Check if we have selected 9 squares
        done = len(self.selected_squares) >= 9

        return self.selected_squares, reward, done

# Define the Q-learning agent
class QLearningAgent:
    def __init__(self, grid, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.grid = grid
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}  # Q-table: key = (state, action), value = Q-value

    def get_q_value(self, state, action):
        return self.q_table.get((tuple(state), action), 0.0)

    def choose_action(self, state, remaining_squares):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(list(remaining_squares))  # Explore
        else:
            # Exploit: choose the action with the highest Q-value
            q_values = [self.get_q_value(state, a) for a in remaining_squares]
            return list(remaining_squares)[np.argmax(q_values)]

    def update_q_value(self, state, action, reward, next_state):
        old_value = self.get_q_value(state, action)
        next_max = max([self.get_q_value(next_state, a) for a in set(self.grid.keys()) - set(next_state)])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[(tuple(state), action)] = new_value

# Train the Q-learning agent for a given starting square
def train_agent(agent, env, start_square, episodes=1000):
    for episode in range(episodes):
        state = env.reset(start_square)
        done = False

        while not done:
            action = agent.choose_action(state, env.remaining_squares)
            next_state, reward, done = env.step(action)
            agent.update_q_value(state, action, reward, next_state)
            state = next_state

# Evaluate all starting squares and select the best one
def find_best_starting_square(grid, high_score_squares, episodes=1000):
    best_start_square = None
    best_squares = []
    best_total_score = -1
    best_avg_distance = float('inf')

    total_squares = len(high_score_squares)
    start_time = time.time()

    for i, start_square in enumerate(high_score_squares.keys()):
        env = GridEnvironment(grid)
        agent = QLearningAgent(grid)

        # Train the agent for this starting square
        train_agent(agent, env, start_square, episodes)

        # Use the trained agent to select the best squares
        state = env.reset(start_square)
        done = False
        while not done:
            action = agent.choose_action(state, env.remaining_squares)
            next_state, reward, done = env.step(action)
            state = next_state

        # Calculate total score and average distance
        total_score = sum(grid[square] for square in state)
        avg_distance = np.mean([manhattan_distance(state[i], state[j]) for i in range(len(state)) for j in range(i + 1, len(state))])

        # Update the best starting square
        if total_score > best_total_score or (total_score == best_total_score and avg_distance < best_avg_distance):
            best_start_square = start_square
            best_squares = state
            best_total_score = total_score
            best_avg_distance = avg_distance

        # Progress tracking
        elapsed_time = time.time() - start_time
        progress = (i + 1) / total_squares * 100
        estimated_total_time = elapsed_time / (i + 1) * total_squares
        remaining_time = estimated_total_time - elapsed_time

        print(f"Progress: {progress:.2f}% | "
              f"Elapsed: {elapsed_time / 60:.2f} min | "
              f"Remaining: {remaining_time / 60:.2f} min | "
              f"Best Score: {best_total_score}")

    return best_start_square, best_squares, best_total_score, best_avg_distance

# Find the best starting square and the corresponding squares
best_start_square, best_squares, best_total_score, best_avg_distance = find_best_starting_square(grid, high_score_squares)

print("\nBest starting square:", best_start_square)
print("Selected squares:", best_squares)
print("Total score:", best_total_score)
print("Average distance:", best_avg_distance)