from domain import *
from tree_search import *
from time import perf_counter
from grid_methods import *
import math

domain = ( 
            lambda s : func_actions(s),
            lambda s,a : func_result(s,a),
            lambda s,a, p : func_cost(s,a,p),
            lambda s,m,l,d : func_heuristic(s,m,l,d),
            lambda s : func_satisfies(s) 
        )
    
initial_state = ("ooxLCCoooLDDAAKoooIJKEENIJFFMNGGHHMN", 6)

print_grid(initial_state)

problem = (domain, initial_state)

tree = SearchTree(problem)

solution = tree.search()


moves = []
for i in range(len(solution) - 1):
    moved_car = get_moved_car(solution[i], solution[i+1])
    move = (moved_car, get_car_movement(solution[i], solution[i+1], moved_car))
    moves.append(move)


cursor_coords = (5, 5)
selected_car = ''

move = moves[0]


def get_cursor_move(cursor_coords, state, car_id):
    car_info = get_car_info(state, car_id)
    car_coords = get_car_coords(car_info, state)

    closest_coords = min(car_coords, key=lambda point: math.hypot(cursor_coords[1] - point[1], cursor_coords[0] - point[0]))

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
    car_index = car_info[1]
    car_length = car_info[2]
    car_orientation = car_info[3]

    car_x = car_index % state[1]
    car_y = car_index // state[1]

    if car_orientation == 'H':
        car_coords = [(car_x + i, car_y) for i in range(car_length)]
    else:
        car_coords = [(car_x, car_y + i) for i in range(car_length)]

    return car_coords

if selected_car == '':
    t0 = perf_counter()
    key = get_cursor_move(cursor_coords, initial_state, move[0])
    tf = perf_counter()
elif selected_car == move[-1]:
    key = move[0]
    moves.pop(-1)
else:
    key = ''

print("Time to calculate closest coords", tf - t0)
print(key)