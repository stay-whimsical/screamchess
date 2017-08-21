class BasePiece:
  job = None
  def __init__(self, color):
    self.color = color

  def __str__(self):
    return self.color + "_" + self.job

  def get_moves(self):
    pass

  def is_legal(self, move, state):
    pass

class King(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'king'

  def is_legal(self, move, state):
    # A king move is legal if it has moved at most one space in any direction (and has moved)
    # The king's moves are legal regardless of other pieces' locations.
    row_diff = abs(move.from_loc[0] - move.to_loc[0])
    col_diff = abs(move.from_loc[1] - move.to_loc[1])
    return col_diff < 2 and row_diff < 2 and (row_diff + col_diff) > 0

class Queen(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'queen'

  def is_legal(self, move, state):
    return True

  
class Knight(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'knight'

  def is_legal(self, move, state):
    # A knight moves 1 step in one direction and 2 in another.
    # The knight's moves are legal regardless of other pieces' locations.
    row_diff = abs(move.from_loc[0] - move.to_loc[0])
    col_diff = abs(move.from_loc[1] - move.to_loc[1])
    return (col_diff == 1 and row_diff == 2)  or (row_diff == 1 and col_diff == 2)   


class Bishop(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'bishop'

  def is_legal(self, move, state):
    return True


class Rook(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'rook'

  def is_legal(self, move, state):
    return True


class Pawn(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'pawn'

  def is_legal(self, move, state):
    # A pawn moves forward only, captures diagonally and moves 1 at a time except for the first move.
    row = move.from_loc[0]
    col = move.from_loc[1]
    moving_piece = state[move.from_loc[0]][move.from_loc[1]].piece
    displaced_piece = state[move.to_loc[0]][move.to_loc[1]].piece
    row_offset = 1 if moving_piece.color == 'white' else -1
    if displaced_piece:
      print "MURDER"
      # Pawns capture diagonally
      return (move.to_loc[0] == row + row_offset) and abs(move.to_loc[1] - col) == 1
    return move.to_loc[0] == row + row_offset and move.to_loc[1] == col

class Move:
  from_loc = None
  to_loc = None  

  def __init__(self, from_loc, to_loc):
    self.from_loc = from_loc
    self.to_loc = to_loc  

  def __str__(self):
    return str(self.from_loc) + "_to_" + str(self.to_loc)


class Space:
  def __init__(self, piece=None):
     self.piece = piece 
     self.danger_from_white = False
     self.danger_from_black = False
 
  def __str__(self):
    output = str(self.piece) if self.piece else '_'
    output += 'whitethreat' if str(self.danger_from_white) else ''
    output += 'blackthreat' if str(self.danger_from_black) else ''
    return output 

class Board:
  def __init__(self):
    # The indices are:  [[(0,0), (0,1), ... (0,7)],
    #                    [(1,0) (1,1) ... (1,7)],
    #                           ....
    #                    [(7,0), (7,1) ... (7,7)]]
    self.state = [[]]
    for row in [[Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')],
                [Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')],
                [None]*8,
                [None]*8,
                [None]*8,
                [None]*8,
                [Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')],
                [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]]:
      for piece in row:
        if len(self.state[-1]) == 8:
          self.state.append([])
        self.state[-1].append(Space(piece))
    
    self.moves = []
    self.turn = 'white'

  def __str__(self):
    output = ''
    for row in self.state:
      for space in row:
        output += (str(space.piece) if space.piece else '_') + ' '
      output += '\n'
    return output

  def replay_moves(self):
    for move in self.moves:
      exec_move(move)

  def update_turn(self):
    self.turn = 'white' if self.turn == 'black' else 'black'

  def exec_move(self, move):
    moving_piece = self.state[move.from_loc[0]][move.from_loc[1]].piece
    assert moving_piece
    assert moving_piece.color == self.turn
    assert moving_piece.is_legal(move, self.state)
    displaced_piece = self.state[move.to_loc[0]][move.to_loc[1]].piece
    self.state[move.to_loc[0]][move.to_loc[1]].piece = moving_piece
    self.state[move.from_loc[0]][move.from_loc[1]].piece = None
    if displaced_piece:
      print "MURDERED " + str(displaced_piece)
    self.update_turn()
     
     










