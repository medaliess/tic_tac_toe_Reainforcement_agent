
import random
from collections import defaultdict
from  TicTacToe_board import TicTacToe
import tqdm
import itertools
from vs_human import vs_human_game


def reward_function( next_state, agent_symbol):


  if agent_symbol == '1' :
      if next_state.count('0') > 4 :
        return 0
  else  :
       if next_state.count('0') > 5 :
        return 0



  opponent_symbol = '2' if agent_symbol == '1' else '1'
  winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                              (0, 3, 6), (1, 4, 7), (2, 5, 8),
                              (0, 4, 8), (2, 4, 6)]

  reward = 0
  usefull=False
  for combination in winning_combinations:


# Check if the agent wins in the next state
      if next_state[combination[0]] == next_state[combination[1]] == next_state[combination[2]] == agent_symbol:
          return 100

      if next_state[combination[0]] == next_state[combination[1]] == next_state[combination[2]] == opponent_symbol:
        return -50

      if next_state[combination[0]] == next_state[combination[1]]  == agent_symbol and  next_state[combination[2]]=='0' :
        usefull=True
        reward+=5
      if next_state[combination[0]] == next_state[combination[2]] == agent_symbol  and  next_state[combination[1]]=='0' :
          usefull=True
          reward+=5

      if next_state[combination[1]] == next_state[combination[2]] == agent_symbol and  next_state[combination[0]]=='0':

          usefull=True
          reward+=5

      if next_state[combination[0]] == next_state[combination[1]]  == opponent_symbol :
        if next_state[combination[2]] == agent_symbol :
          usefull=True
          reward+=5
        else  :
          reward-=5

      if next_state[combination[0]] == next_state[combination[2]]  == opponent_symbol :
        if next_state[combination[1]] == agent_symbol :
          usefull=True
          reward+=5
        else  :
          reward-=5

      if next_state[combination[2]] == next_state[combination[1]]  == opponent_symbol :
        if next_state[combination[0]] == agent_symbol :
          usefull=True
          reward+=5
        else  :
          reward-=5


  if not usefull :
    reward -=5

  return reward



class TD_lambda:
    def __init__(self, alpha=0.1, gamma=0.9, lambda_=0.5, ):
        self.values = {}
        self.eligibilities_X = {}
        self.eligibilities_O = {}  # Initialize eligibility traces
        self.alpha = alpha
        self.X = '1'
        self.O = '2'
        self.empty = '0'
        self.gamma = gamma
        self.lambda_ = lambda_
        self.update_frequency = 2
        self.steps = 0

        # Generate all possible board configurations
        states = [''.join(board) for board in itertools.product('012', repeat=9)]
        for state in states:
            self.values[state] = 0


    def update_eligibilities(self,eligibilities, state):
        eligibilities.setdefault(state , 1)
        for s in eligibilities.keys():
            eligibilities[s] *= self.lambda_


    def update_values(self,eligibilities, reward, next_state):
        delta = reward - self.values[next_state]
        for state, eligibility in eligibilities.items():
            self.values[state] += self.alpha * delta * eligibility

    def epsilon_greedy(self, state, symbol,  epsilon=0.3):
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
                    opponent__moves = [i for i, x in enumerate(next_state) if x == self.empty]
                    if opponent__moves :
                        for opponent__move in opponent__moves  :
                            opp_board = next_state[:opponent__move] + opponent_symbol + next_state[opponent__move+1:]

                            value = self.values[opp_board]
                            if (value > best_value) :
                                best_value = value
                                best_move = move



            return best_move

    def Train(self, episodes=1000):

        for episode in tqdm.tqdm(range(episodes),desc="TD_lambda Training"):

                self.eligibilities_X = {}
                self.eligibilities_O = {}

                agent1_symbol = '1'
                agent2_symbol = '2'
                game = TicTacToe()

                # Agent 1 action
                board = game.board
                available_moves = game.available_moves()
                action = self.epsilon_greedy(board, agent1_symbol)
                game.make_move(action, agent1_symbol)

                # Agent 2 action
                agent2_first_state = game.board
                available_moves = game.available_moves()
                action = self.epsilon_greedy(board, agent2_symbol)
                game.make_move(action, agent2_symbol)



                while game.check_winner() is  None  :
                    agent1_first_state = game.board
                    available_moves = game.available_moves()

                    action = self.epsilon_greedy(agent1_first_state, agent1_symbol)
                    game.make_move(action, agent1_symbol)
                    agent2_next_state = game.board

                    self.update_eligibilities( self.eligibilities_X ,agent1_first_state)

                    self.update_eligibilities( self.eligibilities_O ,agent2_first_state)
                    self.update_eligibilities( self.eligibilities_O ,agent2_next_state)

                    self.steps += 1

                    if game.check_winner() is not None or self.steps == self.update_frequency:
                        reward = reward_function(agent2_next_state, '2')
                        self.update_values(self.eligibilities_O, reward, agent2_next_state)
                        self.eligibilities_O = {state: 0 for state in self.eligibilities_O.keys()}
                        self.steps = 0


                    agent2_first_state = game.board
                    available_moves = game.available_moves()
                    if available_moves :
                        action = self.epsilon_greedy(agent2_first_state, agent2_symbol)
                        game.make_move(action, agent2_symbol)


                        agent1_next_state = game.board

                        self.update_eligibilities( self.eligibilities_X ,agent1_next_state)
                        if game.check_winner() is not None or self.steps == self.update_frequency:
                            reward = reward_function(agent1_next_state, '1')
                            self.update_values(self.eligibilities_X, reward, agent1_next_state)
                            self.eligibilities_X = {state: 0 for state in self.eligibilities_X.keys()}
                            self.steps = 0


                board=game.board
                self.update_eligibilities( self.eligibilities_O , board)
                available_moves = game.available_moves()
                if available_moves:
                    action = random.choice(available_moves)
                    game.make_move(action, agent1_symbol)
                    board=game.board
                    self.update_eligibilities( self.eligibilities_O , board)
                    reward = reward_function(board, '2')
                    self.update_values(self.eligibilities_O, reward, board)
