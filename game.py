from tkinter import Tk, Canvas
from othelloboard import OthelloBoard
from ai import Ai


class OthelloGui(object):

    def __init__(self, root):
        self.root = root
        self.screen = Canvas(root, width=500, height=500,
                             background="#008000")
        self.board = OthelloBoard()
        self.player_id = 0
        self._setup()

    def _reset_game(self):
        self.board.reset_board()
        self._setup()

    def _player_turn(self, xy):
        self.board.apply_move(xy)
        self._update_graphics()

    def _ai_turn(self):
        self.board.apply_move(self.ai.time_limit_move())
        self._update_graphics()

    def _update_graphics(self):
        self.screen.delete("graphics")
        player = self.board.current_player
        color = {-1: "#ffffff", 1: "#111111", None: "#008000"}
        shadow = {-1: "#aaaaaa", 1: "#000000", None: "#008000"}

        for x in range(8):
            for y in range(8):
                disc = self.board.get_disc_value(chr(ord('A') + x) + str(y+1))
                self.screen.create_oval(54+50*x, 54+50*y, 96+50*x, 96+50*y,
                                        tags="graphics",
                                        fill=shadow[disc],
                                        outline=shadow[disc])
                self.screen.create_oval(54+50*x, 52+50*y, 96+50*x, 94+50*y,
                                        tags="graphics",
                                        fill=color[disc],
                                        outline=color[disc])
        if player == self.player_id:
            for x, y in self.board.moves[player]:
                x = ord(x) - ord('A')
                y = int(y) - 1
                self.screen.create_oval(70+50*x, 70+50*y, 80+50*x, 80+50*y,
                                        tags="graphics",
                                        fill='#ff3300',
                                        outline='#ff3300')

        self.screen.create_text(110, 475, tags="graphics",
                                font=("Consolas", 40),
                                fill="white",
                                text=self.board.score[-1])
        self.screen.create_text(390, 475, tags="graphics",
                                font=("Consolas", 40),
                                fill="black",
                                text=self.board.score[1])

        if player == 0:
            self.screen.create_text(250, 25, tags="graphics",
                                    font=("Consolas", 40),
                                    fill="black",
                                    text="GAME OVER")

        else:
            self.screen.create_oval(230, 5, 270, 45,
                                    tags="graphics",
                                    fill=color[player],
                                    outline=color[player])
            self.screen.create_rectangle(175, 22, 200, 28,
                                         tags="graphics",
                                         fill=color[player],
                                         outline=color[player])
            self.screen.create_rectangle(300, 22, 325, 28,
                                         tags="graphics",
                                         fill=color[player],
                                         outline=color[player])

            self.screen.create_polygon(300, 15, 300, 35, 280, 25,
                                       tags="graphics",
                                       fill=color[player],
                                       outline=color[player])
            self.screen.create_polygon(200, 15, 200, 35, 220, 25,
                                       tags="graphics",
                                       fill=color[player],
                                       outline=color[player])

    def _draw_gameboard(self):
        # background
        self.screen.create_rectangle(50, 50, 450, 450,
                                     tags="gameboard",
                                     outline="#000")
        for i in range(7):
            lineShift = 50+50*(i+1)
            self.screen.create_line(50, lineShift, 450, lineShift,
                                    tags="gameboard",
                                    fill="#000")
            self.screen.create_line(lineShift, 50, lineShift, 450,
                                    tags="gameboard",
                                    fill="#000")

        # Restart button
        self.screen.create_rectangle(0, 0, 50, 50,
                                     tags="gameboard",
                                     fill="#000088",
                                     outline="#000088")
        # Arrow
        self.screen.create_arc(5, 5, 45, 45,
                               tags="gameboard",
                               fill="#000088",
                               width="2",
                               style="arc",
                               outline="white",
                               extent=300)
        self.screen.create_polygon(33, 38, 36, 45, 40, 39,
                                   tags="gameboard",
                                   fill="white",
                                   outline="white")

        # Quit button
        self.screen.create_rectangle(450, 0, 500, 50,
                                     tags="gameboard",
                                     fill="#880000",
                                     outline="#880000")
        # "X"
        self.screen.create_line(455, 5, 495, 45,
                                tags="gameboard",
                                fill="white",
                                width="3")
        self.screen.create_line(495, 5, 455, 45,
                                tags="gameboard",
                                fill="white",
                                width="3")

    def _draw_player_select(self):
        self.screen.delete("graphics")
        self.screen.delete("gameboard")
        self.screen.create_rectangle(50, 100, 450, 200,
                                     tags="graphics",
                                     fill="black",
                                     outline="white")
        self.screen.create_text(250, 150,
                                tags="graphics",
                                font=("Consolas", 75),
                                fill="white",
                                text="BLACK")
        self.screen.create_rectangle(50, 300, 450, 400,
                                     tags="graphics",
                                     fill="white",
                                     outline="black")
        self.screen.create_text(250, 350,
                                tags="graphics",
                                font=("Consolas", 75),
                                fill="black",
                                text="WHITE")

    def _clickHandle(self, event):
        if self._game_started:
            if event.x >= 450 and event.y <= 50:
                self.root.destroy()
            elif event.x <= 50 and event.y <= 50:
                self._reset_game()
            elif self.board.current_player == self.player_id:
                x = chr(ord('A') + int((event.x-50)/50))
                y = str(int((event.y-50)/50) + 1)
                xy = x + y
                if xy in self.board.moves[self.player_id]:
                    self._player_turn(xy)
        else:
            if event.x >= 50 and event.x <= 450 and event.y >= 100 and event.y <= 200:
                self.player_id = 1
                self.ai = Ai(self.board, -1, 4)
                self._start_game()
            elif event.x >= 50 and event.x <= 450 and event.y >= 300 and event.y <= 400:
                self.player_id = -1
                self.ai = Ai(self.board, 1, 4)
                self._start_game()

    def _game_loop(self):
        if self._game_started:
            if self.board.current_player == self.player_id * -1:
                self._ai_turn()
            elif self.board.current_player == 0:
                pass
            self.root.after(100, self._game_loop)

    def _setup(self):
        self.screen.pack()
        self._game_started = False
        self.screen.bind("<Button-1>", self._clickHandle)
        self.root.wm_title("Othello")
        self._draw_player_select()

    def _start_game(self):
        self._game_started = True
        self._draw_gameboard()
        self._update_graphics()
        self._game_loop()


if __name__ == "__main__":
    root = Tk()
    OthelloGui(root)
    root.mainloop()
