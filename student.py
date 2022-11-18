"""Example client."""
import asyncio
import getpass
import json
import os
import time
# Next 4 lines are not needed for AI agents, please remove them from your code!
import websockets
import tree_search
from domain import print_grid, func_satisfies, func_result, func_actions, func_cost, func_heuristic
from common import Map, MapException, Coordinates
from map_methods import create_map, map_to_string, coordinates, piece_coordinates, get, move, test_win



async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        solved = False
        level = 1
        commands = []
        domain = ( lambda s : func_actions(s),
                              lambda s,a : func_result(s,a),
                              lambda s,a, p : func_cost(s,a,p),
                              lambda s,m,l,d : func_heuristic(s,m,l,d),
                              lambda s : func_satisfies(s) )
        tf = 0
        prev = ""

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                
                print(state.get("cursor"))                      # Coordenadas do cursor (x,y)
                print(state.get("grid"))                        # String da grelha
                print(state.get("game_speed"))
                # print(state.get("selected"))                  # Peça seleccionada

                if prev != state.get("grid").split(" ")[1]:
                    print("OH NO MY STATE CHANGED!")
                    prev = state.get("grid").split(" ")[1]
                    solved = False
                    commands = []
                    tf = 0
                    level -= 1

                '''
                if level != state.get("level"):
                    solved = False
                    commands = []
                    tf = 0
                '''
                if not solved:
                    # Calculate map movements to complete the level
                    initial_state \
                        = ("A", state.get("grid").split(" ")[1])
                    strategy = "uniform"
                    ## problem = tree_search.SearchProblem(domain.Domain(), initial_state)
                    t0 = time.process_time()

                    problem = (domain, initial_state)
                    tree = tree_search.SearchTree(problem, strategy)
                    moves = tree.search()

                    print(f"Time for tree search: {time.process_time()-t0}")
                    print(moves)

                    # Calculate cursor movements to complete level
                    game_map = create_map(state.get("grid").split(" ")[1])
                    cursor_coords = (state.get("cursor")[0], state.get("cursor")[1])
                    last_moved_piece = None
                    for move in moves[1:]:
                        #print(print_grid(move[1]))
                        game_map, new_commands, cursor_coords = await get_commands(move, game_map, cursor_coords, last_moved_piece)
                        commands += new_commands
                        last_moved_piece = move[0]

                    tf = time.process_time() - t0
                    tf = tf*10
                    
                    print(f"Time to calculate moves: {tf}")
                    print(commands)

                    solved = True
                    level += 1

                '''
                if (len(commands) == 0):
                    solved = False
                    break
                '''

                if tf > 1:
                    tf -= 1
                    continue

                command = commands.pop(0)
                await websocket.send(
                    json.dumps({"cmd": "key", "key": command[0]})
                )  # send key command to server - you must implement this send in the AI agent

                prev = command[1]
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


async def get_commands(move, game_map, cursor_coords, last_moved_piece):
    cursor_moves = []

    map_after_move = create_map(move[1])                                               # Estado do mapa no final do Move ser realizado
    moved_piece = move[0]                                                       # Peça a ser movida
    current_piece_coords = piece_coordinates(game_map,moved_piece)              # Coordenadas atuais da peça
    final_piece_coords = piece_coordinates(map_after_move,moved_piece)          # Coordenadas finais da peça após o Move ser efetuado

    # Mover cursor para posição inicial da peça
    if last_moved_piece != moved_piece:
        (cursor_coords, moves) = move_cursor(cursor_coords, current_piece_coords, game_map)
        cursor_moves += moves

    # Mover a peça da posição inicial para a posição final
    (cursor_coords, moves) = move_cursor(cursor_coords, final_piece_coords, game_map, moved_piece, True, last_moved_piece)
    cursor_moves += moves


    return map_after_move, cursor_moves, cursor_coords


# Move the cursor from an initial position to a final position, given by coordinates
def move_cursor(cursor_coords, final_coords, game_map, moved_piece=None, movingPiece=False, last_moved_piece=None):
    commands = []

    while cursor_coords != final_coords:
        if cursor_coords[0] > final_coords[0][0]:
            if movingPiece:
                game_map = move(game_map, moved_piece, (-1,0))
            commands.append(("a", map_to_string(game_map)))
            cursor_coords = (cursor_coords[0]-1, cursor_coords[1])
        elif cursor_coords[0] < final_coords[0][0]:
            if movingPiece:
                game_map = move(game_map, moved_piece, (1,0))
            commands.append(("d", map_to_string(game_map)))
            cursor_coords = (cursor_coords[0]+1, cursor_coords[1])
        elif cursor_coords[1] > final_coords[0][1]:
            if movingPiece:
                game_map = move(game_map, moved_piece, (0, -1))
            commands.append(("w", map_to_string(game_map)))
            cursor_coords = (cursor_coords[0], cursor_coords[1]-1)
        elif cursor_coords[1] < final_coords[0][1]:
            if movingPiece:
                game_map = move(game_map, moved_piece, (0, 1))
            commands.append(("s", map_to_string(game_map)))
            cursor_coords = (cursor_coords[0], cursor_coords[1]+1)
        else:
            if moved_piece != None and last_moved_piece != moved_piece:
                commands.append((" ", map_to_string(game_map)))
            break

    return cursor_coords, commands

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
