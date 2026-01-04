import unittest
import pygame
from adversary import Adversary
from pacman import PacMan
from foodGoal import FoodGoal

class TestAdversary(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.small_tile_size = 100
        self.ghost = Adversary(1, 1, self.small_tile_size, "stationary")
    def tearDown(self):
        pygame.quit()

    def test_initialise(self):
        counter = 0
        while counter != 100:
            maze = [
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", 0, "W", 0, 0, "W", 0, "W"],
            ["W", 0, "W", 0, "W", "W", 0, "W"],
            ["W", 0, 0, 0, "W", "W", 0, "W"],
            ["W", 0, "W", 0, 0, 0, 0, "W"],
            ["W", 0, "W", "W", 0, "W", 0, "W"],
            ["W", 0, 0, "W", 0, 0, 0, "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ]
            food_goal = FoodGoal(self.small_tile_size)
            fgcoords = food_goal.generate_random_position(maze, 1)
            self.ghost.generate_random_position(maze, fgcoords)
            self.assertEqual(maze[self.ghost.y][self.ghost.x], 2)
            counter += 1

    def test_ghost_costs(self):
        maze = [
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", 0, "W", 0, 0, "W", 0, "W"],
        ["W", 0, "W", 0, "W", "W", 0, "W"],
        ["W", 0, 0, 0, "W", "W", 0, "W"],
        ["W", 0, "W", 0, 0, 0, 0, "W"],
        ["W", 0, "W", "W", 0, "W", 0, "W"],
        ["W", 0, 0, "W", 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ]
        food_goal = FoodGoal(self.small_tile_size)
        fgcoords = food_goal.generate_random_position(maze, 1)
        self.ghost.generate_random_position(maze, fgcoords)
        self.assertIn(maze[self.ghost.y - 1][self.ghost.x], [1, "W"])
        self.assertIn(maze[self.ghost.y + 1][self.ghost.x], [1, "W"])
        self.assertIn(maze[self.ghost.y][self.ghost.x - 1], [1, "W"])
        self.assertIn(maze[self.ghost.y][self.ghost.x + 1], [1, "W"])

    def test_remove_ghost(self):
        maze = [
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", 0, "W", 0, 0, "W", 0, "W"],
        ["W", 0, "W", 0, "W", "W", 0, "W"],
        ["W", 0, 0, 0, "W", "W", 0, "W"],
        ["W", 0, "W", 0, 0, 0, 0, "W"],
        ["W", 0, "W", "W", 0, "W", 0, "W"],
        ["W", 0, 0, "W", 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ]
        food_goal = FoodGoal(self.small_tile_size)
        fgcoords = food_goal.generate_random_position(maze, 1)
        self.ghost.generate_random_position(maze, fgcoords)
        self.ghost.clear(maze, self.screen)
        self.assertIn(maze[self.ghost.y][self.ghost.x], [0, "W"])
        self.assertIn(maze[self.ghost.y - 1][self.ghost.x], [0, "W"])
        self.assertIn(maze[self.ghost.y + 1][self.ghost.x], [0, "W"])
        self.assertIn(maze[self.ghost.y][self.ghost.x - 1], [0, "W"])
        self.assertIn(maze[self.ghost.y][self.ghost.x + 1], [0, "W"])


    def test_ghost_random_movement(self):
            maze = [
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ["W", 0, "W", 0, 0, "W", 0, "W"],
            ["W", 0, "W", 0, "W", "W", 0, "W"],
            ["W", 0, 0, 0, "W", "W", 0, "W"],
            ["W", 0, "W", 0, 0, 0, 0, "W"],
            ["W", 0, "W", "W", 0, "W", 0, "W"],
            ["W", 0, 0, "W", 0, 0, 0, "W"],
            ["W", "W", "W", "W", "W", "W", "W", "W"],
            ]
            food_goal = FoodGoal(self.small_tile_size)
            fgcoords = food_goal.generate_random_position(maze, 1)
            maze = self.ghost.generate_random_position(maze, fgcoords)
            old_y = self.ghost.y
            old_x = self.ghost.x
            self.ghost.random_move(self.screen, maze)
            self.assertNotEqual(maze[old_y][old_x], 2)
            self.assertEqual(maze[self.ghost.y][self.ghost.x], 2)

    def test_aStar(self):
        maze = [
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ["W", 0, "W", 0, 0, "W", 0, "W"],
        ["W", 0, "W", 0, "W", "W", 0, "W"],
        ["W", 0, 0, 0, "W", "W", 0, "W"],
        ["W", 0, "W", 0, 0, 0, 0, "W"],
        ["W", 0, "W", "W", 0, "W", 0, "W"],
        ["W", 0, 0, "W", 0, 0, 0, "W"],
        ["W", "W", "W", "W", "W", "W", "W", "W"],
        ]
        ghost = Adversary(1, 1, self.small_tile_size, "stationary")
        pacman = PacMan(1, 1, self.small_tile_size)
        foodgoal = FoodGoal(self.small_tile_size)
        fgcoords = foodgoal.generate_random_position(maze, 1)
        ghost.generate_random_position(maze, fgcoords)

        self.ghost.a_star(maze, (pacman.y, pacman.x), self.screen)

if __name__ == '__main__':
    unittest.main()
