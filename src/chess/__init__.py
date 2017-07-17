"""
All the chess-related logic: boards, pieces, history, events. This has no real
dependencies of its own.

This is KAREN TERRITORY. NO PABLO'S ALLOWED! My feelings will NOT be hurt if
you change everything here.
"""

from enum import Enum
from collections import namedtuple

Color = Enum('Colors', 'Black White')

PieceType = Enum('PieceTypes', 'King Queen Bishop Knight Rook Pawn')

Piece = namedtuple('Piece', 'color type')

ChessGame = namedtuple('ChessGame', 'board players curr_turn history')


def fresh_game():
    return ChessGame(
            board=[
                [Piece(color=Color.Black, type=PieceType.Rook),
                 Piece(color=Color.Black, type=PieceType.Knight),
                 Piece(color=Color.Black, type=PieceType.Bishop),
                 Piece(color=Color.Black, type=PieceType.Queen),
                 Piece(color=Color.Black, type=PieceType.Rook),
                 Piece(color=Color.Black, type=PieceType.Bishop),
                 Piece(color=Color.Black, type=PieceType.Knight),
                 Piece(color=Color.Black, type=PieceType.Rook)],

                [Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn),
                 Piece(color=Color.Black, type=PieceType.Pawn)],
                [],
                [],
                [],
                [],
                [Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn),
                 Piece(color=Color.White, type=PieceType.Pawn)],

                [Piece(color=Color.White, type=PieceType.Rook),
                 Piece(color=Color.White, type=PieceType.Knight),
                 Piece(color=Color.White, type=PieceType.Bishop),
                 Piece(color=Color.White, type=PieceType.Queen),
                 Piece(color=Color.White, type=PieceType.Rook),
                 Piece(color=Color.White, type=PieceType.Bishop),
                 Piece(color=Color.White, type=PieceType.Knight),
                 Piece(color=Color.White, type=PieceType.Rook)]
                ],
            players=['Karen', 'Pablo'],
            curr_turn='Karen',
            history=[])
