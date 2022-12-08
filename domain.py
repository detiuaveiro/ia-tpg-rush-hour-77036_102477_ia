from grid_methods import *

'''
state = (grid, grid_size)
car_info = (car_id, car_index, car_length, car_orientation)
'''

def func_actions(state):
    """
    This function will go through the list of all cars in the current Map, with the goal of determining whether it's
    possible to move them 1 coordinate up/down (in case they're vertical) or 1 coordinate to the sides
    (in case they're horizontal). The move is only considered possible if these coordinates are currently free.

    Parameters:
        - State: (grid, grid_size) -> Current state of the map

    Returns:
        A list of all the possible actions. Each action is represented by a tuple containing the info of the car to be
        moved, and the key corresponding to the direction in which the move will be made (car_info, key).
    """
    grid = state[0]
    grid_size = state[1]
    actlist = []

    # Determining the cars present in the Map
    cars = set(grid)
    cars.remove('o')
    cars.discard('x')

    # Checking the possible actions for each car
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
    """
    This function receives the current state of the Map, as well as an action to be applied to a car in the map, and
    returns the state of the Map after this action is performed.

    Parameters:
        - State: (grid, grid_size) -> Current state of the map
        - Action: (car_info, key) -> Car in which the action will be applied, as well as the key describing the direction
        of the movement.

    Returns:
        A string representing the new State of the map after the move.
    """
    grid = state[0]
    grid_size = state[1]
    car_info = action[0]
    movement = action[1]

    car_id = car_info[0]
    car_index = car_info[1]
    car_size = car_info[2]

    grid_after_move = list(grid)

    if movement == 'w':
        grid_after_move[car_index - grid_size] = car_id
        grid_after_move[car_index + car_size * grid_size - grid_size] = 'o'
    elif movement == 'a':
        grid_after_move[car_index - 1] = car_id
        grid_after_move[car_index + car_size - 1] = 'o'
    elif movement == 's':
        grid_after_move[car_index + car_size * grid_size] = car_id
        grid_after_move[car_index] = 'o'
    else:
        grid_after_move[car_index + car_size] = car_id
        grid_after_move[car_index] = 'o'

    return (''.join(grid_after_move), grid_size)
    

def func_cost(state, parent_state):
    """
    This function is used to calculate the cost of an action, by considering two sub-costs: the cost of moving the cursor
    from its previous position to the piece moved in the current action, and the cost of moving the piece itself.

    This function is deprecated in the current version of the program, which uses the breadth and the greedy algorithms to
     search for a solution, as it was verified that considering the cost always increases the speed of the tree search by
     0.1-0.5 seconds. Thus, this function considers a different deprecated representation of state, in which the ID of the
     moved car is saved.

    Parameters:
        - State: (grid, grid_size, moved_car) -> Current state of the map
        - Parent_State: (grid, grid_size, moved_car) -> Previous state of the map. The moved_car is thus the car that was
        moved in the previous move of the agent.

    Returns:
        The cost of the current action by the Agent
    """
    moved_car = state[-1]
    prev_car = parent_state[-1]

    grid_before_move = parent_state[0]
    grid_after_move = state[0]

    grid_size = state[1]

    # Map of the previous state - used to determine the initial coordinates of the moved car, and to determine the
    # cost of moving the cursor from its position at the end of the previous move, to the car to be moved in the current
    # move
    moved_car_index = grid_before_move.index(moved_car)
    x_moved_car = moved_car_index % grid_size
    y_moved_car = moved_car_index // grid_size

    if prev_car is not None:
        prev_car_index = grid_before_move.index(prev_car)
        x_prev_car = prev_car_index % grid_size
        y_prev_car = prev_car_index // grid_size
        cursor_cost = abs(x_prev_car - x_moved_car) + (y_moved_car - y_prev_car)
    else:
        cursor_cost = 0

    # Current map - used to determine the final coordinates of the moved car after the move, and thus to determine the
    # cost of moving it from its initial position to the final position
    moved_car_new_index = grid_after_move.index(moved_car)

    new_x_moved_car = moved_car_new_index % grid_size
    new_y_moved_car = moved_car_new_index // grid_size

    car_movement_cost = abs(x_moved_car - new_x_moved_car) + (y_moved_car - new_y_moved_car)

    return cursor_cost + car_movement_cost


def func_heuristic(state):
    """
        This function implements the heuristic used in the Greedy and A* search algorithms applied on the project.
        In this heuristic, the process starts by checking the distance the player car is from the edge of the map, with
        each tile representing 1 heuristic cost. Afterwards, the function verifies how many cars are in the tiles corresponding
        to the line the player car is in, with each car counting as 1 additional heuristic cost.

        Parameters:
            - State: (grid, grid_size) -> Current state of the map

        Returns:
            The heuristic cost of the current state.
    """
    grid = state[0]
    grid_size = state[1]

    # Determining the line of the player car ('A')
    A_index = grid.index('A')

    # calculate the distance from the player car to the right edge of the map
    h = grid_size - (A_index % grid_size + 1)

    # subtract the number of empty cells in the line of the player car
    h -= grid[A_index - A_index % grid_size: A_index - A_index % grid_size + grid_size].count('o')

    return h



def func_satisfies(state):
    """
    This function will verify if the current State of the map already satisfies the conditions to move on to the next
    level, that is, if the player car ('A') is at the right edge of the map.

    Parameters:
        - State: (grid, grid_size) -> Current state of the map

    Returns:
        True if the car is on the edge of the map, False if not.
    """
    grid_size = state[1]

    car_info = get_car_info(state, 'A')
    car_index = car_info[1]

    # Determining the X coordinate of the player car
    car_x = car_index % grid_size + 1

    return car_x == grid_size - 1
