"""
Code used to play sound specifically. We do this the dumbest way possible:
piping commands to the parent OS shell. We don't want to hold up the rest of
the loop with playing sounds, so we'll do them in a separate Python green
thread, like triple hooligans. Much of the fun of the project is the notion
that VIOLENCE IS FUN when it's chess pieces; we will go Full Meta and commit
violence to software engineering principles while we're here.

(after all, this is Python, hyuk hyuk hyuk)
"""
import os
import subprocess
import threading
import platform


ACTIONS_MAP = {
    'kill': 'kill',
    'move': 'move',
    'die': 'die',
    'lift': 'lift',
    'boo': 'boo'
}


# The map of piecenames in the assets directory. Keys are just placeholders,
# but the values are real.
PIECE_MAP = {
    'white pawn': 'whitePawn1',
    'white pawn': 'whitePawn2',
    'white pawn': 'whitePawn3',
    'white pawn': 'whitePawn4',
    'white pawn': 'whitePawn5',
    'white pawn': 'whitePawn6',
    'white pawn': 'whitePawn7',
    'white pawn': 'whitePawn8',
    'white pawn': 'whiteRook1',
    'white pawn': 'whiteRook2',
    'white knight': 'whiteKnight1',
    'white knight': 'whiteKnight2',
    'white bishop': 'whiteBishop1',
    'white bishop': 'whiteBishop2',
    'white queen': 'whiteQueen',
    'white king': 'whiteKing',
    'black pawn': 'blackPawn1',
    'black pawn': 'blackPawn2',
    'black pawn': 'blackPawn3',
    'black pawn': 'blackPawn4',
    'black pawn': 'blackPawn5',
    'black pawn': 'blackPawn6',
    'black pawn': 'blackPawn7',
    'black pawn': 'blackPawn8',
    'black pawn': 'blackRook1',
    'black pawn': 'blackRook2',
    'black knight': 'blackKnight1',
    'black knight': 'blackKnight2',
    'black bishop': 'blackBishop1',
    'black bishop': 'blackBishop2',
    'black queen': 'blackQueen',
    'black king': 'blackKing'
}

MAC_COMMAND = "afplay"
PI_COMMAND = "aplay"


if platform.system() == 'Darwin':
    PLAYSOUND_COMMAND = MAC_COMMAND
else:
    PLAYSOUND_COMMAND = PI_COMMAND


def play_sound(piece):
    """
    Given a piece spec from chess module, plays that piece's sound.
    """
    path = _sound_for_piece(piece)
    _play_sound_async(path)


def _sound_for_piece(piece_spec):
    """
    Placeholder for real logic, as it comes.
    """
    return '{}/{}{}.wav'.format(PIECE_MAP[piece_spec.piece], ACTIONS_MAP[piece_spec.action], 0)


def _play_sound_async(soundfile):
    t = threading.Thread(target=_play_sound, args=(soundfile,))
    t.start()


def _play_sound(soundfile):
    filepath = os.path.abspath(os.path.join('./', 'assets', soundfile))
    subprocess.call([PLAYSOUND_COMMAND, filepath], stdin=None, stdout=None, stderr=None)
