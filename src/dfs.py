from algorithm import *
          
class Dfs(Algorithm):
    def __init__(self, cols, rows):
        super().__init__(cols, rows)
        self.visited = set()
        self.queue = deque()
        self.queue.append(self.start)
    def reset(self):
        self.reset_grid()
        self.visited = set()
        self.queue = deque()
        self.queue.append(self.start)
    def next_step(self):
        if len(self.queue) < 1:
            return False
        node = self.queue.pop()
        if self.cell(*node) == "end":
            self.end_found = True
            return True
        if node not in self.visited:
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
        return node, CELL_COLOR.get("visited"), "visited"
    def cell_content(self, x, y):
        return super().cell_content(x, y)