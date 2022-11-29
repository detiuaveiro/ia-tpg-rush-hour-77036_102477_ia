from common import MapException
from map_methods import *
from functools import cache
from grid_methods import *

'''
state = (grid, grid_size, cursor)
'''

def func_actions(state):
    grid = state[0]
    grid_size = state[1]
    actlist = []

    cars = set(grid)
    cars.remove ('o')
    try:
        cars.remove('x')
    except:
        pass

    for car in cars:
        car_info = get_car_info(state, car)
        car_index = car_info[1]
        car_size = car_info[2]
        car_orientation = car_info[3]

        if car_orientation == 'H':
            if car_index % grid_size != 0 and grid[car_index - 1] == 'o':
                actlist.append((car_info, 'a'))
            if car_index % grid_size + car_size < grid_size and grid[car_index + car_size] == 'o':
                actlist.append((car_info, 'd'))
        else:
            if car_index >= grid_size and grid[car_index - grid_size] == 'o':
                actlist.append((car_info, 'w'))
            if car_index + car_size * grid_size < grid_size * grid_size and grid[car_index + car_size * grid_size] == 'o':
                actlist.append((car_info, 's'))

    return actlist


def func_result(state, action):
    grid = state[0]
    grid_size = state[1]
    car_info = action[0]
    movement = action[1]

    car_id = car_info[0]
    car_index = car_info[1]
    car_size = car_info[2]

    grid_after_move = list(grid)

    match movement:
        case 'w':
            grid_after_move[car_index - grid_size] = car_id
            grid_after_move[car_index + car_size * grid_size - grid_size] = 'o'
        case 'a':
            grid_after_move[car_index - 1] = car_id
            grid_after_move[car_index + car_size - 1] = 'o'
        case 's':
            grid_after_move[car_index + car_size * grid_size] = car_id
            grid_after_move[car_index] = 'o'
        case 'd':
            grid_after_move[car_index + car_size] = car_id
            grid_after_move[car_index] = 'o'
    
    return (''.join(grid_after_move), grid_size)
    

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
    grid = state[0]
    grid_size = state[1]

    if grid_size % 2 == 0:
        return grid[len(grid) // 2 + grid_size - 1] == 'A'
    else:
        return grid[len(grid) // 2 - 1] == 'A'
