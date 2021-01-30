from utils import (
    WoodColors,
    RotationsFromPositionA,
    RotationsFromPositionB,
    RotationsFromPositionC,
    PieceDisjointCircles,
    PieceContiguousCircles,
    Cube,
    CubeChart
)

ROTATIONS_FROM_A = RotationsFromPositionA()
ROTATIONS_FROM_B = RotationsFromPositionB()
ROTATIONS_FROM_C = RotationsFromPositionC()

PIECES = [
    PieceDisjointCircles("1", WoodColors.ORANGE),
    PieceDisjointCircles("2", WoodColors.DARK_BROWN),
    PieceDisjointCircles("3", WoodColors.ORANGE),
    PieceContiguousCircles("4", WoodColors.DARK_BROWN),
    PieceContiguousCircles("5", WoodColors.LIGHT_BROWN),
    PieceContiguousCircles("6", WoodColors.ORANGE),
    PieceContiguousCircles("7", WoodColors.RED),
    PieceContiguousCircles("8", WoodColors.RED),
    PieceContiguousCircles("9", WoodColors.WHITE)
]

cube_chart = CubeChart()
cube = Cube(
    PIECES, ROTATIONS_FROM_A, ROTATIONS_FROM_B, ROTATIONS_FROM_C, cube_chart
)
cube.solve(randomize_pieces=True, randomize_cells=False)
cube.draw_cube(show_steps=True)
