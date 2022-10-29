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
from common import Map, MapException, Coordinates

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                #TODO: Criar função para calcular movimentos a fazer com treesearch que retorna uma fila de comandos a efetuar
                #TODO: Ciclo while vai consumir comandos da fila um a um
                
                print(state.get("cursor"))                      # Coordenadas do cursor (x,y)
                print(state.get("grid"))                        # String da grelha
                # print(state.get("selected"))                  # Peça seleccionada

                game_map = Map(state.get("grid"))
                initial_state = ("A", state.get("grid"))
                cursor_coords = Coordinates(state.get("cursor")[0], state.get("cursor")[1])
                strategy = "breadth"

                problem = tree_search.SearchProblem(domain.Domain(), initial_state)
                tree = tree_search.SearchTree(problem, strategy)

                moves = tree.search()

                for move in moves[1:]:
                    map_after_move = Map(move[1])
                    moved_piece = move[0]
                    piece_coords = game_map.piece_coordinates(moved_piece)
                    final_piece_coords = map_after_move.piece_coordinates(moved_piece)

                    # Mover cursor para posição onde a peça a mover se encontra inicialmente
                    if cursor_coords.x > piece_coords[0].x:
                        key = "a"
                    elif cursor_coords.x < piece_coords[0].x:
                        key = "d"
                    elif cursor_coords.y > piece_coords[0].y:
                        key = "s"
                    elif cursor_coords.y < piece_coords[0].y:
                        key = "w"
                    else:
                        key = " "

                    # Mover a peça para as coordenadas correspondentes ao estado da ação recebida
                    if cursor_coords.x > final_piece_coords[0].x:
                        key = "a"
                    elif cursor_coords.x < final_piece_coords[0].x:
                        key = "d"
                    elif cursor_coords.y > final_piece_coords[0].y:
                        key = "s"
                    elif cursor_coords.y < final_piece_coords[0].y:
                        key = "w"
                    else:
                        key = " "


                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )  # send key command to server - you must implement this send in the AI agent
                    break

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

            # Next line is not needed for AI agent
            pygame.display.flip()


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8080")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
