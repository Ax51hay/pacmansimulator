"""
Adversary Class

This manages all adversarial agents that will be created by maze.py.
For each ghost, it has to randomly generate a set of (suitable) coords to be drawn at
And must update and return an internal map in a way where surrounding tiles have an increased cost
Stationary ghosts are static and will not move
Random ghosts will move randomly step by step with no existing goals/targets
Tracker ghosts will use A* to reach the Pac-Man agent in the quickest way possible.
"""

import heapq
import random
import pygame

#The colours used to create the ghosts
light_pink = (255, 182, 193)
orange = (255, 165, 0)
cyan = (0, 255, 255)

class Adversary:

    def __init__(self, x, y, tile_size, type):
        """
        Initializes an Adversarial agent.

        Parameters:
        - x (int): The initial x-coordinate of the adversary.
        - y (int): The initial y-coordinate of the adversary.
        - tile_size (int): The size of the tiles in the selected maze.
        - type (String): Defines the ghost's functions and colour
        """
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.size = tile_size / 4
        self.type = type

        if(type == "tracker"):
            self.colour = light_pink

        elif(type == "random"):
            self.colour = cyan

        elif(type == "stationary"):
            self.colour = orange

    def clear(self, maze, screen):
        """
        Clears an agent from the maze.

        Parameters:
        - maze (2D Array): The current maze internal map.
        - screen: The Pygame screen to draw on.

        Returns: 
        - maze: An updated version of the internal map for the agents without ghost costs
        """
        tile_x = self.x * self.tile_size + self.tile_size // 2
        tile_y = self.y * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, (0, 0, 0), (tile_x, tile_y), self.size)
        return(self.update_ghost_costs(maze, False))

    def generate_random_position(self, maze, goals):
        """
        Randomly generates a suitable position for the agent in the maze.

        Parameters:
        - maze (2D Array): The current maze internal map.
        - goals (tuple): Coordinates of the food goal in the maze.

        Returns:
        - maze: The updated maze/internal map with the adversary agent and increased costs on its surrounding tiles.
        """
        #Iterates over maze
        row, col = self.find_random_free_tile(maze, goals)
        self.x = col
        self.y = row
        #Prints location of ghost in internal map
        print("Ghost Created at", row, col)
        return (self.update_ghost_costs(maze, True))
                        
    def find_random_free_tile(self, maze, goals):
        """
        Finds a random empty tile in the maze where the ghost can be placed.

        Parameters:
        - maze (2D Array): The current maze internal map.
        - goals (tuple): Coordinates of the food goal in the maze.

        Returns:
        - row, col: Coordinates of the empty tile found.
        """
        empty = []
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                if maze[row][col] == 0 and (row, col) not in goals:
                    empty.append((row, col))
        return random.choice(empty)
               
    def update_ghost_costs(self, maze, adding):
        """
        Removes all costs that have been previously invoked by the ghosts

        Parameters:
        - maze (2D Array): The current maze internal map.

        Returns:
        - maze: An updated version of the internal map for the agents without ghost costs
        """
        directions = ["up", "down", "left", "right"]
        #Iterates over tiles surrounding ghost
        for direction in directions:
            x, y = self.x, self.y
            if direction == "up":
                y -= 1
            elif direction == "down":
                y += 1
            elif direction == "left":
                x -= 1
            elif direction == "right":
                x += 1
                #Only update non-wall tiles, but disregards other existing ghosts
            if maze[y][x] not in ("W", 2):
                #Differenttiates between adding and clearing ghost costs
                if adding:
                    maze[self.y][self.x] = 2
                    maze[y][x] = 1
                else:
                    maze[self.y][self.x] = 0
                    maze[y][x] = 0
        return(maze)
    
    def random_move(self, screen, maze):
        """
        Executes one randomly selected possible move, whilst managing the agent's internal map accordingly.

        Parameters:
        - screen: The Pygame screen to draw on.
        - maze (2D Array): The current maze layout.

        Returns:
        - an updated version of the internal map for the agents, after the move has been executed
        """
        moved = False
        directions = ["up", "down", "left", "right"]
        while not moved:
            x, y = self.x, self.y
            #Picks a direction at random
            random_direction = random.choice(directions)
            if random_direction == "up":
                y -= 1
            elif random_direction == "down":
                y += 1
            elif random_direction == "left":
                x -= 1
            elif random_direction == "right":
                x += 1
            #Only executes the move if it is valid
            if maze[y][x] != "W":
                    maze = self.clear(maze, screen)
                    self.x = x
                    self.y = y
                    self.display(screen)
                    moved = True    
        #Adds updated ghost costs to the internal map
        return (self.update_ghost_costs(maze, True))
    
    def a_star(self, maze, goal, screen):
        """
        Allows for the ghost to reach the pacman using AStar

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - goal (tuple): The location of the pacman
        - screen: The Pygame screen to draw on.

        Returns:
        - an updated version of the internal map for the agents
        """
        #Initialises a priority queue
        priority_queue = [(0 + self.heuristic((self.y, self.x), goal), (self.y, self.x), [])]
        visited = set()

        while priority_queue:
            #Removes the move with the lowest cost from the priority queue
            _ , current_position, path = heapq.heappop(priority_queue)

            if current_position == goal:
                #Executes if pacman has been reached/located
                maze = self.update(maze, path + [(current_position[0], current_position[1])], screen)
                return(maze)

            if current_position in visited:
                continue
            
            #Marks as visited
            visited.add(current_position)

            row, col = current_position
            neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]

            for neighbor_row, neighbor_col in neighbors:
                #Checks if neighbouring position is valid to move to 
                if maze[neighbor_row][neighbor_col] != "W":
                    new_coord = (neighbor_row, neighbor_col)
                    #Calculates costs via Manhattan heuristic
                    new_cost = len(path) + self.heuristic(new_coord, goal)
                    # Adds tile with total cost data to priority queue
                    heapq.heappush(priority_queue, (new_cost, new_coord, path + [current_position]))

    def heuristic(self, current, goal):
        """
        Calculates the raw distance that the ghost is to the pacman via a manhattan approach

        Parameters:
        - current (tuple): The agent's current position.
        - goal (tuple): The position of the goal (pacman).

        Returns:
        - Raw distance between two the pacman and ghost
        """
        return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

    def display(self, screen):
        """
        Draws the adversary in the simulation.

        Parameters:
        - screen: The Pygame screen to draw on.
        """
        tile_x = self.x * self.tile_size + self.tile_size // 2
        tile_y = self.y * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, self.colour, (tile_x, tile_y), self.size)

    
    def update(self, maze, path, screen):
        """
        Manages clearing and adding a ghosts costs after it makes a move, as well as displating it on screen

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - path (List) - The calculated path, containing a ghost's next move
        - screen: The Pygame screen to draw on.

        Returns:
        - an updated version of the internal map for the agents, after managing costs
        """
        if len(path) >= 2:
                #Executes next move
                y, x = path[1]
                #Removes old position, and costs
                maze = self.clear(maze, screen)
                self.x = x
                self.y = y
                self.display(screen)
                pygame.display.flip()
                #Adds new costs to the internal map and returns it
                return (self.update_ghost_costs(maze, True))