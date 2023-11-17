from TicTacToe_board import TicTacToe
import random

def vs_human_game(self):
        agent_symbol = random.choice(['1','2'])  # Agent always plays as 'X'
        human_symbol = '1' if agent_symbol == '2' else '2'  # Human player always plays as 'O'
        game = TicTacToe()

        while game.check_winner() is None:  # Continue until there is a winner or draw
            current_state = game.board
            if agent_symbol == '1' :
                available_moves = game.available_moves()
                if available_moves:
                    # Agent's action
                    action = self.epsilon_greedy(current_state, agent_symbol,0)
                    game.make_move(action, agent_symbol)
                    current_state = game.board
                    print("Current Board:")
                    game.print_board()
                    winner = game.check_winner()
                    if winner == agent_symbol:
                        print ("Agent wins")
                        break
                    elif winner == human_symbol:
                        print ("You win")
                    elif winner == 'Draw':
                        print ("Draw")

                available_moves = game.available_moves()
                if available_moves:
                    # Human player's action

                    while True:
                        try:
                            move = int(input("Enter your move (1-9): ")) - 1
                            if move in game.available_moves():
                                game.make_move(move, human_symbol)
                                break
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number between 1 and 9.")
                    winner = game.check_winner()
                    if winner == agent_symbol:
                        print ("Agent wins")
                    elif winner == human_symbol:
                        print ("You win")
                    elif winner == 'Draw':
                        print ("Draw")

            else:
                available_moves = game.available_moves()
                if available_moves:
                    # Human player's action

                    while True:
                        try:
                            move = int(input("Enter your move (1-9): ")) - 1
                            if move in game.available_moves():
                                game.make_move(move, human_symbol)
                                break
                            else:
                                print("Invalid move. Try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number between 1 and 9.")
                    winner = game.check_winner()
                    if winner == agent_symbol:
                        print ("Agent wins")
                    elif winner == human_symbol:
                        print ("You win")
                    elif winner == 'Draw':
                        print ("Draw")

                available_moves = game.available_moves()
                if available_moves:
                    current_state = game.board
                    # Agent's action
                    action = self.epsilon_greedy(current_state, agent_symbol,0)
                    game.make_move(action, agent_symbol)
                    current_state = game.board
                    print("Current Board:")
                    game.print_board()
                    winner = game.check_winner()
                    if winner == agent_symbol:
                        print ("Agent wins")
                    elif winner == human_symbol:
                        print ("You win")
                    elif winner == 'Draw':
                        print ("Draw")