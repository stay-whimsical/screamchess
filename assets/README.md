# (Back that) Assets (up!)

This contains the assets for Screamchess. We may, someday, do beautiful things
with LEDs, projector screens, or things that aren't sound, but MVP means we're
just sounds for now.

And _within that_, we may have the ability to do things like "sets of sounds"
(i.e. the Halloween screamchess asset library, or the Copyrighted Sounds asset
library, what-have-you) but for now, we just have the flat pair.

**THAT SAID**, if you were so inclined, there's a `directory_maker.sh` to make
sets of them later. For now, we have the default set of the characters flatly
in `assets`

## What goes in a set?

Each set looks a something like this:

* `<color><piece><number>`
  - e.g. `whitePawn1`, `whiteKing`, `blackRook2`
  - This is a directory containing all those character's sounds.

Within those directories:

* `<action><digit>.wav`
  - e.g. `move1.wav` or `die2.wav`
  - This is a .wav file for that sound.

Acceptable names for pieces and actions are in `src/media/sound/__init__.py`,
but (as of this writing are) are:

### Pieces

```
'whitePawn1'
'whitePawn2'
'whitePawn3'
'whitePawn4'
'whitePawn5'
'whitePawn6'
'whitePawn7'
'whitePawn8'
'whiteRook1'
'whiteRook2'
'whiteKnight1'
'whiteKnight2'
'whiteBishop1'
'whiteBishop2'
'whiteQueen'
'whiteKing'
'blackPawn1'
'blackPawn2'
'blackPawn3'
'blackPawn4'
'blackPawn5'
'blackPawn6'
'blackPawn7'
'blackPawn8'
'blackRook1'
'blackRook2'
'blackKnight1'
'blackKnight2'
'blackBishop1'
'blackBishop2'
'blackQueen'
'blackKing'
```

### Actions

```
'kill'   # They kill another piece
'move'   # They move to another part of the board
'die'    # They die
'lift'   # The piece is lifted, not yet set down
'boo'    # They're booing something the player did
```

