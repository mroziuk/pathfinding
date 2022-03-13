from abc import ABC, abstractmethod
from collections import deque, defaultdict as dd
from colors import *
import heapq as hq
import math


class Algorithm(ABC):
    """
    An abstract class to represent pathfinding algorithms
    
    ...
    
    Attributes
    ----------
    cols : int
        numbers of column in the grid
    rows : int
        number of rows in the grid
    grid : list of lost of str
        two dimentional grid for algorithm, could be
        "empty", "wall", "visited", "start", "end"
    end: tuple(int, int)
        position of the end node
    start: tuple(int, int)
        position of the start node
    parents:
        dictionary of parents of visited nodes
    
    Methods
    -------
    next_step( ) -> (None, True, False)
        perform one step of algorithm and update the grid
        return True if end was found
        return False if could not found end (is stuck)
        else return tuple(tuple(int, int), str, str)
        position of updated node, color, content
    cell_content(x : int, y : int) -> str
        return value of grid at position x, y
    reset( ) -> None
        resets all internal data for algorithm, resets grid,
        don't reset walls, start and end position
    reconstruct_path( ) -> list of (int, int)
        return path from start to end node finded by algorithm
        return None if path not founded
    get_data( ) -> dict[str, Any]
        return dictionary with start, end and walls positions
            "start": tuple(int, int),
            "end": tuple(int, int),
            "walls": list(tuple(int,int))
    load_data(data : dict[str, Any]) -> None
        loads walls, start and and from dictionary
    update_cell(x : int, y : int, value : str) - > None
        set grid at position x, y to value
    """ 
    @abstractmethod
    def __init__(self,cols, rows):
        """
        Parameters
        ----------
        cols : int
            numbers of column in the grid
        rows : int
            number of rows in the grid
        """
        self.cols = cols
        self.rows = rows
        self.grid = [["empty"] * cols for _ in range(rows) ]
        self.start = None
        self.end = None
        self.parents = dd()
        self.directions4 = [(0,1),(0,-1),(1,0),(-1,0)]
        self.directions8 = [(0,1),(0,-1),(1,0),(-1,0),(-1,-1),(1,1),(1,-1),(-1,1)]
        self.directions = self.directions4
        self.end_found = False
        super().__init__()
    def set_directions(self, moore):
        if moore:
            self.directions = self.directions8
        else:
            self.directions = self.directions4
    @abstractmethod
    def next_step(self):
        pass
    @abstractmethod
    def cell_content(self, x, y):
        pass
    @abstractmethod
    def reset(self):
        pass
    def set_start(self,node):
        self.start = node
        x,y = node
        self.grid[y][x] = "start"
    def set_end(self,node):
        self.end = node
        x,y = node
        self.grid[y][x] = "end"
    def cell(self, x, y):
        return self.grid[y][x]
    def get_neighbours(self, node):
        """return nodes if four directions
            N, E, S, W
        """    
        neighbours = []
        x, y = node
        for a,b in self.directions:
            if ((x + a <self. cols and x + a >= 0) and
                (y + b < self.rows and y + b >= 0) and
                (self.grid[y+b][x+a] != "wall")):
                neighbours.append((a+x, b+y))
        return neighbours
    def reconstruct_path(self):
        path = []
        if not self.end_found:
            return path
        node = self.end
        while node != self.start:
            path.append(node)
            self.update_cell(*node,"path")
            node = self.parents[node]
        self.update_cell(*self.end,"end")
        return path
    def update_cell(self, x, y, value):
        self.grid[y][x] = value
    def reset_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.grid[i][j]
                self.grid[i][j] = cell if cell in ["wall", "start", "end"] else "empty"
    def get_data(self):
        walls = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == "wall":
                    walls.append((j,i))
        return {
            "walls": walls,
            "start": self.start,
            "end": self.end
        }
    def load_data(self, data):
        self.__init__(self.cols, self.rows)
        self.set_start(data["start"])
        self.set_end(data["end"])
        for x,y in data["walls"]:
            self.grid[y][x] = "wall"