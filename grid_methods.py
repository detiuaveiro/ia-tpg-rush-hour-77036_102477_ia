import math

def get_car_info(state, car_id):
    """
    Returns the information that describes a car in the board, in tuple form.

    Parameters:
        - state1: (grid, grid_size, cursor) -> Current state of the map
        - car_id: Character representing the car

    Returns: Tuple with car ID, the index of the first appearance of the car in grid, the car size and its orientation.
    """
    # grid info
    grid = state[0]

    # car info
    car_index = grid.index(car_id)
    car_size = grid.count(car_id)

    # Calculate car orientation
    if grid[car_index - 1] == car_id  or grid[car_index +  car_size - 1] == car_id:
        car_orientation = 'H'
    else:
        car_orientation = 'V'
    
    return (car_id, car_index, car_size, car_orientation)


def print_grid(state):
    grid = state[0]
    grid_size = state[1]
    for i in range(grid_size):
        for j in range(grid_size):
            print(grid[i * grid_size + j], end = ' ')
        print()


def get_moved_car(state1, state2):
    """
    Determines the car to be moved in a given move, using a comparison between the strings representing the current
    state of the grid and the state of the grid after the move.

    Parameters:
        - state1: (grid, grid_size, cursor) -> State of the map before the move
        - state2: (grid, grid_size, cursor) -> State of the map after the move

    Returns: Char represeting the car to be moved
    """
    grid1 = state1[0]
    grid2 = state2[0]

    for i in range(len(grid1)):
        if grid1[i] != grid2[i]:
            if grid1[i] == 'o':
                return grid2[i]
            else:
                return grid1[i]

    return None


def get_car_movement(state1, state2, car_id):
    """
    Finds the direction in which a car must move in order to go from its position in state1 to its position in
    state2, and returns the key corresponding to that direction.

    Parameters:
       - state1: (grid, grid_size, cursor) -> State of the map before the move
       - state2: (grid, grid_size, cursor) -> State of the map after the move
       - car_id: Character representing the car

    Returns: Key pressed to move the car in the correct direction
    """
    # Getting the car info before and after the move
    car_info_1 = get_car_info(state1, car_id)
    car_info_2 = get_car_info(state2, car_id)

    car_index_1 = car_info_1[1]
    car_index_2 = car_info_2[1]

    car_orientation = car_info_1[3]

    # Determining the coordinates of the car, representing the map in grid form, before and after the move
    car_1_x = car_index_1 % state1[1]
    car_1_y = car_index_1 // state1[1]

    car_2_x = car_index_2 % state2[1]
    car_2_y = car_index_2 // state2[1]

    # Determining in which direction the car must move
    if car_orientation == 'H':
        if car_1_x < car_2_x:
            return 'd'
        else:
            return 'a'
    else:
        if car_1_y < car_2_y:
            return 's'
        else:
            return 'w'


def get_cursor_move(cursor_coords, state, car_id):
    """
    Function used when the cursor of the game currently has no car selected, in order to determine the direction in
    which the cursor must move to select the car being moved in the next move of the Agent.

    Parameters:
       - cursor_coords: (X,Y) -> Current coordinates of the cursor in the game map
       - state: (grid, grid_size, cursor) -> Current state of the map
       - car_id: Character representing the car to be mvoed by the Agent in the next game move

    Returns: Key pressed to move the cursor in the correct direction
    """
    # Getting the info of the car and its current coordinates
    car_info = get_car_info(state, car_id)
    car_coords = get_car_coords(car_info, state)

    # Determining the coordinates of the piece of the car closest to the cursor
    closest_coords = min(car_coords, key=lambda point: math.hypot(cursor_coords[1] - point[1], cursor_coords[0] - point[0]))

    # Deciding which key to press in order to move the cursor in the correct direction
    if closest_coords == cursor_coords:
        return ' '

    if closest_coords[0] == cursor_coords[0]:
        if closest_coords[1] < cursor_coords[1]:
            return 'w'
        else:
            return 's'
    else:
        if closest_coords[0] < cursor_coords[0]:
            return 'a'
        else:
            return 'd'


def get_car_coords(car_info, state):
    """
    Used to determine the coordinates of the game map occupied by a car.

    Parameters:
       - car_info: (car_id, car_index, car_size, car_orientation) -> Tuple representing the car
       - state: (grid, grid_size, cursor) -> Current state of the map

    Returns: List containing all the coordinates the car occupies, in tuple form (X,Y)
    """
    # Destructuring the car_info tuple
    car_index = car_info[1]
    car_length = car_info[2]
    car_orientation = car_info[3]

    # Determining the (X,Y) coordinates of the "front" of the car
    car_x = car_index % state[1]
    car_y = car_index // state[1]

    # Determining the full list of coordinates of the car
    if car_orientation == 'H':
        car_coords = [(car_x + i, car_y) for i in range(car_length)]
    else:
        car_coords = [(car_x, car_y + i) for i in range(car_length)]

    return car_coords