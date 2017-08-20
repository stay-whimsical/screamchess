"""
What the server needs to keep track of at all times.
"""
from collections import namedtuple

from chess.models import Board

Gamestate = namedtuple('Gamestate', 'current_game should_go_on')


def fresh_gamestate():
    return Gamestate(current_game=Board(), should_go_on=True)
