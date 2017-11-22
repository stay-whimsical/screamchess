# Actions we need to support/detect for debugging.

### Camera only

* Set calibration for colors on current camera/lighting setup.
* Detect when a piece is lifted.
* Detect when a piece is put down after a lift (or, alternatively, that all the
  pieces are on the board at the same time).

### Chess-no-camera

* Advance the state of the game.
  - Play appropriate sound
  - Add to a game's history
* History
  - Go back to last game state, forward.
    - View/print history of a game.
  - History of sound effects were played.
  - Ideally, as much as possible of this experience can be played back with what
  	we've logged/recorded (this can help us find patterns to avoid
  	staleness/repetition).
* Reset to start of game.
* Assign "characters" to the various pieces, ideally in a way that is easily
  changeable/configurable (i.e. a YAML file with a naming convention on mp4s on
  a directory or somesuch, not in Python code)

### All together now

* Take current camera image and estimate the current model of chess game.

* Detecting when a move has been completed from camera changes, output a new
  model of the game.
