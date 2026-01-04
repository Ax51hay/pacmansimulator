import unittest
import pygame
from foodGoal import FoodGoal

class TestFoodGoal(unittest.TestCase):
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
        self.foodGoal = FoodGoal(self.small_tile_size)

    def tearDown(self):
        pygame.quit()

    def test_initialise(self):
        for food_goal in self.foodGoal.goals:
            self.foodGoal.generate_random_position(self.maze, 3)
            for next_goal in self.foodGoal.goals:
                if next_goal != food_goal:
                    self.assertNotEqual((food_goal.x, food_goal.y), (next_goal.x, next_goal.y))

if __name__ == '__main__':
    unittest.main()
