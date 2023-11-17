import random
from collections import defaultdict
from  TicTacToe_board import TicTacToe
import tqdm
from vs_human import vs_human_game

class MonteCarlo:
    def __init__(self,episodes=10000):
        self.values = defaultdict(lambda: [0, 0])  # Initialize all states' values to [0, 0] where [0] is the total reward and [1] is the number of visits

        # Define symbols
        self.X = '1'
        self.O = '2'
        self.empty = '0'
        self.traininig_games = episodes

    def update_values(self, episode):
        for state, reward in episode:
            self.values[state][1] += 1
            self.values[state][0] += (reward-self.values[state][0])/self.values[state][1]

    def calculate_return(self, rewards, gamma=1.0):
        total_reward = 0
        for t in range(len(rewards)):
            total_reward = rewards[t] + gamma * total_reward
        return total_reward


    def epsilon_greedy(self, state, symbol, epsilon=0.1):
        opponent_symbol = '1' if symbol == '2' else '2'
        available_moves = [i for i, x in enumerate(state) if x == self.empty]
        if random.random() < epsilon:
            return random.choice(available_moves)
        else:
            best_move = available_moves[0]
            best_value = float("-inf")
            if available_moves :
                for move in available_moves:
                    next_state = state[:move] + symbol + state[move+1:]

                    if next_state in self.values.keys() and self.values[next_state][0] > best_value:
                          best_value = self.values[next_state][0]
                          best_move = move


            return best_move





    def reward (self, agent_symbol , game):
        winner = game.check_winner()
        next_state= game.board
        if winner == agent_symbol:
            return 100

        else:
            return  -80

        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                               (0, 3, 6), (1, 4, 7), (2, 5, 8),
                               (0, 4, 8), (2, 4, 6)]

        opponent_symbol = '2' if agent_symbol == '1' else '1'
        reward =0
        if next_state[combination[0]] == next_state[combination[1]]  == opponent_symbol :
            if next_state[combination[2]] == agent_symbol :
              reward+=5
            else  :
              reward-=5

        if next_state[combination[0]] == next_state[combination[2]]  == opponent_symbol :
          if next_state[combination[1]] == agent_symbol :

            reward+=5
          else  :
            reward-=5

        if next_state[combination[2]] == next_state[combination[1]]  == opponent_symbol :
          if next_state[combination[0]] == agent_symbol :
            reward+=5
          else  :
            reward-=5

        return reward





    def train (self,episodes):

        for i in  tqdm.tqdm(range(episodes), desc="Monte Carlo Training"):
            agent1_symbol = '1'
            agent2_symbol= '2'
            game = TicTacToe()
            episode1 = []
            episode2 = []

            while game.check_winner() is None:
                current_state = game.board
                available_moves = game.available_moves()
                if available_moves:
                    action = self.epsilon_greedy(current_state,agent1_symbol)
                    game.make_move(action, agent1_symbol)
                    current_state = game.board
                    episode1.append((current_state, 0))  # Add current state with reward 0

                current_state = game.board
                available_moves = game.available_moves()
                if available_moves:
                    action = self.epsilon_greedy(current_state,agent2_symbol)
                    game.make_move(action, agent2_symbol)
                    current_state = game.board
                    episode2.append((current_state, 0))  # Add current state with reward 0



            reward1 = self.reward(agent1_symbol,game)
            reward2 = self.reward(agent2_symbol,game)

            # Update rewards in the episode with the final reward
            for i in range(len(episode1)):
                state, _ = episode1[i]
                episode1[i] = (state, reward1)

            self.update_values(episode1)

            for i in range(len(episode2)):
                state, _ = episode2[i]
                episode2[i] = (state, reward2)


            self.update_values(episode2)

        print("Training complete.")
