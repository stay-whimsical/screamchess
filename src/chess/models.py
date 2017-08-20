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

  def exec_move(self, move):
    moving_piece = self.state[move.from_loc[0]][move.from_loc[1]].piece
    displaced_piece = self.state[move.to_loc[0]][move.to_loc[1]].piece
    assert moving_piece
    assert moving_piece.color == self.turn
    self.state[move.to_loc[0]][move.to_loc[1]].piece = moving_piece
    self.state[move.from_loc[0]][move.from_loc[1]].piece = None
    if displaced_piece:
      print "MURDERED " + str(displaced_piece)
     
     










