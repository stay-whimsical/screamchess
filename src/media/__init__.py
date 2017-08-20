"""
Code used to play various sounds, blink LEDs, and manage the media generally.
"""
import sound

from chess.models import King

sound.create_sound_bank()


def test_sound(gamestate, events):
    sound.play_sound(King('white'), sound.Actions.MoveSafety)
    return gamestate
