"""Example client."""
import asyncio
import getpass
import json
import os

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame
import websockets
import tree_search
import domain
from domain import print_grid
from common import Map, MapException, Coordinates

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        solved = False
        level = 0
        commands = []

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                
                print(state.get("cursor"))                      # Coordenadas do cursor (x,y)
                print(state.get("grid"))                        # String da grelha
                # print(state.get("selected"))                  # Peça seleccionada

                if level != state.get("level"):
                    solved = False
                    commands = []

                if not solved:
                    # Calculate map movements to complete the level
                    initial_state = ("A", state.get("grid"))
                    strategy = "breadth"
                    problem = tree_search.SearchProblem(domain.Domain(), initial_state)
                    tree = tree_search.SearchTree(problem, strategy)
                    moves = tree.search()
                    print(moves)

                    # Calculate cursor movements to complete level
                    game_map = Map(state.get("grid"))
                    cursor_coords = Coordinates(state.get("cursor")[0], state.get("cursor")[1])
                    for move in moves[1:]:
                        print(print_grid(move[1]))
                        game_map, new_commands, cursor_coords = await get_commands(move, game_map, cursor_coords)
                        commands += new_commands
                    
                    print(commands)

                    solved = True
                    level += 1
                    continue


                await websocket.send(
                    json.dumps({"cmd": "key", "key": commands.pop(0)})
                )  # send key command to server - you must implement this send in the AI agent

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


async def get_commands(move, game_map, cursor_coords):
    cursor_moves = []

    map_after_move = Map(move[1])                                               # Estado do mapa no final do Move ser realizado
    moved_piece = move[0]                                                       # Peça a ser movida
    current_piece_coords = game_map.piece_coordinates(moved_piece)              # Coordenadas atuais da peça
    final_piece_coords = map_after_move.piece_coordinates(moved_piece)          # Coordenadas finais da peça após o Move ser efetuado

    # Mover cursor para posição inicial da peça
    (cursor_coords, moves) = await move_cursor(cursor_coords, current_piece_coords)
    cursor_moves += moves

    # Mover a peça da posição inicial para a posição final
    (cursor_coords, moves) = await move_cursor(cursor_coords, final_piece_coords)
    cursor_moves += moves

    return map_after_move, cursor_moves, cursor_coords


# Move the cursor from an initial position to a final position, given by coordinates
async def move_cursor(cursor_coords, final_coords):
    commands = []

    while cursor_coords != final_coords:
        if cursor_coords.x > final_coords[0].x:
            commands.append("a")
            cursor_coords.x -= 1
        elif cursor_coords.x < final_coords[0].x:
            commands.append("d")
            cursor_coords.x += 1
        elif cursor_coords.y > final_coords[0].y:
            commands.append("w")
            cursor_coords.y -= 1
        elif cursor_coords.y < final_coords[0].y:
            commands.append("s")
            cursor_coords.y += 1
        else:
            commands.append(" ")
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
