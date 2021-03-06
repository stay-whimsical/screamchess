import unittest
from models import *
import time


class TestMoves(unittest.TestCase):
  def test_white_move(self):
    b = Board()
    self.assertEqual(b.turn, 'white')
    b.exec_move(Move((1,0), (2,0)))
    self.assertEqual(str(b.state[2][0].piece), 'white_pawn')
    self.assertEqual(b.turn, 'black')

  def test_black_move(self):
    b = Board()
    self.assertEqual(b.turn, 'white')
    b.exec_move(Move((1,0), (2,0)))
    self.assertEqual(b.turn, 'black')
    b.exec_move(Move((6,0), (5,0)))
    self.assertEqual(str(b.state[5][0].piece), 'black_pawn')
    self.assertEqual(b.turn, 'white')

  def test_wrong_turn_move(self):
    b = Board()
    self.assertEqual(b.turn, 'white')
    with self.assertRaises(AssertionError):
      b.exec_move(Move((6,0), (5,0)))
    self.assertIsNone(b.state[5][0].piece)
    self.assertEqual(b.turn, 'white')

  def test_illegal_move(self):
    b = Board()
    self.assertEqual(b.turn, 'white')
    with self.assertRaises(AssertionError):
      b.exec_move(Move((1,0), (2,1)))
    self.assertIsNone(b.state[2][1].piece)
    self.assertEqual(b.turn, 'white')

  def test_king(self):
    b = Board()
    king = b.state[0][4].piece
    self.assertEqual(set(), king.threatened_spaces((0, 4), b.state))

  def test_knight(self):
    b = Board()
    knight = b.state[0][1].piece
    self.assertEqual({(2,0), (2, 2)}, knight.threatened_spaces((0, 1), b.state))

  def test_white_pawn(self):
    b = Board()
    pawn = b.state[1][0].piece
    self.assertEqual({(3, 0), (2, 0)}, pawn.threatened_spaces((1, 0), b.state))
  
  def test_black_pawn(self):
    b = Board()
    b.exec_move(Move((1,1), (5,1)), force=True)
    pawn = b.state[6][2].piece
    self.assertEqual({(4, 2), (5, 2), (5, 1)}, pawn.threatened_spaces((6, 2), b.state))

  def test_rook(self):
    b = Board()
    rook = b.state[0][0].piece
    self.assertEqual(set(), rook.threatened_spaces((0, 0), b.state))
    b.state[5][0].piece = b.state[7][0].piece
    b.state[7][0].piece = None
    rook = b.state[5][0].piece
    self.assertEqual({(5, 4), (5, 5), (2, 0), (5, 6), (5, 7), (3, 0), (5, 1), (1, 0), (4, 0), (5, 2), (5, 3)}, rook.threatened_spaces((5, 0), b.state))

  def test_bishop(self):
    b = Board()
    bishop = b.state[0][2].piece
    self.assertEqual(set(), bishop.threatened_spaces((0, 2), b.state))
    b.state[3][2].piece =  b.state[0][2].piece
    bishop = b.state[3][2].piece
    self.assertEqual(set({(5, 4), (4, 3), (2, 1), (2, 3), (5, 0), (4, 1), (6, 5)}), bishop.threatened_spaces((3, 2), b.state))

 

if __name__ == '__main__':
  unittest.main()
