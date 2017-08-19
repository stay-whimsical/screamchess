"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import sound
from collections import namedtuple

# NOT A REAL SPEC, JUST TESTING MAPS
PieceSpec = namedtuple('PieceSpec', 'piece action')


def test_sound(gamestate, events):
    sound.play_sound(PieceSpec(piece='white king', action='move'))
    return gamestate
