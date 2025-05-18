import tkinter as tk
from gol import GOL
from brush import BaseBrush

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HIGHT = 20


class GolGUI:
    def __init__(self, gol: GOL):
        self.game = gol
        self.root = tk.Tk()
        self.root.title("Game of Life")
        button_frame = tk.Frame(self.root)
        button_frame.pack(anchor=tk.CENTER, pady=0)
            # felső gombok - base, gilder, blinker, pulsar
        self.base_button = tk.Button(button_frame,text="Base",command = None)
        self.gilder_button = tk.Button(button_frame,text="Gilder",command=self.gilder)
        self.blinker_button = tk.Button(button_frame,text="Blinker",command=self.blinker)
        self.pulsar_button = tk.Button(button_frame,text="Pulsar",command=self.pulsar)
        self.base_button.pack(side=tk.LEFT)
        self.gilder_button.pack(side=tk.LEFT)
        self.blinker_button.pack(side=tk.LEFT)
        self.pulsar_button.pack(side=tk.LEFT)
            #
        self.brush = BaseBrush()
        self.canvas = tk.Canvas(self.root,
                                width=GRID_WIDTH * CELL_SIZE, 
                                height=GRID_HIGHT * CELL_SIZE, 
                                bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<Button-3>", self.toggle_barricade)
        self.draw_grid()
            # alsó gombok - start, step
        button_frame = tk.Frame(self.root)
        button_frame.pack(anchor=tk.CENTER, pady=0)
        self.start_button = tk.Button(button_frame,text="Start",command=self.toggle_running)
        self.step_button = tk.Button(button_frame,text="Step",command=self.step)
        self.clear_button = tk.Button(button_frame,text="Clear",command=self.clear)
        self.start_button.pack(side=tk.LEFT)
        self.step_button.pack(side=tk.LEFT)
        self.clear_button.pack(side=tk.LEFT)
            #  statisztikák - alive, dead, generations
        self.stats_label = tk.Label(self.root, text="Generations: 0")
        self.stats_label.pack(pady=10) 
            # 
        self.is_running = False
        self.root.mainloop()

    def toggle_running(self):
        self.is_running = not self.is_running
        self.start_button.config(text="Pause" if self.is_running else "Start")
        if self.is_running:
            self.run()
    


    def run(self):
        if self.is_running:
            self.step()
            self.root.after(500,self.run)
    
    def step(self):
        self.game.next_state()
        self.draw_grid()
        self.update_statistics()
    
    def clear(self):
        self.game.board = [[0 for _ in range(self.game.cols)] for _ in range(self.game.rows)]
        self.game.generations = 0
        self.draw_grid()
        self.update_statistics()
    
    def update_statistics(self):
        alive, dead = self.game.get_statistics()
        stats_text = f"Generations: {self.game.generations}, Alive: {alive}, Dead: {dead}"
        self.stats_label.config(text=stats_text)

    def gilder(self):
        pattern = [
            (0, 1),
            (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        
        base_row, base_col = 5, 5
        for dr, dc in pattern:
            row = base_row + dr
            col = base_col + dc
            if 0 <= row < self.game.rows and 0 <= col < self.game.cols:
                self.game.board[row][col] = 1
        self.draw_grid()
        self.update_statistics()

    def blinker(self):
        pattern = [
            (0, 0),
            (1, 0),
            (2, 0), 
        ]
        
        base_row, base_col = 8, 10
        for dr, dc in pattern:
            row = base_row + dr
            col = base_col + dc
            if 0 <= row < self.game.rows and 0 <= col < self.game.cols:
                self.game.board[row][col] = 1
        self.draw_grid()
        self.update_statistics()

    def pulsar(self):
        pattern = [
           (2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
            (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
            (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
            (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12),
            (4, 2), (5, 2), (6, 2), (10, 2), (11, 2), (12, 2),
            (4, 7), (5, 7), (6, 7), (10, 7), (11, 7), (12, 7),
            (4, 9), (5, 9), (6, 9), (10, 9), (11, 9), (12, 9),
            (4, 14), (5, 14), (6, 14), (10, 14), (11, 14), (12, 14)
        ]

        base_row, base_col = 2, 2
        for dr, dc in pattern:
            row = base_row + dr
            col = base_col + dc
            if 0 <= row < self.game.rows and 0 <= col < self.game.cols:
                self.game.board[row][col] = 1
        self.draw_grid()
        self.update_statistics()

    def toggle_cell(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.brush.apply(gol,row,col)
        self.draw_grid()

    def toggle_barricade(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.game.set_barricade(row,col)
        self.draw_grid()
        
    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if self.game.board[r][c] == 1:
                    colour = "black"
                elif self.game.board[r][c] == -1:
                    colour = "red"
                else:
                    colour = "white"

                self.canvas.create_rectangle(
                    c*CELL_SIZE,
                    r*CELL_SIZE,
                    (c+1)*CELL_SIZE,
                    (r+1)*CELL_SIZE,
                    fill=colour,
                    outline="gray"
                )



if __name__ == "__main__":
    gol = GOL(GRID_WIDTH, GRID_HIGHT)
    GolGUI(gol)