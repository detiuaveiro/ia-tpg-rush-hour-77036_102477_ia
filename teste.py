from domain import *
from tree_search import *
from time import perf_counter

domain = ( 
            lambda s : func_actions(s),
            lambda s,a : func_result(s,a),
            lambda s,a, p : func_cost(s,a,p),
            lambda s,m,l,d : func_heuristic(s,m,l,d),
            lambda s : func_satisfies(s) 
        )
    
initial_state = ("A", "oCCDDKoEEJoKxAAJoLooIFFLooIoooGGGoox")

problem = (domain, initial_state)

t0 = perf_counter()

tree = SearchTree(problem)

moves = tree.search()

tf = perf_counter()

print("Time to calculate moves", tf - t0)