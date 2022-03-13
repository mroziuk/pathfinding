from ..src import interface
from ..src import data
import unittest


class TestPythfinding(unittest.TestCase):
    def setUp(self):
        self.Game = interface.Game()
    def tearDown(self):
        data.reset()
    def test_get_neighbours_with_no_walls(self):
        self.assertEqual([(0,1),(1,0)], data.get_neighbours((0,0)))
        self.assertEqual(set([(0,1),(1,0),(2,1),(1,2)]), set(data.get_neighbours((1,1))))
    def test_get_neighbours_with_walls(self):
        data.matrix[0][1] = "wall"
        expected = set([(0,1)])
        actual = set(data.get_neighbours((0,0)))
        self.assertEqual(expected,actual)
    def test_get_cell(self):
        data.matrix[3][4] = "wall"
        self.assertEqual(
            self.Game.cell(4,3),
            "wall"
        )
        data.matrix[3][4] = "visited"
        self.assertEqual(
            self.Game.cell(4,3),
            "visited"
        )
    def test_clear_matrix(self):
        data.matrix[0][0] = "visited"
        self.assertEqual(data.matrix[0][0], "visited")
        data.clear_matrix()
        self.assertEqual(data.matrix[0][0], "empty")
    def test_clear_matrix_dont_clear_walls(self):
        data.matrix[0][0] = "wall"
        self.assertEqual(data.matrix[0][0], "wall")
        data.clear_matrix()
        self.assertEqual(data.matrix[0][0], "wall")
if __name__ == '__main__':
    unittest.main()