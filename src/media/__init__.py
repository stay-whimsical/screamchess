"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import random

from media import sound
from chess.models import King, Rook, Bishop, Knight, Queen, Pawn


sound.create_sound_bank()


def test_sound(gamestate, events):
    try:
        sound.play_sound(_random_piece(), sound.random_action())
    except ValueError:
        test_sound(gamestate, events)
    return gamestate


def test_sound_sequence(gamestate, events):
    sound.play_sounds([(_random_piece(), sound.random_action()),
                       (_random_piece(), sound.random_action())])
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
        # Pawn('white', 2),
        # Pawn('white', 3),
        Pawn('white', 4),
        Pawn('white', 5),
        # Pawn('white', 6),
        # Pawn('white', 7),
        # Pawn('white', 8),

        # Rook('black', 1),
        Knight('black', 1),
        Bishop('black', 1),
        # Queen('black'),
        # King('black'),
        Bishop('black', 2),
        Knight('black', 2),
        # Rook('black', 2),

        # Pawn('black', 1),
        # Pawn('black', 2),
        # Pawn('black', 3),
        Pawn('black', 4),
        Pawn('black', 5)
        # Pawn('black', 6),
        # Pawn('black', 7),
        # Pawn('black', 8),
    ]
    piece_index = random.randint(0, len(pieces) - 1)
    return pieces[piece_index]
