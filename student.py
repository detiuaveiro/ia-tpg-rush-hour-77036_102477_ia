"""Example client."""
import asyncio
import json
import os
import websockets
import tree_search
from domain import *


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        solved = False
        moves = []
        domain = ( 
            lambda s : func_actions(s),
            lambda s,a : func_result(s,a),
            lambda s,a, p : func_cost(s,a,p),
            lambda s,m,l,d : func_heuristic(s,m,l,d),
            lambda s : func_satisfies(s) 
        )
        prev = ""
        level = 1

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                grid = state.get("grid").split(" ")[1]
                grid_size = state.get("dimensions")[0]
                selected = state.get("selected")
                cursor_coords = (state.get("cursor")[0], state.get("cursor")[1])
                game_level = state.get("level")

                if game_level != level:
                    level = game_level
                    moves = []
                    prev = ""

                if prev != grid:
                    solved = False
                    moves = []

                if not solved:
                    # Calculate map movements to complete the level
                    strategy = "breadth"

                    initial_state = (grid, grid_size)
                    problem = (domain, initial_state)
                    tree = tree_search.SearchTree(problem, strategy)
                    solution = tree.search()

                    for i in range(len(solution) - 1):
                        moved_car = get_moved_car(solution[i], solution[i+1])
                        move = (moved_car, get_car_movement(solution[i], solution[i+1], moved_car), solution[i+1][0])
                        moves.append(move)

                    solved = True
                
                move = moves[0]
                if selected == '':
                    key = get_cursor_move(cursor_coords, (grid, grid_size), move[0])
                    prev = grid
                elif selected == move[0]:
                    prev = move[-1]
                    key = move[1]
                    moves.pop(0)
                elif selected != move[0]:
                    key = ' '
                    prev = grid
                else:
                    solved = False
                    moves = []

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key to server

            except websockets.exceptions.ConnectionClosedOK:
                return




# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", '102477')
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
