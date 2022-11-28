from common import MapException
from map_methods import *
from functools import cache


def func_actions(state):
    map_grid = create_map(state[1])
    pieces = map_grid[-1]

    actlist = []
    for piece in pieces:
        piece_coords = piece_coordinates(map_grid, piece)

        orientation = "vertical" if piece_coords[0][0] == piece_coords[1][0] else "horizontal"

        if orientation == "horizontal":
            # Andar para a frente
            if not piece_coords[-1][0] == 5 and not is_coord_occupied(map_grid, (piece_coords[-1][0] + 1, piece_coords[0][1])):
                actlist.append((piece, (1, 0)))

            # Andar para trás
            if not piece_coords[0][0] == 0 and not is_coord_occupied(map_grid, (piece_coords[0][0] - 1, piece_coords[0][1])):
                actlist.append((piece, (-1, 0)))
        else:
            # Andar para baixo
            if not piece_coords[-1][1] == 5 and not is_coord_occupied(map_grid, (piece_coords[-1][0], piece_coords[-1][1] + 1)):
                actlist.append((piece, (0, 1)))

            # Andar para cima
            if not piece_coords[0][1] == 0 and not is_coord_occupied(map_grid, (piece_coords[0][0], piece_coords[0][1] - 1)):
                actlist.append((piece, (0, -1)))

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


@cache
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
