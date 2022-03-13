from algorithm import *
class Dijkstra(Algorithm):
    """
    A class represrenting Dijkstra pathfinding algorithm
    
    Attributes
    ----------
    visited : list
        list of already visited nodes
    weights : defaultdict
        dictionary of nodes and cost getting from start to node
    heap_queue : list
        list representation of priority queue for nodes to visit
    Methods
    -------
    reset( ) -> None
        restores default values for internal data
    next_step( ) -> (True,False, None)
        perform one step of pathfinding algorithm
    cell_content(x : int, y : int) -> str
        return values of g and h of a node at position x, y
    """
    def __init__(self, cols, rows):
        super().__init__(cols, rows)
        self.visited = []
        self.weights = dd(lambda: math.inf)
        self.heap_queue = []
        self.weights[self.start] = 0
        hq.heappush(self.heap_queue, (0,self.start))
    def reset(self):
        self.reset_grid()
        self.visited = set()
        self.weights = dd(lambda: math.inf)
        self.heap_queue = []
        self.weights[self.start] = 0
        hq.heappush(self.heap_queue, (0,self.start))
    def next_step(self):
        if len(self.heap_queue) < 1:
            return False
        g, u = hq.heappop(self.heap_queue)
        if self.cell(*u) == "end":
            self.end_found = True
            return True
        self.visited.add(u)
        self.update_cell(*u, "visited")
        for v in self.get_neighbours(u):
            if v not in self.visited:
                f = g + 1
                if f < self.weights[v]:
                    self.weights[v] = f
                    self.parents[v] = u
                    hq.heappush(self.heap_queue, (f, v))
        if self.cell(*u) == "start":
            return u, CELL_COLOR.get("start"), "start"
        return u, CELL_COLOR.get("visited"), str(g)
    def cell_content(self, x, y):
        return self.cell(x,y)
 