from math import hypot
from tree_search import *
from common import Map, MapException, Coordinates

class Domain(SearchDomain):
    def __init__(self):
        pass

    def actions(self, state):
        print(state)
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

                    vector = Coordinates(i - piece_coords[0].x, 0) if change_direction else Coordinates(i - piece_coords[-1].x, 0)

                    actlist.append((piece, vector))
            else:
                change_direction = False
                for i in range(map_grid.grid_size - 1, -1, -1):
                    if i in [coord.y for coord in piece_coords]:
                        change_direction = True
                        continue 

                    vector = Coordinates(0, i - piece_coords[0].y) if change_direction else Coordinates(0, i - piece_coords[-1].y)

                    actlist.append((piece, vector))
            
        return actlist

    def result(self, state, action):
        current_map = Map(state[1])
        (piece, movement_vector) = action

        try:
            current_map.move(piece, movement_vector)
            return piece, current_map.__str__()
        except MapException:
            return None

    def cost(self, state, action):
        pass
    def heuristic(self, state, goal):
        pass
    def satisfies(self, state):
        current_map = Map(state[1])

        return current_map.test_win()


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

"""
d = Domain()
grid = "02 ooooBoooooBoAAooBooooooooooooooooooo 14"
actList = d.actions(grid)
print(actList)

for a in actList:
    print("Piece" + a[0])
    newGrid = d.result(grid, a)
    print(print_grid(newGrid))

'''
o o o o B o 
o o o o B o 
A A o o B o
o o o o o o
o o o o o o
o o o o o o
'''

"""