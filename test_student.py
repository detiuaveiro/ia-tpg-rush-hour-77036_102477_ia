from domain import *
from tree_search import *
from time import perf_counter
from grid_methods import *

domain = ( 
            lambda s : func_actions(s),
            lambda s,a : func_result(s,a),
            lambda s,a, p : func_cost(s,a,p),
            lambda s,m,l,d : func_heuristic(s,m,l,d),
            lambda s : func_satisfies(s) 
        )
    
initial_state = ("ooooooooooBoAAooBooooooooooooooooooo", 6)

problem = (domain, initial_state)

tree = SearchTree(problem)

solution = tree.search()

t0 = perf_counter()

moves = []
for i in range(len(solution) - 1):
    moved_car = get_moved_car(solution[i], solution[i+1])
    move = (moved_car, get_car_movement(solution[i], solution[i+1], moved_car))
    moves.append(move)

tf = perf_counter()

print(moves)
print()
print("Time to calculate moves", tf - t0)