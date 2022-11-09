import math
from common import MapException
'''
map = (grid_size, grid, cars)
'''

empty_tile = "o"
wall_tile = "x"
player_car = "A"

def create_map(grid_str: str):
    grid_size = int(math.sqrt(len(grid_str)))
    grid = []

    line = []
    for i, pos in enumerate(grid_str):
        line.append(pos)
        if (i + 1) % grid_size == 0:
            grid.append(line)
            line = []

    cars = set([car for car in grid_str if car != wall_tile and car != empty_tile])

    return (grid_size, grid, cars)


def map_to_string(map):
    """Revert map object to string."""
    raw = ""
    for line in map[1]:
        for column in line:
            raw += column
    return f"{raw}"


def coordinates(map):
    """Representation of ocupied map positions through tuples x,y,value."""
    _coordinates = []

    for y, line in enumerate(map[1]):
        for x, column in enumerate(line):
            if column != empty_tile:
                _coordinates.append((x, y, column))

    return _coordinates


def piece_coordinates(map, piece: str):
    """List coordinates holding a piece."""
    return [(x, y) for (x, y, p) in coordinates(map) if p == piece]


def is_occupied(map, vector):
    """Checks if a given coordinate is occupied by a piece"""
    if len([p for (x, y, p) in coordinates(map) if x == vector[0] and y == vector[1]]) > 0:
        return True
    else:
        return False


def get(map, cursor):
    """Return piece at cursor position."""
    if 0 <= cursor[0] < map[0] and 0 <= cursor[1] < map[0]:
        return map[1][int(cursor[1])][int(cursor[0])]
    raise MapException("Out of the grid")


def move(map, piece: str, vector):
        """Move piece in direction given by a vector."""
        if piece == wall_tile:
            raise MapException("Blocked piece")

        piece_coord = piece_coordinates(map, piece)

        # Don't move vertical pieces sideways
        if vector[0] != 0 and any([line.count(piece) == 1 for line in map[1]]):
            raise MapException("Can't move sideways")
        # Don't move horizontal pieces up-down
        if vector[1] != 0 and any([line.count(piece) > 1 for line in map[1]]):
            raise MapException("Can't move up-down")

        def sum(a, b):
            return (a[0] + b[0], a[1] + b[1])

        for pos in piece_coord:
            if not get(map, sum(pos, vector)) in [piece, empty_tile]:
                raise MapException("Blocked piece")

        for pos in piece_coord:
            map[1][pos[1]][pos[0]] = empty_tile

        for pos in piece_coord:
            new_pos = sum(pos, vector)
            map[1][new_pos[1]][new_pos[0]] = piece

        return map

def test_win(map):
    """Test if player_car has crossed the left most column."""
    return any(
        [c[0] == map[0] - 1 for c in piece_coordinates(map, player_car)]
    )


'''
map = create_map("oooooHoxCCoHAAoGoooFoGoooFDDxooooooo")
print(coordinates(map))
print(piece_coordinates(map, "A"))
grid = move(map, "A", (1,0))
print(piece_coordinates(map, "A"))
print(map)
print(map_to_string(map))
'''