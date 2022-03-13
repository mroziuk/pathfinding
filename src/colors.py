from collections import defaultdict as dd

BG_COLOR = "#263d42"

CELL_COLOR = dd(lambda: "#d1a11d")
CELL_COLOR["wall"] = "#515151"
CELL_COLOR["empty"] = "#121212"
CELL_COLOR["visited"] = "#d1a11d"
CELL_COLOR["path"] = "#34a825"
CELL_COLOR["start"] = "#a82585"
CELL_COLOR["end"] = "#a8254c"
CELL_COLOR["red"] = "red"

MAIN_FONT = ("Verdana", 6)