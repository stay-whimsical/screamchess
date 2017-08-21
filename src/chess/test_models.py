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

if __name__ == '__main__':
  unittest.main()
