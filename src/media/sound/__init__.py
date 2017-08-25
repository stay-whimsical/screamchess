"""
Code used to play sound specifically. We do this the dumbest way possible:
piping commands to the parent OS shell. We don't want to hold up the rest of
the loop with playing sounds, so we'll do them in a separate Python green
thread, like triple hooligans. Much of the fun of the project is the notion
that VIOLENCE IS FUN when it's chess pieces; we will go Full Meta and commit
violence to software engineering principles while we're here.

(after all, this is Python, hyuk hyuk hyuk)

# Actions datatype

This module exports the `Actions` enumeration, which is every type of action
we have a sound for. These map to filenames we store in `assets`. Callers of
`play_sound` will need to pass one of these to get their sounds to play
correctly.

# Sound Bank

Characters have a variable number of sounds for each action we support, and
we mandate that they have at least one of each kind. In order to make sure we
call one they have, we initialize the program with a Sound Bank, a data
structure that knows how many of each sound each piece has. So it'll know,
for example, that the White Rook 1 has 3 deaths, 2 moves, and 1 kill.

Current logic is to have it pick them randomly.
"""
import os
import platform
import random
import re
import subprocess
import threading

from enum import Enum
# from collections import namedtuple

Actions = Enum('Actions', 'Kill MoveDanger MoveSafety Die Lift Boo Castle')

ACTIONS_MAP = {
    Actions.Kill: 'kill',
    Actions.MoveSafety: 'move_safe',
    Actions.MoveDanger: 'move_danger',
    Actions.Die: 'die',
    Actions.Lift: 'lift',
    Actions.Boo: 'boo',
    Actions.Castle: 'castle'
}


# The map of piecenames in the assets directory. Keys are just placeholders,
# but the values are real.
PIECE_MAP = {
    'white_pawn1': 'whitePawn1',
    'white_pawn2': 'whitePawn2',
    'white_pawn3': 'whitePawn3',
    'white_pawn4': 'whitePawn4',
    'white_pawn5': 'whitePawn5',
    'white_pawn6': 'whitePawn6',
    'white_pawn7': 'whitePawn7',
    'white_pawn8': 'whitePawn8',
    'white_rook1': 'whiteRook1',
    'white_rook2': 'whiteRook2',
    'white_knight1': 'whiteKnight1',
    'white_knight2': 'whiteKnight2',
    'white_bishop1': 'whiteBishop1',
    'white_bishop2': 'whiteBishop2',
    'white_queen': 'whiteQueen',
    'white_king': 'whiteKing',
    'black_pawn1': 'blackPawn1',
    'black_pawn2': 'blackPawn2',
    'black_pawn3': 'blackPawn3',
    'black_pawn4': 'blackPawn4',
    'black_pawn5': 'blackPawn5',
    'black_pawn6': 'blackPawn6',
    'black_pawn7': 'blackPawn7',
    'black_pawn8': 'blackPawn8',
    'black_rook1': 'blackRook1',
    'black_rook2': 'blackRook2',
    'black_knight1': 'blackKnight1',
    'black_knight2': 'blackKnight2',
    'black_bishop1': 'blackBishop1',
    'black_bishop2': 'blackBishop2',
    'black_queen': 'blackQueen',
    'black_king': 'blackKing'
}

MAC_COMMAND = "afplay"
PI_COMMAND = "aplay"


ASSET_BANK = {}


if platform.system() == 'Darwin':
    PLAYSOUND_COMMAND = MAC_COMMAND
else:
    PLAYSOUND_COMMAND = PI_COMMAND


def create_sound_bank():
    """
    Each character has a variable number of sounds for a given action (i.e.
    three move queues, two die cues, one kill). While we don't load the sounds
    themselves, we still investigate the filesystem to collect metadata: namely

    * Piece-by-piece breakdown of how many of which actions it has (so we can select
      them sequentially, or randomly).

    Someday, I'd like to put a text file in the sound directories to have metadata
    like the names of the actors so we can print credits or something.
    """
    for piece_name in PIECE_MAP.itervalues():
        path = _asset_path(piece_name)
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        action_counts = {key: 0 for key in ACTIONS_MAP.itervalues()}
        for f in files:
            for action in ACTIONS_MAP.itervalues():
                if re.match(action, f):
                    curr = action_counts[action]
                    action_counts[action] = curr + 1
        ASSET_BANK[piece_name] = action_counts


def play_sound(piece, action):
    """
    Given a piece and an action, plays the appropriate sound.
    """
    path = _sound_for_piece(piece, action)
    _play_sound_async(path)


def random_action():
    actions = [Actions.Kill, Actions.MoveSafety, Actions.MoveDanger, Actions.Die, Actions.Lift]
    action_index = random.randint(0, len(actions) - 1)
    return actions[action_index]


def _sound_for_piece(piece, action):
    piece_name = PIECE_MAP[piece.hash()]
    action_name = ACTIONS_MAP[action]
    action_index_max = ASSET_BANK[piece_name][action_name]
    action_index = random.randint(0, action_index_max - 1)
    return '{}/{}{}.wav'.format(piece_name, action_name, action_index)


def _play_sound_async(soundfile):
    t = threading.Thread(target=_play_sound, args=(soundfile,))
    t.start()


def _play_sound(soundfile):
    filepath = _asset_path(soundfile)
    subprocess.call([PLAYSOUND_COMMAND, filepath], stdin=None, stdout=None, stderr=None)


def _asset_path(piece_dir):
    return os.path.abspath(os.path.join('./', 'assets', piece_dir))
