"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import sound
from collections import namedtuple

# NOT A REAL SPEC, JUST TESTING MAPS
PieceSpec = namedtuple('PieceSpec', 'piece action')


sound.create_sound_bank()


def test_sound(gamestate, events):
    sound.play_sound(PieceSpec(piece='white king', action=sound.Actions.Move))
    return gamestate
