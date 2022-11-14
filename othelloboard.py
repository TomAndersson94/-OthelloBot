class OthelloBoard(object):

    def __init__(self):
        self.score = {}
        self.current_player = -1
        self.moves = {}
        self.reset_board()

    def reset_board(self):
        self._possible = set()
        self.taken = set()
        self._gameboard = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = -1
        self._add_disc('D4')
        self._add_disc('E5')
        self.current_player = 1
        self._add_disc('D5')
        self._add_disc('E4')
        self.score = {-1: 2, 1: 2}
        self._update_moves()

    def _to_num(self, xy):
        x, y = xy
        LUT = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        return LUT[x.upper()] - 1, int(y) - 1

    def _to_str(self, x, y):
        LUT = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
        return LUT[x+1] + str(y+1)

    def get_disc_value(self, xy):
        x, y = self._to_num(xy)
        return self._gameboard[x][y]

    def _update_possibles(self, xy):
        self.taken.add(xy)
        if xy in self._possible:
            self._possible.remove(xy)
        x, y = self._to_num(xy)
        for dx, dy in [[1, 0], [1, 1], [0, 1], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]]:
            tx = x + dx
            ty = y + dy
            if self._on_board(tx, ty) and self._to_str(tx, ty) not in self.taken:
                self._possible.add(self._to_str(tx, ty))

    def _get_discs(self, xy, player):
        x, y = self._to_num(xy)
        discs_to_flip = []
        if self._gameboard[x][y] is not None:
            return discs_to_flip

        for dx, dy in [[1, 0], [1, 1], [0, 1], [-1, 1],
                       [-1, 0], [-1, -1], [0, -1], [1, -1]]:
            tx = x + dx
            ty = y + dy
            op_discs = []
            while self._on_board(tx, ty) and self._gameboard[tx][ty] is not None:
                disc = self._gameboard[tx][ty]
                if disc == player:
                    if op_discs:
                        discs_to_flip += op_discs
                    break
                else:
                    op_discs.append(self._to_str(tx, ty))

                tx += dx
                ty += dy

        return discs_to_flip

    def _update_moves(self):
        self.moves[1] = self._get_moves(1)
        self.moves[-1] = self._get_moves(-1)

    def _get_moves(self, player):
        moves = {}
        for cord in self._possible:
            discs = self._get_discs(cord, player)
            if discs:
                moves[cord] = discs
        return moves

    def _update_player(self):
        if self.moves[self.current_player * -1]:
            self.current_player *= -1
        elif not self.moves[self.current_player]:
            self.current_player = 0

    def apply_move(self, xy):
        discs = self.moves[self.current_player][xy]
        self._add_disc(xy)
        self._flip_discs(discs)
        self.score[self.current_player] += 1 + len(discs)
        self.score[self.current_player * -1] -= len(discs)
        self._update_moves()
        self._update_player()

    def _add_disc(self, xy):
        x, y = self._to_num(xy)
        self._update_possibles(xy)
        self._gameboard[x][y] = self.current_player

    def _flip_discs(self, discs):
        for disc in discs:
            x, y = self._to_num(disc)
            self._gameboard[x][y] = self.current_player

    def _on_board(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7
