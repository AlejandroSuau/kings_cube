import numpy as np
import random
import matplotlib.pyplot as plt

from copy import deepcopy
from mpl_toolkits.mplot3d import axes3d


class WoodColors:
    WHITE = "#FFF8DD"
    DARK_BROWN = "#563312"
    RED = "#80230B"
    ORANGE = "#B16C20"
    LIGHT_BROWN = "#674433"


class Rotations:
    """
        Attributes:
            STARTING_ROTATION:
            elements: a list containing rotation np arrays.
    """
    STARTING_ROTATION = np.array([])

    def __init__(self):
        self.elements = [self.STARTING_ROTATION]
        self._compute_rotations()

    def _compute_rotations(self):
        pass


class RotationsFromPositionA(Rotations):
    STARTING_ROTATION = np.array([
        [[0, 0], [0, 0]],
        [[1, 0], [1, 1]]
    ])

    def _compute_rotations(self):
        rotation = self.STARTING_ROTATION
        for i in range(3):
            rotation = np.array([rotation[0], np.rot90(rotation[1])])
            self.elements.append(rotation)


class RotationsFromPositionB(Rotations):
    STARTING_ROTATION = np.array([
        [[0, 0], [1, 0]],
        [[1, 0], [1, 0]]
    ])

    def _compute_rotations(self):
        piece = self.STARTING_ROTATION
        for i in range(3):
            piece = np.rot90(piece)
            self.elements.append(piece)


class RotationsFromPositionC(Rotations):
    STARTING_ROTATION = np.array([
        [[0, 0], [1, 0]],
        [[0, 0], [1, 1]]
    ])

    def _compute_rotations(self):
        piece = self.STARTING_ROTATION
        for i in range(3):
            if i % 2 == 0:
                flip_axis = 0
            else:
                flip_axis = 2
            piece = np.flip(piece, flip_axis)
            self.elements.append(piece)


class Piece:
    """
        Attributes:
            PARTS_NUMBER: the number of cubes which forms a piece.

            name: string which identifies Piece.
            color: string with hex code which references a color.
            rotation: 3-d numpy array which the current rotation.
    """
    PARTS_NUMBER = 3

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color
        self.rotation = None

    def __str__(self):
        return self.name


class PieceContiguousCircles(Piece):
    pass


class PieceDisjointCircles(Piece):
    pass


class Cell:
    """
    """

    def __init__(self, page, row, col):
        self.page = page
        self.row = row
        self.col = col


class PieceHasNoRotation(Exception):
    pass


class NotAvailableRotations(Exception):
    pass


class CubeChart:
    """
        Attributes:
            PAUSE_SECONDS: a float number with the number of seconds that will
                stop after place a piece.
            fig: plf figure object.
            ax: axis element for plt object.

    """
    PAUSE_SECONDS = 0.5

    def __init__(self):
        self.fig = plt.figure()
        self.fig.suptitle('Kings Cube', fontsize=14, fontweight='bold')
        self.ax = self.fig.gca(projection='3d')
        self._set_lims_3d()

        plt.ion()

    def clear(self):
        """ """
        self.ax.clear()
        self._set_lims_3d()

    def _set_lims_3d(self):
        """ """
        self.ax.set_xlim3d(0, 3)
        self.ax.set_ylim3d(0, 3)
        self.ax.set_zlim3d(3, 0)

    def draw_structure(self, structure, show_steps=False):
        """ Draw current cube's structure.

            Args:
                structure: 3-d np array of Pieces instances.
                show_steps: a boolean which enables to show step placements.
        """
        drew_pieces_names = []
        page = 2
        while page >= 0:
            row = 2
            while row >= 0:
                for col in range(3):
                    cell_item = structure[page][row][col]
                    if (isinstance(cell_item, Piece)
                            and cell_item.name not in drew_pieces_names):
                        self.draw_piece_parts(structure, cell_item)
                        drew_pieces_names.append(cell_item.name)

                    if show_steps:
                        plt.pause(self.PAUSE_SECONDS)
                row -= 1
            page -= 1

        plt.pause(self.PAUSE_SECONDS)

    def draw_piece_parts(self, structure: np.array, piece: Piece):
        """ Search all piece parts from bottom and draw it.

            Args:
                structure:
                piece:
        """
        drew_parts = 0
        page = 2
        while page >= 0:
            row = 2
            while row >= 0:
                for col in range(3):
                    cell_item = structure[page][row][col]
                    if (isinstance(cell_item, Piece) and
                            cell_item.name == piece.name):
                        self.draw_cube(page, row, col, piece.color)
                        drew_parts += 1

                    if drew_parts == Piece.PARTS_NUMBER:
                        return
                row -= 1
            page -= 1

    def draw_cube(self, page: int, row: int, col: int, color):
        """ Draw a cube (part of a piece) build by its 6 faces. """
        r = [0, 1]
        X, Y = np.meshgrid(r, r)
        # top face
        self.ax.plot_surface(col + X, page + Y, np.atleast_2d(row + 1),
                             alpha=1, color=color, edgecolors='black')
        # bottom face
        self.ax.plot_surface(col + X, page + Y, np.atleast_2d(row + 0),
                             alpha=1, color=color, edgecolors='black')
        # front face
        self.ax.plot_surface(col + X, page + 0, np.atleast_2d(row + Y),
                             alpha=1, color=color, edgecolors='black')
        # back face
        self.ax.plot_surface(col + X, page + 1, np.atleast_2d(row + Y),
                             alpha=1, color=color, edgecolors='black')
        # left face
        self.ax.plot_surface(col + 0, page + X, np.atleast_2d(row + Y),
                             alpha=1, color=color, edgecolors='black')
        # right face
        self.ax.plot_surface(col + 1, page + X, np.atleast_2d(row + Y),
                             alpha=1, color=color, edgecolors='black')


