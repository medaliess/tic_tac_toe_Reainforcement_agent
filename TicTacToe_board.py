import random
import itertools

class TicTacToe:
    def __init__(self):
        self.board = '0' * 9  # Initialize board as a binary string

    def print_board(self):
        print("-------------")
        for i in range(0, 9, 3):
            row = "| " + " | ".join(["X" if cell == '1' else "O" if cell == '2' else " " for cell in self.board[i:i+3]]) + " |"
            print(row)
            print("-------------")
    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == '0']

    def make_move(self, position, symbol):
        self.board = self.board[:position] + symbol + self.board[position+1:]

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] == '1':
                return '1'  # Agent wins
            elif self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] == '2':
                return '2'  # Computer wins
        if '0' not in self.board:
            return 'Draw'
        return None


