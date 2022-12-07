from domain import *
from tree_search import *
from time import perf_counter
from grid_methods import *

domain = ( 
            lambda s : func_actions(s),
            lambda s,a : func_result(s,a),
            lambda a,p : func_cost(a,p),
            lambda s : func_heuristic(s),
            lambda s : func_satisfies(s) 
        )
    
initial_state = ("ooooooooooooCFILooooCFILoooBDGJMAAoBDGJMooooEHKNooooEHKNoooooooo", 8)

problem = (domain, initial_state)

t0 = perf_counter()

tree = SearchTree(problem, "a*")

moves = tree.search()

tf = perf_counter()

for move in moves:
    print_grid(move)
    print()

print("Time to calculate moves", tf - t0)
