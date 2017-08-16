"""
Modules related to operating the camera to read a gamestate. Has a dependency on
chess to appropriately construct board instances.

That said, this drives the main event loop; it's up to this code to use the
camera to determine when a move has occurred and what it even was.
"""
from src.gamestate import Gamestate


def start_event_loop(state):
    print('Starting event loop!')
    return Gamestate(current_game=state.current_game, should_go_on=True)


def stop_event_loop(state):
    print('Stopping event loop!')
    return Gamestate(current_game=state.current_game, should_go_on=True)
