"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import random

import sound
from chess.models import King, Rook, Bishop, Knight


sound.create_sound_bank()


def test_sound(gamestate, events):
    sound.play_sound(_random_piece(), sound.random_action())
    return gamestate


def _random_piece():
    pieces = [King('white'), Rook('white'), Bishop('white'), Knight('white')]
    piece_index = random.randint(0, len(pieces) - 1)
    return pieces[piece_index]
