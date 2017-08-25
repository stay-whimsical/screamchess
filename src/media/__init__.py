"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import random

import sound
from chess.models import King, Rook, Bishop, Knight, Queen, Pawn


sound.create_sound_bank()


def test_sound(gamestate, events):
    sound.play_sound(_random_piece(), sound.random_action())
    return gamestate


def _random_piece():
    pieces = [
              Rook('white', 1),
              Knight('white', 1),
              Bishop('white', 1),
              Queen('white'),
              King('white'),
              Bishop('white', 2),
              Knight('white', 2),
              Rook('white', 2),
              Pawn('white', 1),
              Pawn('white', 4),
              Pawn('white', 5),

              Knight('black', 1),
              Bishop('black', 1),
              Knight('black', 2),
              Pawn('black', 4),
              Pawn('black', 5)]
    piece_index = random.randint(0, len(pieces) - 1)
    return pieces[piece_index]
