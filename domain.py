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
    cars.discard('x')

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
    pass


def func_heuristic(state, movement_vector, limit, depth):
    pass


def func_satisfies(state):
    grid_size = state[1]

    car_info = get_car_info(state, 'A')
    car_index = car_info[1]

    car_x = car_index % grid_size + 1

    return car_x == grid_size - 1
