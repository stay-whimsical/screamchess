"""
Module that can parse chess notation for individual moves. Mostly to debug
things and/or introduce chess states without having to wire up the entire
camera setup on a physical board.

Note that we're using standard Algebraic Notation:

https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

Maybe we move on to FEN https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
to start from boards?

BUGS:
  - Doesn't handle pawn promotions
  - Doesn't handle disambiguations (when two knights can reach the same place)
"""
import re
from enum import Enum
from collections import namedtuple


# Data definitions. Currently don't allow for draws.
Piece = Enum('Piece', 'Pawn Rook Knight Bishop Queen King')
Action = Enum('Action', 'Move Capture CastleKingside CastleQueenside PawnPromotion')
Modifier = Enum('Modifier', 'Check CheckMate')

Col = Enum('Col', 'A B C D E F G H')
Row = Enum('Row', 'One Two Three Four Five Six Seven Eight')

Position = namedtuple('Position', 'row col')
Move = namedtuple('Move', 'piece action position modifiers')
# Black could be None in the case of a white Checkmate
Turn = namedtuple('Turn', 'white black')

LINE_REGEX = re.compile('(?:\d+\.\s+)\s*(\S+)(?:\s+(\S+)\s*)?$')
POSITION_PATTERN = '([a-h])(1|2|3|4|5|6|7|8)'
POSITION_REGEX = re.compile(POSITION_PATTERN)
PIECE_MAP = {
    'B': Piece.Bishop,
    'R': Piece.Rook,
    'Q': Piece.Queen,
    'K': Piece.King,
    'N': Piece.Knight
}
COL_MAP = {'a': Col.A, 'b': Col.B, 'c': Col.C, 'd': Col.D, 'e': Col.E, 'f': Col.F, 'g': Col.G, 'h': Col.H}
ROW_MAP = {
    '1': Row.One,
    '2': Row.Two,
    '3': Row.Three,
    '4': Row.Four,
    '5': Row.Five,
    '6': Row.Six,
    '7': Row.Seven,
    '8': Row.Eight
}
ACTION_MAP = {
    'x': Action.Capture,
    'O-O': Action.CastleKingside,
    'O-O-O': Action.CastleQueenside,
    '=': Action.PawnPromotion
}


def parse_file(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [parse_line(line.rstrip('\n')) for line in lines]


def parse_line(line):
    components = LINE_REGEX.match(line)
    white_move = _parse_move(components.group(1))

    black_move = None
    black_move_spec = components.group(2)
    if black_move_spec:
        black_move = _parse_move(black_move_spec)
    return Turn(white=white_move, black=black_move)


def _parse_move(move):
    if re.match('O-O-O', move):
        return Move(piece=None, action=Action.CastleQueenside, position=None, modifiers=[])
    elif re.match('O-O', move):
        return Move(piece=None, action=Action.CastleKingside, position=None, modifiers=[])

    piece = _get_piece(move)
    action = _get_action(move)
    position = _get_position(move)
    modifiers = _get_modifiers(move)
    return Move(piece=piece, action=action, position=position, modifiers=modifiers)


def _get_piece(move):
    """
    The piece is realatively easy to determine: it's either a pawn, or directly
    determined by its first letter. Gets _a little_ weird for when pawns capture,
    so we default to that if the first character isnt' a recognized one.
    """
    match = re.search('^' + POSITION_PATTERN, move)
    if match:
        return Piece.Pawn
    else:
        return PIECE_MAP.get(move[0], Piece.Pawn)


def _get_action(move):
    for action in ACTION_MAP.iterkeys():
        if re.search(action, move):
            return ACTION_MAP[action]
    return Action.Move


def _get_position(move):
    """
    The position is pretty easily determined by one of the "acceptable letters" followed by
    an acceptable number.
    """
    match = POSITION_REGEX.search(move)
    return Position(col=COL_MAP[match.group(1)], row=ROW_MAP[match.group(2)])


def _get_modifiers(move):
    modifiers = []
    if re.search('\+', move):
        modifiers.append(Modifier.Check)
    elif re.search('#', move):
        modifiers.append(Modifier.CheckMate)
    return modifiers


def test_data():
    return [
           Turn(white=Move(piece=Piece.Pawn,
                           action=Action.Move,
                           position=Position(col=Col.E, row=Row.Four),
                           modifiers=[]),
                black=Move(piece=Piece.Pawn,
                           action=Action.Move,
                           position=Position(col=Col.E, row=Row.Five),
                           modifiers=[])),
            ]
