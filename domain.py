from math import hypot
from tree_search import *
from common import Map, MapException, Coordinates
from map_methods import create_map, map_to_string, coordinates, piece_coordinates, get, move, test_win, is_occupied, move_cursor



def func_actions(state):
    map_grid = create_map(state[1])
    pieces = map_grid[-1]

    actlist = []
    for piece in pieces:
        piece_coords = piece_coordinates(map_grid, piece)
        piece_x_coords = [coord[0] for coord in piece_coords]
        piece_y_coords = [coord[1] for coord in piece_coords]
        orientation = "vertical" if len(set(piece_x_coords)) == 1 else "horizontal"

        if orientation == "horizontal":
            max_x = max(piece_x_coords)
            min_x = min(piece_x_coords)

            # Andar para a frente
            for i in range(max_x + 1, map_grid[0], 1):
                if len(is_occupied(map_grid, (i, piece_coords[0][1]))) > 0:
                    break

                vector = (i - max_x, 0)

                actlist.append((piece, vector))

            # Andar para trás
            for i in range(min_x - 1, -1, -1):
                if len(is_occupied(map_grid, (i, piece_coords[0][1]))) > 0:
                    break

                vector = (i - min_x, 0)

                actlist.append((piece, vector))
        else:
            max_y = max(piece_y_coords)
            min_y = min(piece_y_coords)

            # Andar para baixo
            for i in range(max_y + 1, map_grid[0], 1):
                if len(is_occupied(map_grid, (piece_coords[0][0], i))) > 0:
                    break

                vector = (0, i - max_y)

                actlist.append((piece, vector))

            # Andar para cima
            for i in range(min_y - 1, -1, -1):
                if len(is_occupied(map_grid, (piece_coords[0][0], i))) > 0:
                    break

                vector = (0, i - min_y)

                actlist.append((piece, vector))

    return actlist


def func_result(state, action):
    current_map = create_map(state[1])
    (piece, movement_vector) = action

    try:
        current_map = move(current_map, piece, movement_vector)
    except MapException:
        return None

    return piece, map_to_string(current_map)


def func_cost(state, action, parent_state):
    current_map = create_map(state[1])
    (piece, movement_vector) = action

    # Coordenadas do cursor no inicio da ação
    cursor_coords = piece_coordinates(current_map, parent_state[0])[0]
    # Coordenadas da peça no inicio da ação
    piece_coords = piece_coordinates(current_map, piece)

    cursor_cost = len(move_cursor(cursor_coords, piece_coords)[1])

    return cursor_cost + abs(movement_vector[0] + movement_vector[1]) + 1


