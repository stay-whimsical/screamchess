#!/bin/bash
# Rather than copy a bunch of sounds, we can simulate having all piece sound assets by
# linking to the one I already made. We make sounds fo

BASEPIECE='whiteKing'

# Specifically excludes whiteKing. If you change BASEPIECE, sub it back in
PIECENAMES=('whitePawn1' 'whitePawn2' 'whitePawn3' 'whitePawn4' 'whitePawn5' 'whitePawn6' 'whitePawn7' 'whitePawn8' 'whiteRook1' 'whiteRook2' 'whiteKnight1' 'whiteKnight2' 'whiteBishop1' 'whiteBishop2' 'whiteQueen' 'blackPawn1' 'blackPawn2' 'blackPawn3' 'blackPawn4' 'blackPawn5' 'blackPawn6' 'blackPawn7' 'blackPawn8' 'blackRook1' 'blackRook2' 'blackKnight1' 'blackKnight2' 'blackBishop1' 'blackBishop2' 'blackQueen' 'blackKing');

for i in "${PIECENAMES[@]}"; do
  rm -f $i/move0.wav
  rm -f $i/move1.wav
  rm -f $i/kill0.wav
  rm -f $i/kill1.wav
  rm -f $i/lift0.wav
  rm -f $i/all_i_see_is_blood.wav
  rm -f $i/placeholder.txt

  ln $BASEPIECE/move0.wav $i/move0.wav
  ln $BASEPIECE/move1.wav $i/move1.wav
  ln $BASEPIECE/kill0.wav $i/kill0.wav
  ln $BASEPIECE/kill1.wav $i/kill1.wav
  ln $BASEPIECE/lift0.wav $i/lift0.wav
  ln $BASEPIECE/all_i_see_is_blood.wav $i/die0.wav
  rm -f $i/placeholder.txt
done
