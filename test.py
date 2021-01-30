import unittest
import numpy as np

from utils import (
    RotationsFromPositionA,
    RotationsFromPositionB,
    RotationsFromPositionC,
    Piece,
    Cell,
    Cube,
    NotAvailableRotations
)


class TestCube(unittest.TestCase):

    def setUp(self):
        self.rotations_from_A = RotationsFromPositionA()
        self.rotations_from_B = RotationsFromPositionB()
        self.rotations_from_C = RotationsFromPositionC()

        self.cube = Cube(
            [],
            self.rotations_from_A,
            self.rotations_from_B,
            self.rotations_from_C,
            None
        )

    def test_get_cell_rotations_from_page_0(self):
        """ Test some cells with not available rotations. """
        cells = [
            Cell(0, 0, 0),
            Cell(0, 0, 1), Cell(0, 0, 2),
            Cell(0, 1, 2), Cell(0, 2, 2)
        ]
        for cell in cells:
            self.assertRaises(
                NotAvailableRotations,
                self.cube.get_cell_rotations,
                cell
            )

        cell = Cell(0, 1, 0)
        rotations = self.cube.get_cell_rotations(cell)
        self.assertTrue(
            np.array_equal(rotations, self.rotations_from_A.elements)
        )

    def test_place_piece_1(self):
        """ Places a piece with the first rotation from A in first
            cube cell.
        """
        piece = Piece("1", "")
        piece.rotation = self.rotations_from_A.elements[0]
        cell = self.cube.cells[0]
        placed = self.cube.place_piece(piece, cell)
        self.assertTrue(placed)


class TestPieceRotations(unittest.TestCase):

    def test_rotations_from_position_A(self):
        """ Rotations from position A """
        rotations_list = RotationsFromPositionA()

        self.assertTrue(len(rotations_list.elements) == 4)

    def test_rotations_from_position_B(self):
        """ Rotations from position B """
        rotations_list = RotationsFromPositionB()

        self.assertTrue(len(rotations_list.elements) == 4)

    def test_rotations_from_position_C(self):
        """ Rotations from position C """
        rotations_list = RotationsFromPositionC()

        self.assertTrue(len(rotations_list.elements) == 4)


if __name__ == '__main__':
    unittest.main()
