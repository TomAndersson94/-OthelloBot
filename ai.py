
from othelloboard import OthelloBoard
from copy import deepcopy
from math import inf
from time import time


class Ai(object):

    def __init__(self, board, player, time_limit):
        self.board = board
        self.player = player
        self.time_limit = time_limit

    def best_move(self):
        _, move = self._minimax(self.board, 5, -inf, inf, self.player)
        return move

    def time_limit_move(self):
        depth = 3
        start_time = time()
        _, move = self._minimax(self.board, depth, -inf, inf, self.player)
        passed_time = time()-start_time
        while(passed_time < self.time_limit/2):
            depth += 1
            _, move = self._minimax(
                self.board, depth, -inf, inf, self.player)
            passed_time = time() - start_time
        return move

    def _evaluate_moves(self, moves):
        def get_weight(move):
            weights = {
                'A1': 200, 'B1': -100, 'C1': 100,  'D1': 50,
                'E1': 50, 'F1': 100, 'G1': -100,  'H1': 200,
                'A2': -100, 'B2': -200, 'C2': -50, 'D2': -50,
                'E2': -50, 'F2': -50, 'G2': -200, 'H2': -100,
                'A3': 100,  'B3': -50, 'C3': 100,   'D3': 0,
                'E3': 0, 'F3': 100,  'G3': -50,  'H3': 100,
                'A4': 50,  'B4': -50,   'C4': 0,   'D4': 0,
                'E4': 0,   'F4': 0,  'G4': -50,   'H4': 50,
                'A5': 50,  'B5': -50,   'C5': 0,   'D5': 0,
                'E5': 0,   'F5': 0,  'G5': -50,   'H5': 50,
                'A6': 100,  'B6': -50, 'C6': 100,   'D6': 0,
                'E6': 0, 'F6': 100,  'G6': -50,  'H6': 100,
                'A7': -100, 'B7': -200, 'C7': -50, 'D7': -50,
                'E7': -50, 'F7': -50, 'G7': -200, 'H7': -100,
                'A8': 200, 'B8': -100, 'C8': 100,  'D8': 50,
                'E8': 50, 'F8': 100, 'G8': -100,  'H8': 200,
            }
            return weights[move]
        return sorted(moves, key=get_weight, reverse=True)

    def _minimax(self, board, depth, alpha, beta, player):
        if depth == 0 or board.current_player == 0:
            return self._static_evaluation(board, player), None

        if player == board.current_player:
            max_score = -inf
            for move in self._evaluate_moves(board.moves[player].keys()):
                temp_board = deepcopy(board)
                temp_board.apply_move(move)
                score = self._minimax(temp_board, depth-1,
                                      alpha, beta, player)[0]
                if max_score < score:
                    max_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score, best_move

        else:
            min_score = inf
            for move in self._evaluate_moves(board.moves[player*-1]):
                temp_board = deepcopy(board)
                temp_board.apply_move(move)
                score = self._minimax(temp_board, depth-1,     
                                       alpha, beta, player)[0]
                if min_score > score:
                    min_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score, best_move

    def _static_evaluation(self, board, player):
        discs = board.score[player] + board.score[player*-1]
        score = 0
        if(board.current_player == 0):
            score += 100000*self._true_score(board, player)
            return score
        elif(discs < 19):
            score += 5*self._mobility(board, player)
            score += 20*self._position_weights(board, player)
            score += 10000*self._corners(board, player)
            score += 10000*self._corner_bonus(board, player)
            return score
        elif(discs < 57):
            score += 10*self._disc_difference(board, player)
            score += 2*self._mobility(board, player)
            score += 10*self._position_weights(board, player)
            score += 100*self._last_disc(board, player)
            score += 10000*self._corners(board, player)
            score += 10000*self._corner_bonus(board, player)
            return score
        else:
            score += 500*self._disc_difference(board, player)
            score += 500*self._last_disc(board, player)
            score += 10000*self._corners(board, player)
            score += 10000*self._corner_bonus(board, player)
            return score

    def _true_score(self, board, player):
        return board.score[player] - board.score[player * -1]

    def _position_weights(self, board, player):
        weights = {
            'A1': 500, 'B1': -100, 'C1': 100,  'D1': 50,
            'E1': 50, 'F1': 100, 'G1': -100,  'H1': 500,
            'A2': -100, 'B2': -200, 'C2': -50, 'D2': -50,
            'E2': -50, 'F2': -50, 'G2': -200, 'H2': -100,
            'A3': 100,  'B3': -50, 'C3': 100,   'D3': 0,
            'E3': 0, 'F3': 100,  'G3': -50,  'H3': 100,
            'A4': 50,  'B4': -50,   'C4': 0,   'D4': 0,
            'E4': 0,   'F4': 0,  'G4': -50,   'H4': 50,
            'A5': 50,  'B5': -50,   'C5': 0,   'D5': 0,
            'E5': 0,   'F5': 0,  'G5': -50,   'H5': 50,
            'A6': 100,  'B6': -50, 'C6': 100,   'D6': 0,
            'E6': 0, 'F6': 100,  'G6': -50,  'H6': 100,
            'A7': -100, 'B7': -200, 'C7': -50, 'D7': -50,
            'E7': -50, 'F7': -50, 'G7': -200, 'H7': -100,
            'A8': 500, 'B8': -100, 'C8': 100,  'D8': 50,
            'E8': 50, 'F8': 100, 'G8': -100,  'H8': 500,
        }

        if('A1' in board.taken):
            weights['B1'] = 0
            weights['C1'] = 0
            weights['D1'] = 0
            weights['A2'] = 0
            weights['B2'] = 0
            weights['C2'] = 0
            weights['D2'] = 0
            weights['A3'] = 0
            weights['B3'] = 0
            weights['C3'] = 0
            weights['A4'] = 0
            weights['B4'] = 0
        if('H1' in board.taken):
            weights['G1'] = 0
            weights['F1'] = 0
            weights['E1'] = 0
            weights['H2'] = 0
            weights['G2'] = 0
            weights['F2'] = 0
            weights['E2'] = 0
            weights['H3'] = 0
            weights['G3'] = 0
            weights['F3'] = 0
            weights['H4'] = 0
            weights['G4'] = 0
        if('A8' in board.taken):
            weights['B8'] = 0
            weights['C8'] = 0
            weights['D8'] = 0
            weights['A7'] = 0
            weights['B7'] = 0
            weights['C7'] = 0
            weights['D7'] = 0
            weights['A6'] = 0
            weights['B6'] = 0
            weights['C6'] = 0
            weights['A5'] = 0
            weights['B5'] = 0
        if('H8' in board.taken):
            weights['G8'] = 0
            weights['F8'] = 0
            weights['E8'] = 0
            weights['H7'] = 0
            weights['G7'] = 0
            weights['F7'] = 0
            weights['E7'] = 0
            weights['H6'] = 0
            weights['G6'] = 0
            weights['F6'] = 0
            weights['H5'] = 0
            weights['G5'] = 0

        score = 0
        for xy in board.taken:
            disc = board.get_disc_value(xy)
            if disc == player:
                score += weights[xy]
        return score

    def _disc_difference(self, board, player):
        diff = board.score[player] - board.score[player * -1]
        total = board.score[player] + board.score[player * -1]
        return 100 * diff / total

    def _corners(self, board, player):
        corners = ['A1', 'H1', 'A8', 'H8']
        player = 0
        op = 0
        for corner in corners:
            disc = board.get_disc_value(corner)
            if disc == player:
                player += 1
            if disc == player * -1:
                op += 1
        return 100 * (player - op)/(player + op + 1)

    def _last_disc(self, board, player):
        remaining_discs = 64 - board.score[player] - board.score[player * -1]
        if (remaining_discs % 2):
            return -1
        else:
            return 1

    def _mobility(self, board, player):
        own_moves = sum([len(x) for x in board.moves[player].values()])
        op_moves = sum([len(x) for x in board.moves[player*-1].values()])
        return 100 * (own_moves - op_moves) / (own_moves + op_moves + 1)

    def _corner_bonus(self, board, player):
        def _stable_discs(player):
            directions = {'A1': [1, 'H', 1, '8'], 'H1': [-1, 'A', 1, '8'],
                          'A8': [1, 'H', -1, '1'], 'H8': [-1, 'A', -1, '1']}
            stables = 0
            for key, value in directions.items():
                dx, xstop, dy, ystop = value
                for x in range(ord(key[0]), ord(xstop)+dx, dx):
                    xy = chr(x)+key[1]
                    if board.get_disc_value(xy) == player:
                        for y in range(ord(key[1])+dy, ord(ystop)+dy, dy):
                            xy = chr(x)+chr(y)
                            if board.get_disc_value(xy) == player:
                                stables += 1
                            else:
                                break
                    else:
                        break
            return stables
        own_bonus = _stable_discs(player)
        op_bonus = _stable_discs(player * -1)
        return own_bonus - op_bonus
