class BasePiece:
  job = None
  def __init__(self, color):
    self.color = color

  def __str__(self):
    return self.color + "_" + self.job

  def get_moves(self):
    pass


class King(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'king'


class Queen(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'queen'

  
class Knight(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'knight'


class Bishop(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'bishop'


class Rook(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'rook'

class Pawn(BasePiece):
  def __init__(self, color):
    BasePiece.__init__(self, color)
    self.job = 'pawn'


class Move:
  piece = None
  from_loc = None
  to_loc = None  

  def __init__(self, from_loc, to_loc, piece=None):
    self.piece = piece
    self.from_loc = from_loc
    self.to_loc = to_loc  

  def __str__(self):
    return str(self.from_loc) + "_to_" + str(self.to_loc)

class Board:
  def __init__(self):
    self.state = [[Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')],
                  [Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')],
                  [None]*8,
                  [None]*8,
                  [None]*8,
                  [None]*8,
                  [Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')],
                  [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')]]
    self.moves = []
    self.turn = 'white'

  def __str__(self):
    output = ''
    for row in self.state:
      for piece in row:
        output += (str(piece) if piece else '_') + ' '
      output += '\n'
    return output

  def replay_moves(self):
    for move in self.moves:
      exec_move(move)

  def exec_move(self, move):
    moving_piece = self.state[move.from_loc[0]][move.from_loc[1]]
    displaced_piece = self.state[move.to_loc[0]][move.to_loc[1]]
    assert moving_piece
    assert moving_piece.color == self.turn
    self.state[move.to_loc[0]][move.to_loc[1]] = self.state[move.from_loc[0]][move.from_loc[1]]
    self.state[move.from_loc[0]][move.from_loc[1]] = None
    if old_piece:
      print "MURDERED " + str(old_piece)
     
     










