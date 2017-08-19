#!/bin/bash
# It's a pain in the ass to make too many directories, so this makes an entire
# chess set + placeholder files so it's easy to 'git add'.

PIECENAMES=('whitePawn1' 'whitePawn2' 'whitePawn3' 'whitePawn4' 'whitePawn5' 'whitePawn6' 'whitePawn7' 'whitePawn8' 'whiteRook1' 'whiteRook2' 'whiteKnight1' 'whiteKnight2' 'whiteBishop1' 'whiteBishop2' 'whiteQueen' 'whiteKing' 'blackPawn1' 'blackPawn2' 'blackPawn3' 'blackPawn4' 'blackPawn5' 'blackPawn6' 'blackPawn7' 'blackPawn8' 'blackRook1' 'blackRook2' 'blackKnight1' 'blackKnight2' 'blackBishop1' 'blackBishop2' 'blackQueen' 'blackKing');

for i in "${PIECENAMES[@]}"; do
  echo $i
  mkdir $i
  echo "NOT A SOUND\nGit needs a file to add" >> $i/placeholder.txt
done