class Cube:
    """
        Attributes:
            DIMENSIONS: int which indicates the cube dimensions.

            structure: 3-d np matrix with the current structure.
            cells: a list containing all available cells to ease iteration.
            pieces: a list containing all the pieces.
            rotations_from_A:
            rotations_from_B:
            rotations_from_C:
            rotations_all:
            cube_chart:
    """
    DIMENSIONS = 3

    def __init__(
            self, pieces: list[Piece],
            rotations_from_a: RotationsFromPositionA,
            rotations_from_b: RotationsFromPositionB,
            rotations_from_c: RotationsFromPositionC,
            cube_chart: CubeChart
    ):
        self.pieces = pieces
        self.rotations_from_A = rotations_from_a
        self.rotations_from_B = rotations_from_b
        self.rotations_from_C = rotations_from_c
        self.rotations_all = np.concatenate(
            (self.rotations_from_A.elements,
             self.rotations_from_B.elements,
             self.rotations_from_C.elements)
        )
        self.cube_chart = cube_chart

        self.current_solutions = 0
        self.structure = np.zeros(
            (self.DIMENSIONS, self.DIMENSIONS, self.DIMENSIONS), dtype=Piece
        )
        self._setup_cells_list()

    def _setup_cells_list(self):
        """ Creates a list of cells which allows to iterate over them easy. """
        self.cells = []
        page = 2
        while page >= 0:
            row = 2
            while row >= 0:
                col = 0
                while col <= 2:
                    self.cells.append(Cell(page, row, col))
                    col += 1
                row -= 1
            page -= 1

    def get_cell_rotations(self, cell: Cell):
        """
            Args:
                cell: a Cell instance.

            Returns:
                a list with all rotations available for a position.

            Raises:
                NotAvailableRotationsForThisPosition: if there aren't
                    a rotation available to fill in this position.
        """
        if cell.page == 0:
            if cell.row == 0 or cell.col == self.DIMENSIONS - 1:
                raise NotAvailableRotations
            else:
                return self.rotations_from_A.elements
        else:
            if cell.col == self.DIMENSIONS - 1:
                if cell.row == 0:
                    raise NotAvailableRotations
                else:
                    return self.rotations_from_B.elements
            else:
                if cell.row == 0:
                    return self.rotations_from_C.elements
                else:
                    return self.rotations_all

    def solve(self, randomize_pieces=False, randomize_cells=False):
        """
            Args:
                randomize_pieces:
                randomize_cells:
        """
        if randomize_pieces:
            random.shuffle(self.pieces)

        if randomize_cells:
            random.shuffle(self.cells)

        return self.find_solution(self.pieces, self.cells)

    def find_solution(self, pieces: list[Piece], cells: list[Cell]):
        """
            Args:
                pieces:
                cells:
        """
        for i, piece in enumerate(pieces):
            for j, cell in enumerate(cells):
                try:
                    rotations = self.get_cell_rotations(cell)
                except NotAvailableRotations:
                    continue

                for rotation in rotations:
                    structure_copied = self.structure.copy()
                    piece.rotation = rotation
                    placed = self.place_piece(piece, cell)
                    if placed:
                        # self.cube_chart.draw_structure(self.structure)

                        pieces_copied = deepcopy(pieces)
                        pieces_copied.pop(i)
                        cells_copied = deepcopy(cells)
                        cells_copied.pop(j)
                        if len(pieces_copied) == 0:
                            return True
                        else:
                            if self.find_solution(pieces_copied, cells_copied):
                                return True

                        self.structure = structure_copied

                        # self.cube_chart.clear()
                        # self.cube_chart.draw_structure(self.structure)

        return False

    def place_piece(self, piece: Piece, starting_cell: Cell):
        """
            Args:
                piece:
                starting_cell:

            Returns:
                True if the piece could be placed. False otherwise.

            Raises:
                PieceHasNoRotation: is piece has not defined rotation.
        """
        if piece.rotation is None:
            raise PieceHasNoRotation

        z, y, x = np.where(piece.rotation == 1)

        piece_parts_new_cells = []
        for i in range(piece.PARTS_NUMBER):
            new_cell = Cell(
                page=starting_cell.page + z[i] - 1,
                row=starting_cell.row + y[i] - 1,
                col=starting_cell.col + x[i]
            )
            if self.is_free(new_cell):
                piece_parts_new_cells.append(new_cell)

        if len(piece_parts_new_cells) == piece.PARTS_NUMBER:
            for cell in piece_parts_new_cells:
                self.structure[cell.page][cell.row][cell.col] = piece
            return True
        else:
            return False

    def is_free(self, cell):
        """
            Args:
                cell: an instance of Cell to check.

            Returns:
                True is the cell doesn't contain a part of a piece.
        """
        return self.structure[cell.page][cell.row][cell.col] == 0

    def draw_cube(self, show_steps=False):
        """ """
        self.cube_chart.clear()
        self.cube_chart.draw_structure(self.structure, show_steps)
        plt.pause(20)
