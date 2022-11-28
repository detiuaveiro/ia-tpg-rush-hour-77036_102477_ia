
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

