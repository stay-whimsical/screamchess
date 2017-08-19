"""
What the server needs to keep track of at all times.
"""
from collections import namedtuple

from chess import fresh_game

Gamestate = namedtuple('Gamestate', 'current_game should_go_on do_a_thing')


def a_thing(gamestate):
    pass


def fresh_gamestate():
    return Gamestate(current_game=fresh_game(), should_go_on=True, do_a_thing=a_thing)
