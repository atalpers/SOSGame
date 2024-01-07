import unittest
from unittest.mock import patch
from GameLogic import *

class TestComputerPlayer(unittest.TestCase):

    def setUp(self):
        self.game = SOSGame(3)

    def test_computer_move_on_empty_board(self):
        with patch('random.choice', side_effect=lambda x: x[0]):
            move = self.game.computer_move()
            self.assertIsNotNone(move)
            self.assertIn(move, [(i, j) for i in range(3) for j in range(3)])
            self.assertIn(self.game.board[move[0]][move[1]], [1, 2])

    def test_computer_move_on_partially_filled_board(self):
        self.game.board = [[1, 0, 0], [0, 2, 0], [0, 0, 0]]
        with patch('random.choice', side_effect=lambda x: x[0]):
            move = self.game.computer_move()
            self.assertIsNotNone(move)
            self.assertNotEqual(move, (0, 0))
            self.assertNotEqual(move, (1, 1))
            self.assertIn(self.game.board[move[0]][move[1]], [1, 2])

    def test_computer_move_on_full_board(self):
        self.game.board = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]
        move = self.game.computer_move()
        self.assertIsNone(move)