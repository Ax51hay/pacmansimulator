"""
Food Goal Class

This manages when an end goal point is created by maze.py.
It has to randomly generate a set of (suitable) coords fir the goal to be set to and drawn at
"""

import pygame
import random

white = (255, 255, 255)

class FoodGoal:

    def __init__(self, tile_size):
        """
        Initializes an End Goal.

        Parameters:
        - x (int): The initial x-coordinate of the goal.
        - y (int): The initial y-coordinate of the goal.
        - tile_size (int): The size of the tiles in the selected maze.
        """
        self.goals = []
        self.tile_size = tile_size
        self.size = tile_size/4

    def generate_random_position(self, maze, amount):
        """
        Randomly generates a suitable position for the end goal in the maze.

        Parameters:
        - maze (2D Array): The current maze layout.

        Returns:
        - row, col (tuple): The coords of the end goal.
        """
        for _ in range(amount):
            goal_made = False
            while not goal_made:
                row = random.randint(0, len(maze) - 1)
                col = random.randint(0, len(maze[0]) - 1)
                if maze[row][col] == 0 and row not in (1,2) and col not in (1,2) and (row,col) not in self.goals and (row - 1,col) not in self.goals and (row,col - 1) not in self.goals and (row + 1,col) not in self.goals and (row,col + 1) not in self.goals:
                    self.goals.append((row, col))
                    goal_made = True
        return(self.goals)

    def create(self, screen):
        """
        Draws the end goal in the simulation.

        Parameters:
        - screen: The Pygame screen to draw on.
        """
        for goal in self.goals:
            tile_x = goal[1] * self.tile_size + self.tile_size // 2
            tile_y = goal[0] * self.tile_size + self.tile_size // 2
            pygame.draw.rect(screen, white, (tile_x - self.size/2, tile_y - self.size/2, self.size, self.size))
