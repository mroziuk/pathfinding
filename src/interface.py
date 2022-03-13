import tkinter as tk
from tkinter import ttk
import random
from colors import *
import pickle
import os
from algorithm import *
from astar import Astar
from dfs import Dfs
from bfs import Bfs
from dijkstra import Dijkstra
from greedy import Greedy
class Game(tk.Frame):
    """
    A class to visualise pathfinging algorithms
    
    Attributes
    ----------
    WIDTH : int
        width of displayed screen
    HEIGHT : int
        height of displayed screen
    cols : int
        number of columns in the grid
    rows : int
        number of rows in the grid
    dict_of_algs " dict[str, Algorithm]
        dictionary with names of algorithms and
        class implementing them, class must derive from
        abstarct class Algorithm
    algorithm : Algorithm
        currently selected algorithm for simulation
        
        
    Methods
    -------
    run( ) -> None
        start simulation and visualisation
        if found configuration file load data from it
        else calls place_start_end
        saves data to config file after exiting app
    place_start_end( ) -> None
        randomly place start and end node
    next_step( ) -> None
        performs one step of currently selected algorithm and update GUI
    run_till_finish( ) -> None
        perfoms steps of the algorithm until find end or gets stuck
    reconstruct_path( ) -> None
        gets path from angorithm and color cells on the path with
        color specified for path cells
    update_GUI( ) -> None
        update color and values in the displayed cells
    mouse_press_cell(event) -> None
        handles mouse being pressed
        if wall pressed, removes it
        if empty cell pressed puts wall
        if start or end pressed start moving them
    mouse_drag_cell(event) -> None
        handles mouse being dragged
        if dragged over wall and wall was first pressed, removes it
        if dragged over empty cell and wall was first pressed puts wall
        if start or end was pressed moves them
    mouse_release_cell(event) -> None
        handles mouse being released
        if start or end was pressed and there is empty space
        moves it from previous location
    """
    def __init__(self):
        # initialize main frame with main grid
        self.WIDTH = 800
        self.HEIGHT = 600
        self.cols = 20
        self.rows = 15
        self.scaleX = self.WIDTH // self.cols
        self.scaleY = self.HEIGHT // self.rows
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("pathfinding visualization")
        
        self.main_grid = tk.Frame(self, bg=BG_COLOR, bd=1, width=self.WIDTH, height=self.HEIGHT)
        self.main_grid.grid(padx=(0,200))
        self.end_cell_pressed = False
        self.start_cell_pressed = False
        self.empty_cell_pressed = False
        self.wall_cell_pressed = False
        # pathfinding variables
        self.move_step = False
        self.end_position = (-1,-1)
        self.start_position = (-1,-1)
        # algorithms
        self.end_found = False
        self.pathfinding_started = False
        
        self.algorithms_list = [
            "dfs",
            "bfs",
            "astar",
            "dijkstra",
            "greedy"
        ]
        self.dict_of_algs = {
            "dfs": Dfs,
            "bfs": Bfs,
            "astar": Astar,
            "dijkstra":Dijkstra,
            "greedy": Greedy
        }
        self.algorithm : Algorithm = Bfs(
            self.cols,
            self.rows
        )
    
    def run(self):
        """
        if 'config.dictionary' exist in app directory load data from it
        else initialize start and end position randomly
        """
        self.make_GUI()
        if os.path.isfile('config.dictionary'):
            with open('config.dictionary', 'rb') as config_dictionary_file:
                config_dictionary = pickle.load(config_dictionary_file)
                self.algorithm.load_data(config_dictionary)
                self.update_GUI()
        else:
            self.place_start_end()
        tk.mainloop()
        self.save_to_file()

    def save_to_file(self):
        config_dictionary = self.algorithm.get_data()
        with open('config.dictionary', 'wb') as config_dictionary_file:
            pickle.dump(config_dictionary, config_dictionary_file)
    
    def make_GUI(self):
        """initialize GUI with cells
            colors, bindings
        """
        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg = CELL_COLOR["empty"],
                    # bg = random.choice(list(CELL_COLOR.values())),
                    width=self.WIDTH/self.cols,
                    height=self.HEIGHT/self.rows
                )
                cell_frame.grid(row=i, column=j, padx=1, pady=1)
                cell_number = tk.Label(self.main_grid, bg=CELL_COLOR["empty"])
                cell_number.grid(row=i, column=j)
                cell_number.configure(font = MAIN_FONT)
                
                cell_detail = tk.Label(self.main_grid, bg=CELL_COLOR["empty"])
                cell_number.grid(row=i, column=j)
                cell_number.configure(font = MAIN_FONT)
                
                cell_frame.bind('<ButtonPress 1>', self.mouse_press_cell)
                cell_number.bind('<ButtonPress 1>', self.mouse_press_cell)
                cell_detail.bind('<ButtonPress 1>', self.mouse_press_cell)
                cell_frame.bind('<B1-Motion>', self.mouse_drag_cell)
                cell_number.bind('<B1-Motion>', self.mouse_drag_cell)
                cell_detail.bind('<B1-Motion>', self.mouse_drag_cell)
                cell_frame.bind('<ButtonRelease 1>', self.mouse_release_cell)
                cell_number.bind('<ButtonRelease 1>', self.mouse_release_cell)
                cell_detail.bind('<ButtonRelease 1>', self.mouse_release_cell)
                
                cell_data = {"frame":cell_frame, "number":cell_number, "detail":cell_detail}
                row.append(cell_data)
            self.cells.append(row)
            # next step button
            next_step_button = tk.Button(self, borderwidth=2, text="next step", width="20", command=self.next_step)
            next_step_button.place(relx=0.92, rely=0.1, anchor= "center")
            # run till end button
            run_till_finish_button = tk.Button(self, borderwidth=2, text="run", width="20", command=self.run_till_finish)
            run_till_finish_button.place(relx=0.92, rely=0.15, anchor= "center")
            # show path button
            show_path_button = tk.Button(self, borderwidth=2, text="show path", width="20", command=self.reconstruct_path)
            show_path_button.place(relx=0.92, rely=0.2, anchor= "center")
            # clear button
            clear_button = tk.Button(self, borderwidth=2, text="clear", width="20", command=self.clear_pathfinding)
            clear_button.place(relx=0.92, rely=0.25, anchor= "center")
            # choose an algorithm
            self.selected_algorithm_var = tk.StringVar()
            self.choose_algorithm_combobox = ttk.Combobox(self, values=self.algorithms_list,textvariable=self.selected_algorithm_var, state='readonly')
            self.choose_algorithm_combobox.bind('<<ComboboxSelected>>', self.algorithm_selected)
            self.selected_algorithm_var.set("bfs")
            self.choose_algorithm_combobox.place(relx=0.92, rely=0.3, anchor="center")

    def algorithm_selected(self, event):
        """select algorithm used"""
        # remember start and end position
        data = self.algorithm.get_data()
        self.choose_algorithm_combobox.selection_clear()
        self.algorithm = self.dict_of_algs.get(self.selected_algorithm_var.get())(self.cols, self.rows)
        self.algorithm.load_data(data)
        self.clear_pathfinding()
        
    def get_cell_cords(self, event):
        """return cordinates of clicked cell"""
        a, b = event.x_root - self.winfo_rootx(), event.y_root- self.winfo_rooty()
        x, y = self.main_grid.grid_location(a, b)
        return x, y
    
    def mouse_press_cell(self, event):
        """handle mouse click
            - start cliced
            - end clicked
            - wall clicked
            - empty cell clicked"""
        x, y = self.get_cell_cords(event)
        cell = self.algorithm.grid[y][x]
        if cell == "start":
            self.start_cell_pressed = True
            self.previous_start_cords = x,y
        elif cell == "end":
            self.end_cell_pressed = True
            self.previous_end_cords = x,y
        elif cell == "empty":
            self.algorithm.grid[y][x] = "wall"
            self.update_cell(x,y,"wall")
            self.wall_cell_pressed = True
        elif cell == "wall":
            self.algorithm.grid[y][x] = "empty"
            self.update_cell(x,y,"empty")
            self.empty_cell_pressed = True
        self.update_cell(x,y,cell)
        
    def mouse_drag_cell(self, event):
        """handle mouse drag"""
        x, y = self.get_cell_cords(event)
        cell = self.algorithm.grid[y][x]
        if self.wall_cell_pressed and cell == "empty":
            self.algorithm.grid[y][x] = "wall"
            self.update_cell(x,y,"wall")
        elif self.empty_cell_pressed and cell == "wall":
            self.algorithm.grid[y][x] = "empty"    
            self.update_cell(x,y,"empty")
                
    def mouse_release_cell(self, event):
        """hande mouse release"""
        self.wall_cell_pressed = False
        self.empty_cell_pressed = False
        x, y = self.get_cell_cords(event)
        cell = self.algorithm.grid[y][x]
        if self.start_cell_pressed and cell == "empty":
            self.algorithm.grid[y][x] = "start"
            x2, y2 = self.previous_start_cords
            self.algorithm.grid[y2][x2] = "empty"
            self.update_cell(x2,y2,cell)
            self.update_cell(x,y,"start")
            self.algorithm.start = (x,y)
        elif self.end_cell_pressed and cell == "empty":
            self.algorithm.grid[y][x] = "end"
            x2, y2 = self.previous_end_cords
            self.algorithm.grid[y2][x2] = "empty"
            self.update_cell(x2,y2,cell)
            self.update_cell(x,y,"end")
            self.algorithm.end = (x,y)    
        self.start_cell_pressed = False
        self.end_cell_pressed = False
        self.update_GUI()
    
    def place_start_end(self):
        """randomly place start and end node on the grid"""
        row = random.randint(0,self.rows-1)
        col = random.randint(0,self.cols-1)
        self.algorithm.grid[row][col] = "start"
        self.algorithm.start = (col, row)
        while(self.algorithm.grid[row][col] != "empty"):
            row = random.randint(0,self.rows-1)
            col = random.randint(0,self.cols-1)
        self.algorithm.grid[row][col] = "end"
        self.algorithm.end = (col, row)
        self.update_GUI()

    def clear_pathfinding(self):
        """reset internal data of current algotithm and update GUI"""
        self.algorithm.reset()
        self.update_GUI()
    def next_step(self):
        """perform one step of the algorithm and update GUI
        if pathfinding was not started resets internal data
        of current algorithm"""
        if not self.pathfinding_started:
            self.pathfinding_started = True
            self.algorithm.reset()
        res = self.algorithm.next_step()
        if res not in [True, False]:
            node, color, value = res
            self.update_cell(*node, value)
            self.set_cell_color(*node, color)
        return res
    def run_till_finish(self):
        """perform steps of algorithm until end found or gets stuck"""
        while self.next_step() not in [True, False]:
            pass
    def reconstruct_path(self):
        """
        gets path from angorithm and color cells on the path with
        color specified for path cells
        does nothing if path wasnt found
        """ 
        for x,y in self.algorithm.reconstruct_path():
            if self.algorithm.cell_content(x,y) not in ["start", "end"]:
                self.set_cell_color(x,y,CELL_COLOR["path"])
        self.update_cell(*self.algorithm.start, "start")
        self.update_cell(*self.algorithm.end, "end")
        
    def set_cell_color(self, x, y, color):
        self.cells[y][x]["number"].configure(bg=color)
        self.cells[y][x]["frame"].configure(bg=color)
    def update_cell(self, x, y, value):
        """set cell GUI at x , y to value and update"""
        # self.algorithm.update_cell(x,y,value)
        if self.algorithm.cell_content(x,y) in ["start", "end"]:
            return
        self.cells[y][x]["number"].configure(bg=CELL_COLOR.get(value), text=(lambda x: "" if x == "empty" else x)(value))
        self.cells[y][x]["frame"].configure(bg=CELL_COLOR.get(value))
        self.update_idletasks()
    
    def update_GUI(self):
        """update all cells form data matrix"""
        for i in range(self.rows):
            for j in range(self.cols):
                cell_value = self.algorithm.grid[i][j]
                if cell_value == "empty":
                    self.cells[i][j]["number"].configure(bg=CELL_COLOR.get(cell_value), text="")
                else:
                    self.cells[i][j]["number"].configure(bg=CELL_COLOR.get(cell_value), text=str(cell_value))
                self.cells[i][j]["frame"].configure(bg=CELL_COLOR.get(cell_value))
        self.update_idletasks()

def main():
    Game().run()
if __name__ == "__main__":
    main()