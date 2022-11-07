from math import hypot
from tree_search import *
from common import Map, MapException, Coordinates

def func_actions(state):
    map_grid = Map(state[1])
    pieces = set([a[2] for a in map_grid.coordinates])

    actlist = []
    for piece in pieces:
        piece_coords = map_grid.piece_coordinates(piece)
        orientation = "vertical" if len(set([coord.x for coord in piece_coords])) == 1 else "horizontal"

        if orientation == "horizontal":
            change_direction = False
            for i in range(map_grid.grid_size - 1, -1, -1):
                if i in [coord.x for coord in piece_coords]:
                    change_direction = True
                    continue

                vector = Coordinates(i - piece_coords[0].x, 0) if change_direction else Coordinates(
                    i - piece_coords[-1].x, 0)

                actlist.append((piece, vector))
        else:
            change_direction = False
            for i in range(map_grid.grid_size - 1, -1, -1):
                if i in [coord.y for coord in piece_coords]:
                    change_direction = True
                    continue

                vector = Coordinates(0, i - piece_coords[0].y) if change_direction else Coordinates(0, i - piece_coords[
                    -1].y)

                actlist.append((piece, vector))

    return actlist
def func_result(state,action):
    current_map = Map(state[1])
    (piece, movement_vector) = action

    if movement_vector.x > 0:
        for i in range(1, movement_vector.x + 1):
            try:
                current_map.move(piece, Coordinates(1, 0))
            except MapException:
                return None
    elif movement_vector.x < 0:
        for i in range(-1, movement_vector.x - 1, -1):
            try:
                current_map.move(piece, Coordinates(-1, 0))
            except MapException:
                return None
    elif movement_vector.y > 0:
        for i in range(1, movement_vector.y + 1):
            try:
                current_map.move(piece, Coordinates(0, 1))
            except MapException:
                return None
    elif movement_vector.y < 0:
        for i in range(-1, movement_vector.y - 1, -1):
            try:
                current_map.move(piece, Coordinates(0, -1))
            except MapException:
                return None
    return piece, current_map.__str__()
def func_cost(state, action):
    pass
def func_heuristic(state,goal):
    pass
def func_satisfies(state):
    current_map = Map(state[1])

    return current_map.test_win()

'''
class Domain(SearchDomain):
    def __init__(self):
        pass

    def actions(self, state):
        return func_actions(state)

    def result(self, state, action):
        return func_result(state, action)

    def cost(self, state, action):
        pass
    def heuristic(self, state, goal):
        pass
    def satisfies(self, state):
        return func_satisfies(state)
'''


''' TESTS '''
def print_grid(state):
    """Prints the map object in an easier to read format"""
    if state is None:
        return None

    grid = state.split(" ")[1]
    raw = ""
    i = 1
    for char in grid:
        raw += char
        if i%6 == 0:
            raw += "\n"
        i += 1
    return f"{raw}"

'''
d = Domain()
grid = ('A', '04 oooooHoxCCoHAAoGoooFoGoooFDDxooooooo 302')
print("Initial Grid")
print(print_grid(grid[1]))
actList = d.actions(grid)
print(actList)

for a in actList:
    print("\nPiece " + a[0])
    try:
        piece, newGrid = d.result(grid, a)
        print(a)
        print(print_grid(newGrid))
    except:
        print("None")


'''

'''
o o o o o H 
o x C C o H
A A o G o o
o F o G o o
o F D D x o
o o o o o o
'''
