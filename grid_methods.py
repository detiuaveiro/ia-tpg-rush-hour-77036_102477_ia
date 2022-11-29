
def get_car_info(state, car_id):
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


# get car that moved in the last move
def get_moved_car(state1, state2):
    grid1 = state1[0]
    grid2 = state2[0]

    for i in range(len(grid1)):
        if grid1[i] != grid2[i]:
            if grid1[i] == 'o':
                return grid2[i]
            else:
                return grid1[i]

    return None


# get car movement 
def get_car_movement(state1, state2, car_id):
    car_info_1 = get_car_info(state1, car_id)
    car_info_2 = get_car_info(state2, car_id)

    car_index_1 = car_info_1[1]
    car_index_2 = car_info_2[1]

    car_orientation = car_info_1[3]

    car_1_x = car_index_1 % state1[1]
    car_1_y = car_index_1 // state1[1]

    car_2_x = car_index_2 % state2[1]
    car_2_y = car_index_2 // state2[1]

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