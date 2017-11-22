#!/bin/bash
# Rather than copy a bunch of sounds, we can simulate having all piece sound assets by
# linking to the one I already made. We make sounds fo

BASEPIECE='whiteBishop2'

# Specifically excludes whiteKing. If you change BASEPIECE, sub it back in
PIECENAMES=('whitePawn2' 'whitePawn3' 'whitePawn6' 'whitePawn7' 'whitePawn8' 'blackRook1' 'blackQueen' 'blackKing' 'blackBishop2' 'blackRook2' 'blackPawn1' 'blackPawn2' 'blackPawn3' 'blackPawn6' 'blackPawn7' 'blackPawn8');


for i in "${PIECENAMES[@]}"; do
  rm -f $i/*.wav

  ln $BASEPIECE/move_safe0.wav $i/move_safe0.wav
  ln $BASEPIECE/move_danger0.wav $i/move_danger0.wav
  ln $BASEPIECE/kill0.wav $i/kill0.wav
  ln $BASEPIECE/kill1.wav $i/kill1.wav
  ln $BASEPIECE/lift0.wav $i/lift0.wav
  ln $BASEPIECE/die0.wav $i/die0.wav
  rm -f $i/placeholder.txt
done
