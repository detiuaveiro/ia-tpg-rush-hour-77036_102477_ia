"""Example client."""
import asyncio
import getpass
import json
import os
import time
# Next 4 lines are not needed for AI agents, please remove them from your code!
import websockets
import tree_search
from domain import func_satisfies, func_result, func_actions, func_cost, func_heuristic
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
        cars_to_move = []
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
                
                #print(state.get("cursor"))                      # Coordenadas do cursor (x,y)
                #print(state.get("grid"))                        # String da grelha
                #print(state.get("game_speed"))
                # print(state.get("selected"))                  # Peça seleccionada

                #TODO: Recalcular tree search apenas se crazy car afetou uma peça que vamos mover
                newstate = state.get("grid").split(" ")[1]
                if prev != newstate:
                    moved_car = "none"
                    for i in range(0, len(prev)):
                        if prev[i] != newstate[i]:
                            moved_car = newstate[i]

                    if moved_car in set(cars_to_move):
                        #print("Oh no my state changed!")
                        prev = newstate
                        solved = False
                        commands = []
                        tf = 0
                        #print("A car I don't care about moved!")

                if not solved:
                    # Calculate map movements to complete the level
                    initial_state \
                        = ("A", state.get("grid").split(" ")[1])
                    strategy = "a*"
                    cars_to_move = []
                    ## problem = tree_search.SearchProblem(domain.Domain(), initial_state)
                    t0 = time.process_time()

                    problem = (domain, initial_state)
                    tree = tree_search.SearchTree(problem, strategy)
                    moves = tree.search()

                    #print(f"Time for tree search: {time.process_time()-t0}")
                    #print(moves)

                    # Calculate cursor movements to complete level
                    game_map = create_map(state.get("grid").split(" ")[1])
                    cursor_coords = (state.get("cursor")[0], state.get("cursor")[1])
                    last_moved_piece = None
                    for move in moves[1:]:
                        #print(print_grid(move[1]))
                        if len(cars_to_move) <= 5:
                            cars_to_move.append(move[0])
                        game_map, new_commands, cursor_coords = await get_commands(move, game_map, cursor_coords, last_moved_piece)
                        commands += new_commands
                        last_moved_piece = move[0]

                    tf = time.process_time() - t0
                    tf = tf*state.get("game_speed")
                    
                    #print(f"Time to calculate moves: {tf}")
                    #print(commands)

                    solved = True

                if tf > 1:
                    tf -= 1
                    continue

                if len(commands) != 0:
                    command = commands.pop(0)
                else:
                    solved = False
                    #print("I ran out of commands :(")
                    continue

                await websocket.send(
                    json.dumps({"cmd": "key", "key": command[0]})
                )  # send key command to server - you must implement this send in the AI agent

                prev = command[1]
            except websockets.exceptions.ConnectionClosedOK:
                #print("Server has cleanly disconnected us")
                return


async def get_commands(move, game_map, cursor_coords, last_moved_piece):
    cursor_moves = []

    map_after_move = create_map(move[1])                                                # Estado do mapa no final do Move ser realizado
    moved_piece = move[0]                                                               # Peça a ser movida
    current_piece_coords = piece_coordinates(game_map,moved_piece)                      # Coordenadas atuais da peça
    final_piece_coords = piece_coordinates(map_after_move,moved_piece)                  # Coordenadas finais da peça após o Move ser efetuado

    # Mover cursor para posição inicial da peça
    if last_moved_piece != moved_piece:
        if last_moved_piece is not None:
            cursor_moves.append((" ", map_to_string(game_map)))
        (cursor_coords, moves) = move_cursor(cursor_coords, current_piece_coords, game_map)
        cursor_moves += moves

    # Mover a peça da posição inicial para a posição final
    (cursor_coords, moves) = move_cursor(cursor_coords, final_piece_coords, game_map, moved_piece, True)
    cursor_moves += moves

    return map_after_move, cursor_moves, cursor_coords


# Move the cursor from an initial position to a final position, given by coordinates
def move_cursor(cursor_coords, final_coords, game_map, moved_piece=None, movingPiece=False):
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
            if moved_piece is None:
                commands.append((" ", map_to_string(game_map)))
            break

    return cursor_coords, commands

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", '102477')
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
