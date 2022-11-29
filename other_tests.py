from grid_methods import *

grid1 = 'IJxCCoIJDDMooAAoMNooKEENFFKLoNGGoLHH'
grid2 = 'IJxCCoIJDDMoooAAMNooKEENFFKLoNGGoLHH'

print_grid((grid1, 6))
print()
print_grid((grid2, 6))
print()

# get car that moved in the last move
def get_moved_car(state1, state2):
    grid1 = state1[0]
    grid2 = state2[0]

    for i in range(len(grid1)):
        if grid1[i] != grid2[i]:
            return grid1[i]

    return None

moved_car = get_moved_car((grid1, 6), (grid2, 6))
print(moved_car)

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
    
car_movement = get_car_movement((grid1, 6), (grid2, 6), moved_car)
print(car_movement)