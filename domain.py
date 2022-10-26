from math import hypot
from tree_search import *
from common import Map, MapException, Coordinates

class Domain(SearchDomain):
    def __init__(self):
        pass

    def actions(self, grid: str):
        map_grid = Map(grid)    
        pieces = set([a[2] for a in map_grid.coordinates])

        actlist = []
        for piece in pieces:
            piece_coords = map_grid.piece_coordinates(piece)
            orientation = "horizontal" if len(set([coord.x for coord in piece_coords])) == 1 else "vertical"

            if orientation == "horizontal":
                change_direction = False
                for i in range(map_grid.grid_size, 0, -1):
                    if i in [coord.y for coord in piece_coords]:
                        change_direction = True
                        continue 

                    vector = Coordinates(i - piece_coords[0].x, 0) if change_direction else Coordinates(i - piece_coords[-1].x, 0)

                    actlist.append(piece, vector)
            else:
                change_direction = False
                for i in range(map_grid.grid_size, 0, -1):
                    if i in [coord.x for coord in piece_coords]:
                        change_direction = True
                        continue 

                    vector = Coordinates(0, i - piece_coords[0].y) if change_direction else Coordinates(0, i - piece_coords[-1].y)

                    actlist.append(piece, vector)
            
            return actlist



    def result(self):
        pass
    def cost(self):
        pass
    def heuristic(self):
        pass
    def satisfies(self, state, goal):
        pass


d = Domain()
print(d.actions("02 ooooBoooooBoAAooBooooooooooooooooooo 14"))