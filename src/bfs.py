from algorithm import *

class Bfs(Algorithm):
    def __init__(self, cols, rows):
        super().__init__(cols, rows)
        self.visited = set()
        self.queue = deque()
        self.queue.append(self.start)
    def cell_content(self, x, y):
        return self.cell(x,y)
    def next_step(self):
        if len(self.queue) < 1:
            return False
        node = self.queue.popleft()
        while len(self.queue) > 1 and self.cell(*node) not in ["empty", "end"]:
            node = self.queue.popleft()
        if node in self.visited:
            return False
        if self.cell(*node) == "end":
            self.end_found = True
            return True
        x,y = node
        if self.cell(x,y) == "empty":
            self.visited.add(node)
            self.grid[y][x] = "visited"
            self.update_cell(x,y, "visited")
        neighbours = self.get_neighbours(node)
        for n in neighbours:
            self.queue.append(n)
            if self.cell(*n) != "visited":
                self.parents[n] = node
        if self.cell(x,y) == "start":
            return node, CELL_COLOR.get("start"), "start"
        return node, CELL_COLOR.get("visited"), "visited"
            
    def reset(self):
        self.reset_grid()
        self.visited = set()
        self.queue = deque()
        self.queue.append(self.start)
   