def func_heuristic(state, movement_vector, limit, depth):
    h_cost = 0
    blocking_pieces = set()

    if depth >= limit:
        return float("inf")

    piece_to_move = state[0]
    current_map = create_map(state[1])
    piece_coords = piece_coordinates(current_map, piece_to_move)
    piece_x_coords = [coord[0] for coord in piece_coords]
    piece_to_move_orientation = "vertical" if len(set(piece_x_coords)) == 1 else "horizontal"


    if movement_vector[0] != 0 and movement_vector[0] > 0:
        # Horizontal a andar para a frente
        for i in range(piece_coords[-1][0] + 1, piece_coords[-1][0] + movement_vector[0] + 1, 1):
            blocks = is_occupied(current_map, (i, piece_coords[0][1]))
            if len(blocks) > 0:
                blocking_pieces.add(blocks[0])
            if i > 5 or i < 0:
                return float("inf")
    elif movement_vector[0] != 0 and movement_vector[0] < 0:
        # Horizontal a andar para trás
        for i in range(piece_coords[0][0] - 1, piece_coords[0][0] - movement_vector[0] - 1, -1):
            blocks = is_occupied(current_map, (i, piece_coords[0][1]))
            if len(blocks) > 0:
                blocking_pieces.add(blocks[0])
            if i > 5 or i < 0:
                return float("inf")
    elif movement_vector[1] != 0 and movement_vector[1] > 0:
        # Vertical a andar para baixo
        for i in range(piece_coords[-1][1] + 1, piece_coords[-1][1] + movement_vector[1] + 1, 1):
            blocks = is_occupied(current_map, (piece_coords[0][0], i))
            if len(blocks) > 0:
                blocking_pieces.add(blocks[0])
            if i > 5 or i < 0:
                return float("inf")
    else:
        # Vertical a andar para cima
        for i in range(piece_coords[0][1] - 1, piece_coords[0][1] - movement_vector[1] - 1, -1):
            blocks = is_occupied(current_map, (piece_coords[0][0], i))
            if len(blocks) > 0:
                blocking_pieces.add(blocks[0])
            if i > 5 or i < 0:
                return float("inf")

    if len(blocking_pieces) > 0:
        h_cost += abs(movement_vector[0] + movement_vector[1])

    if "x" in blocking_pieces:
        return float("inf")

    for piece in blocking_pieces:
        new_piece_coords = piece_coordinates(current_map, piece)
        new_piece_x_coords = [coord[0] for coord in new_piece_coords]
        new_piece_y_coords = [coord[1] for coord in new_piece_coords]
        new_piece_length = len(new_piece_y_coords)
        orientation = "vertical" if len(set(new_piece_x_coords)) == 1 else "horizontal"

        if orientation == "horizontal" and piece_to_move_orientation == "horizontal":
            h_cost += func_heuristic((piece, current_map), movement_vector, limit, depth + 1)
        elif orientation == "horizontal" and piece_to_move_orientation == "vertical":
            h1 = func_heuristic((piece, current_map), (piece_coords[0][0] - new_piece_coords[0][0]  + 1, 0), limit, depth + 1)
            h2 = func_heuristic((piece, current_map), (piece_coords[0][0] - (new_piece_coords[0][0] + new_piece_length -1) - 1, 0), limit, depth + 1)
            h_cost += min(h1, h2)
        elif orientation == "vertical" and piece_to_move_orientation == "vertical":
           h_cost += func_heuristic((piece, current_map), movement_vector, limit, depth + 1)
        else:
            h1 = func_heuristic((piece, current_map), (piece_coords[0][1] - new_piece_coords[0][1] + 1, 0), limit,
                                depth + 1)
            h2 = func_heuristic((piece, current_map),
                                (piece_coords[0][1] - (new_piece_coords[0][1] + new_piece_length - 1) - 1, 0), limit,
                                depth + 1)
            h_cost += min(h1, h2)

    return h_cost


def func_satisfies(state):
    current_map = create_map(state[1])

    return test_win(current_map)


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

    grid = state
    raw = ""
    i = 1
    for char in grid:
        raw += char
        if i % 6 == 0:
            raw += "\n"
        i += 1
    return f"{raw}"


d = (lambda s: func_actions(s),
     lambda s, a: func_result(s, a),
     lambda s, a: func_cost(s, a),
     lambda s, goal: func_heuristic(s, goal),
     lambda s: func_satisfies(s))
grid = ('A', 'oBBCCoooFGHoAAFGHooooGooxoEEoooooooo')
print("Initial Grid")
print(print_grid(grid[1]))
actList = d[0](grid)
print(actList)

for a in actList:
    print("\nPiece " + a[0])
    print("\nCost: " + str(func_cost((a[0], "oBBCCoooFGHoAAFGHooooGooxoEEoooooooo"), a, ("G", "oBBCCoooFGHoAAFGHooooGooxoEEoooooooo"))))
    print("\nHeuristic: " + str(func_heuristic((a[0], "oBBCCoooFGHoAAFGHooooGooxoEEoooooooo"), a[1], 4, 0)))
    try:
        piece, newGrid = d[1](grid, a)
        print(a)
        print(print_grid(newGrid))
    except:
        print("None")

'''
o o o o o o 
o x C C o H
A A o G o H
o F o G o o
o F D D x o
o o o o o o
'''
