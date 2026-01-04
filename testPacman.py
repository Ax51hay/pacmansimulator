import unittest
import pygame
from pacman import PacMan
from adversary import Adversary
from foodGoal import FoodGoal

class TestPacMan(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.small_tile_size = 100
        self.maze = [
    ["W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", 0, "W", 0, 0, "W", 0, "W"],
    ["W", 0, "W", 0, "W", "W", 0, "W"],
    ["W", 0, 0, 0, "W", "W", 0, "W"],
    ["W", 0, "W", 0, 0, 0, 0, "W"],
    ["W", 0, "W", "W", 0, "W", 0, "W"],
    ["W", 0, 0, "W", 0, 0, 0, "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W"],
    ]
        self.pacman = PacMan(1, 1, self.small_tile_size)

    def tearDown(self):
        pygame.quit()

    def test_initialise(self):
        self.assertEqual(self.pacman.x, 1)
        self.assertEqual(self.pacman.y, 1)

    def test_dfs(self):
        foodgoal = (6, 6)

        #DFS always returns a path so this should always work
        self.pacman.dfs(self.maze, foodgoal)

    def test_bfs(self):
        foodgoal = (6, 6)

        #BFS always returns a path so this should always work
        self.pacman.bfs(self.maze, foodgoal)

    def test_ucs(self):
        ghost = Adversary(1, 1, self.small_tile_size, "stationary")
        foodgoal = FoodGoal(self.small_tile_size)
        fgcoords = foodgoal.generate_random_position(self.maze, 1)
        ghost.generate_random_position(self.maze, fgcoords)

        self.pacman.ucs(self.maze, [foodgoal])

    def test_aStar(self):
        ghost = Adversary(1, 1, self.small_tile_size, "stationary")
        foodgoal = FoodGoal(self.small_tile_size)
        fgcoords = foodgoal.generate_random_position(self.maze, 1)
        fgcoords = fgcoords[0]
        ghost.generate_random_position(self.maze, [foodgoal])

        self.pacman.a_star(self.maze, fgcoords)

    def test_reset(self):
        foodgoal = (6, 6)
        self.pacman.dfs(self.maze, foodgoal)
        self.pacman.reset(self.screen)
        self.assertEqual(self.pacman.x, 1)
        self.assertEqual(self.pacman.y, 1)

    def test_update(self):
        new_pos = (1,3)
        self.pacman.update(self.screen, new_pos, False)
        self.assertEqual((self.pacman.y, self.pacman.x), new_pos)

    def test_game_end(self):
        ghost = Adversary(6, 1, self.small_tile_size, "stationary")
        foodgoal = FoodGoal(self.small_tile_size)
        foodgoal.y = 6
        foodgoal.x = 6
        ended = self.pacman.game_end((self.pacman.y, self.pacman.x), [ghost], (foodgoal.y, foodgoal.x))
        self.assertFalse(ended)

        self.pacman.y = 6
        self.pacman.x = 6

        ended = self.pacman.game_end((self.pacman.y, self.pacman.x), [ghost], (foodgoal.y, foodgoal.x))
        self.assertTrue(ended)

        self.pacman.y = 1
        self.pacman.x = 1

        ended = self.pacman.game_end((self.pacman.y, self.pacman.x), [ghost], (foodgoal.y, foodgoal.x))
        self.assertFalse(ended)

        ghost.x = 1
        ghost.y = 1

        ended = self.pacman.game_end((self.pacman.y, self.pacman.x), [ghost], (foodgoal.y, foodgoal.x))
        self.assertTrue(ended)

    def test_detect_avoid(self):
        ghost = Adversary(1, 1, self.small_tile_size, "stationary")
        foodgoal = FoodGoal(self.small_tile_size)
        fgcoords = foodgoal.generate_random_position(self.maze, 1)
        fgcoords = fgcoords[0]
        self.maze = [
        ["W", "W", "W", "W", "W"],
        ["W", 0, 0, 0, "W"],
        ["W", 0, 0, 0, "W"],
        ["W", 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W"],
        ]
        ghost_positions = [(2,1), (1,2), (2,3), (3,2)]
        for pos in ghost_positions:
        
            self.x = 2
            self.y = 2
            ghost.y, ghost.x = pos
            self.pacman.detect(self.maze, fgcoords, self.screen)
            self.assertNotEqual((self.pacman.y, self.pacman.x), (2,2))
            self.assertNotEqual((self.pacman.y, self.pacman.x), pos)

    def test_get_moves(self):
        self.maze = [
        ["W", "W", "W", "W", "W"],
        ["W", 0, 0, 0, "W"],
        ["W", 0, 0, 0, "W"],
        ["W", 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W"],
        ]

        self.x = 2
        self.y = 2
        suitable = self.pacman.get_moves((self.y, self.x), self.maze, None)
        self.assertEqual(suitable, [(1,2), (3,2), (2,1), (2,3)])

        self.x = 3
        self.y = 1
        suitable = self.pacman.get_moves((self.y, self.x), self.maze, None)
        self.assertEqual(suitable, [(2,3), (1,2)])

        self.x = 1
        self.y = 3
        suitable = self.pacman.get_moves((self.y, self.x), self.maze, None)
        self.assertEqual(suitable, [(2,1), (3,2)])

    def test_eval_pos(self):
        self.maze = [
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", 0, 0, 0, 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ]
        foodgoal = FoodGoal(self.small_tile_size)
        foodgoal.y = 1
        foodgoal.x = 3
        ghost = Adversary(1, 1, self.small_tile_size, "stationary")
        utility = self.pacman.eval_pos_pacman((self.pacman.y,self.pacman.x), (foodgoal.y, foodgoal.x), [ghost])
        self.assertEqual(str(utility), '-inf')
        self.pacman.y = 7
        self.pacman.x = 6
        utility = self.pacman.eval_pos_pacman((self.pacman.y,self.pacman.x), (foodgoal.y, foodgoal.x), [ghost])
        self.assertEqual(utility, -9)

if __name__ == '__main__':
    unittest.main()