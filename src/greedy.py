from algorithm import *

class Greedy(Algorithm):
    """
    A class representing Greedy Best First Search pathfinding algorithm
    
    Best-first search is a class of search algorithms,
    which explore a graph by expanding the most promising node
    chosen according to heuristic
    """
    def __init__(self, cols, rows):
        super().__init__(cols, rows)
        self.open = []
        self.closed = set()
        self.g = dd(lambda: 0)
        self.f = dd(lambda: 0)
        self.g[self.start] = 0
        self.open.append(self.start)
    def reset(self):
        """
        reset values in the grid except walls, start, end node
        
        clears grid of visited and path nodes,
        clears g, f, closed sets and open list
        """
        self.reset_grid()
        self.open = []
        self.closed = set()
        self.g = dd(lambda: 0)
        self.f = dd(lambda: 0)
        self.g[self.start] = 0
        self.open.append(self.start)
    def next_step(self):
        """
        perform one step of Greedy Bfs algorithm
        
        if cant find end return False
        if found end in this step return True
        else (x,y), color, content
        
        find node with lowest h value in the open list
        add this node to closed set and check if it is end
        find neighbours of current node and if neighbour is
        already visited check if it could have lower g value
        if so update g value and set current as parent of neighbour
        else add neighbour on open list
        
        """
        if len(self.open) <= 0:
            return False
        current_node = self.open[0]
        current_index = 0
        for index, item in enumerate(self.open):
            if self.f[item] < self.f[current_node]:
                current_node = item
                current_index = index
        # pop current, add to closed
        self.open.pop(current_index)
        self.closed.add(current_node)
        if self.cell(*current_node) == "end":
            self.end_found = True
            return True
        ix, iy = current_node
        if self.grid[iy][ix] == "empty":
            self.grid[iy][ix] = "visited"
        for v in self.get_neighbours(current_node):
            if v not in self.closed:
                # self.g[v] = self.g[current_node] + 1
                self.f[v] = self.h(v)
                for open_node in self.open:
                    if v == open_node and self.g[v] > self.g[open_node]:
                        continue
                self.parents[v] = current_node
                if v not in self.open:
                    self.open.append(v)
        return current_node, CELL_COLOR.get(self.grid[iy][ix]), f"{self.h(current_node)}"           
    def h(self, node):
        """
        return heuristic (estimated) distance from the current node to the end node
        
        return manhattan (sum of horizontal distance and vertical distance)
        distance from node to end
        
        Parameters
        ----------
        node : tuple(int, int)
            node on the grid
        
        """
        x1, y1 = node
        x2, y2 = self.end
        a = x1 - x2
        b = y1 - y2
        return abs(a) + abs(b)
    def cell_content(self, x, y):
        """
        return value of the grid at position x, y
        """
        # return f"{self.g[(x,y)]}, {self.h[(x,y)]}"
        return self.cell(x,y)