"""
Pacman Agent Class

This manages the main pacman agent, that will be created by maze.py.
It includes the maintenance of the agent priority of food goals, as well as all of the algorithms used (DFS, BFS, UCS, A*, Reflex Agent, Minimax, AB Pruning)
"""

import heapq
import pygame
import random

#The only colour needed by the Pac-Man
yellow = (255, 255, 0)

class PacMan:

    def __init__(self, x, y, tile_size):
        """
        Initializes a Pac-Man agent.

        Parameters:
        - x (int): The initial x-coordinate of the pacman.
        - y (int): The initial y-coordinate of the pacman.
        - tile_size (int): The size of the tiles in the selected maze.
        """
        self.x = x
        self.y = y
        #Adjusts the size of the agent to fit within the maze
        self.size = tile_size / 4
        self.tile_size = tile_size
        self.moving = False

    def draw(self, screen):
        """
        Draws the pacman into the simulation.

        Parameters:
        - screen: The Pygame screen to draw on.
        """
        tile_x = self.x * self.tile_size + self.tile_size // 2
        tile_y = self.y * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, yellow, (tile_x, tile_y), self.size)
        pygame.draw.polygon(screen, (0, 0, 0), [(tile_x, tile_y), (tile_x + self.size, tile_y - self.size // 2),
                                                    (tile_x + self.size, tile_y + self.size // 2)])

    def reset(self, screen):
        """
        Resets the pacman's position to (1,1).

        Parameters:
        - screen: The Pygame screen to draw on.
        """
        self.x = 1
        self.y = 1
        self.draw(screen)
        pygame.display.flip()

    def clear(self, screen):
        """
        Clears the pacman from the simulation.

        Parameters:
        - screen: The Pygame screen to cleared from.
        """
        tile_x = self.x * self.tile_size + self.tile_size // 2
        tile_y = self.y * self.tile_size + self.tile_size // 2
        pygame.draw.circle(screen, (0, 0, 0), (tile_x, tile_y), self.size)

    def update(self, screen, move, temporary):
        """
        Executes the given move and updates the Pac-Man accordingly

        Parameters:
        - screen: The Pygame screen to cleared from.
        - move (tuple): The tile that the agent will move to
        - temporary (bool): Whether a move is made just for a calculation or is an actual execution
        
        Returns:
        - Pacman's updated position
        """
        if not temporary:
            self.clear(screen)
            self.y = move[0]
            self.x = move[1]
            self.draw(screen)
            pygame.display.flip()
        return[move[0], move[1]]
    
    def get_moves(self, pos, maze, avoiding):
        """
        Calculates all executable moves from a given loaction

        Parameters:
        - pos (tuple): The position to be used
        - maze (2D Array): The selected maze in the simulation.
        
        Returns:
        - All possible moves from given position
        """
        suitable = []
        directions = ["up", "down", "left", "right"]

        if(avoiding == "above"):
            directions.remove("up")
        elif(avoiding == "below"):
            directions.remove("down")
        elif(avoiding == "left"):
            directions.remove("left")
        elif(avoiding == "right"):
            directions.remove("right")

        for direction in directions:
            y,x = pos[0], pos[1]
            if direction == "up":
                y -= 1
            elif direction == "down":
                y += 1
            elif direction == "left":
                x -= 1
            elif direction == "right":
                x += 1
            #Only adds the move if it is not a wall tile
            if maze[y][x] != "W":
                suitable.append((y,x))
        return suitable

    def move(self, direction, maze, screen):
        """
        Allows for the pacman agent to be manually controlled via arrow keys

        Parameters:
        - direction (String): The direction the user wishes the pacman to travel in
        - maze (2D Array): The selected maze in the simulation
        - screen: The Pygame screen to updated.
        """
        if not self.moving:
            #Updates coords
            new_x, new_y = self.x, self.y
        
            #Calculates new coords
            if direction == "up":
                new_y -= 1
            elif direction == "down":
                new_y += 1
            elif direction == "left":
                new_x -= 1
            elif direction == "right":
                new_x += 1
            
            #Ensures pacman cannot move outside of maze paths
            if maze[new_y][new_x] != "W":
                    self.update(screen, (new_y, new_x), False)
                    self.moving = True

    """
        Given a list of goals, returns them sorted out by how close they are to the pacman in its current position

        Parameters:
        - goals (list of tuples): The remaining goals to be eaten
        - maze (2D Array): The selected maze in the simulation

        Returns:
        - sorted_goals - The sorted list, ready for the first goal to be prioritised by the Pac-Man
        """
    def goal_sorter(self, goals, maze):
        sorted_goals  = []
        for goal in goals:
            #Calculates Manhattan distance
            distance = self.heuristic((self.y,self.x), goal, maze)
            sorted_goals.append((goal, distance))
        #Sorts via priority 
        sorted_goals.sort(key=lambda x: x[1])
        sorted_goals = [goal[0] for goal in sorted_goals]

        return sorted_goals


    def dfs(self, maze, goal):
        """
        Allows for the pacman to reach an end goal using Depth First Search

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - goal (tuple): The location of the food goal

        Returns:
        - the path to be executed
        """
        #Creates a copy of the maze in the simulation to be edited
        new_maze = [row[:] for row in maze]
        rows, cols = len(new_maze), len(new_maze[0])
        #Initialises a stack with current start position
        stack = [(self.y, self.x, [])]  # (row, col, path)

        #Explores entire path LIFO
        while stack:
            row, col, path = stack.pop()

            #Ends once goal has been reached
            if (row, col) == goal:
                path.append(goal)
                #Returns path
                return path[1:]

            if 0 <= row < rows and 0 <= col < cols and new_maze[row][col] == 0:
                new_maze[row][col] = "V"  # Mark the current tile as visited

            # Explores neighbors in the order: up, right, down, left
                neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
                for neighbor_row, neighbor_col in neighbors:
                    #If neighbouring tile is not a wall, adds to stack
                    if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and new_maze[neighbor_row][neighbor_col] == 0:
                        stack.append((neighbor_row, neighbor_col, path + [(row, col)]))


    def bfs(self, maze, goal):
        """
        Allows for the pacman to reach an end goal using Breadth First Search

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - goal (tuple): The location of the food goal
        
        Returns:
        - the path to be executed
        """
        #Creates a copy of the maze in the simulation to be edited
        new_maze = [row[:] for row in maze]
        rows, cols = len(new_maze), len(new_maze[0])
        #Initialises a queue with current start position
        queue = [(self.y, self.x, [])]

        while queue:
            #FIFO
            row, col, path = queue.pop(0)
            #Ends once goal has been reached
            if (row, col) == goal:
                path.append(goal)
                #Returns path
                return path[1:]

            if 0 <= row < rows and 0 <= col < cols and new_maze[row][col] == 0:
                new_maze[row][col] = "V" # Mark the current tile as visited

                # Explores neighbors in the order: up, right, down, left
                neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
                for neighbor_row, neighbor_col in neighbors:
                    #If neighbouring tile is not a wall, adds to queue
                    if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and new_maze[neighbor_row][neighbor_col] == 0:
                        queue.append((neighbor_row, neighbor_col, path + [(row, col)]))

    def ucs(self, maze, goal):
        """
        Allows for the pacman to reach an end goal using Uniform Cost Search

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - goal (tuple): The location of the food goal
        
        Returns:
        - the path to be executed
        """
        #Creates a copy of the maze in the simulation to be used
        new_maze = [row[:] for row in maze]
        # Initialize the priority queue with starting position
        priority_queue = [(0, (self.y,self.x), [])]
        # Keeps track of visited tiles
        visited = set()

        while priority_queue:
            # Prioritises smallest costs
            cost, current_position, path = heapq.heappop(priority_queue)

            if current_position == goal:
                path.append(goal)
                #Returns path
                return path[1:]

            #Skips tiles that have already been visited
            if current_position in visited:
                continue

            visited.add(current_position)

            row, col = current_position
            neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]

            for neighbor_row, neighbor_col in neighbors:
                if (new_maze[neighbor_row][neighbor_col] != "W"):
                    #Calculates cost based on internal map
                    new_coord = (neighbor_row, neighbor_col)
                    new_cost = cost + new_maze[neighbor_row][neighbor_col]
                    # Adds tile with cost data to priority queue
                    heapq.heappush(priority_queue, (new_cost, new_coord, path + [current_position]))


    def a_star(self, maze, goal):
        """
        Allows for the pacman to reach an end goal using A*

        Parameters:
        - maze (2D Array): The selected maze in the simulation
        - goal (tuple): The location of the food goal
        
        Returns:
        - the path to be executed
        """
        #Creates a copy of the maze in the simulation to be used
        new_maze = [row[:] for row in maze]
        #Initialises a priority queue, using the heuristic function
        priority_queue = [(0 + self.heuristic((self.y, self.x), goal, maze), (self.y, self.x), [])]
        visited = set()

        while priority_queue:
            # Prioritises smallest costs
            _ , current_position, path = heapq.heappop(priority_queue)

            if current_position == goal:
                path.append(goal)
                #Returns path
                return path[1:]

            #Skips previously visited tiles
            if current_position in visited:
                continue

            visited.add(current_position)

            row, col = current_position
            neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]

            for neighbor_row, neighbor_col in neighbors:
                if new_maze[neighbor_row][neighbor_col] != "W":
                    #Calculates cost based on internal map and Manhattan heuristic
                    new_coord = (neighbor_row, neighbor_col)
                    new_cost = len(path) + self.heuristic(new_coord, goal, maze)
                    # Adds tile with total cost data to priority queue
                    heapq.heappush(priority_queue, (new_cost, new_coord, path + [current_position]))

    def heuristic(self, current, goal, maze):
        """
        Calculates the raw distance that the pacman is to the goal via a manhattan approach

        Parameters:
        - current (tuple): The agent's current position.
        - goal (tuple): The position of the food goal.
        - maze (list): The selected maze

        Returns:
        - Raw distance between two given points
        """
        #Disregards ghost tiles completely as there is no way past them
        if maze[current[0]][current[1]] == 2:
            return 100 * (abs(current[0] - goal[0]) + abs(current[1] - goal[1]))
        #Adds a higher cost charge for dangerous tiles
        elif maze[current[0]][current[1]] == 1:
            return 5 * (abs(current[0] - goal[0]) + abs(current[1] - goal[1]))
        return (abs(current[0] - goal[0]) + abs(current[1] - goal[1]))
    
    def detect(self, maze, goal, screen):
        """
        Checks to see if a ghost is near to the agent and will call avoid appropriately.

        Parameters:
        - maze (2D Array): The selected maze in the simulation.
        - goal (tuple): The location of the current food goal
        - screen: The Pygame screen to draw on.
        """

        if(maze[self.y - 1][self.x] in (1, 2)):
            return self.avoid(maze, "above", goal, screen)

        if(maze[self.y + 1][self.x] in (1, 2)):
            return self.avoid(maze, "below", goal, screen)

        if(maze[self.y][self.x + 1] in (1, 2)):
            return self.avoid(maze, "right", goal, screen)

        if(maze[self.y][self.x - 1] in (1, 2)):
            return self.avoid(maze, "left", goal, screen)

    def avoid(self, maze, avoiding, goal, screen):
        """
        Executes a step that will ensure that the agent moves away from the adversary, whilst still prioritising getting closer to the goal.

        Parameters:
        - maze (2D Array): The selected maze in the simulation.
        - avoiding (String): Shows which direction the ghost is approaching in
        - goal (tuple): the location of the food goal
        - screen: The Pygame screen to draw on.
        """
        valid_moves = self.get_moves((self.y, self.x), maze, avoiding)
        if not valid_moves:
            return False
    
        best_moves = self.get_best_moves(valid_moves, goal, maze)

        x, y = self.x, self.y
        rand_best_move = random.choice(best_moves)
        
        if rand_best_move == "up":
            y -= 1
        elif rand_best_move == "down":
            y += 1
        elif rand_best_move == "left":
            x -= 1
        elif rand_best_move == "right":
            x += 1

        self.update(screen, (y,x), False)

    def get_best_moves(self, valid_moves, goal, maze):
        """
        Get the best moves based on their Manhattan distance to the goal.

        Parameters:
        - valid_moves (List): List of valid moves considering the direction to avoid.
        - goal (tuple): the location of the food goal
        - maze (2D Array): The selected maze in the simulation.

        Returns:
        - best_moves (List): List of best moves based on their Manhattan distance to the goal.
        """
        best_moves = []
        best_distance = float('inf')
        for move in valid_moves:
            y, x = move[0], move[1]
            goal_distance = self.heuristic((y, x), goal, maze)
            if goal_distance < best_distance:
                best_moves = [(y, x)]
                best_distance = goal_distance
            elif goal_distance == best_distance:
                best_moves.append((y, x))
        return best_moves

    def eval_pos_pacman(self, pos, goal, ghosts):
        """
        Calculates the utility of a location, used for minimax

        Parameters:
        - pos (tuple): The position to be evaluated
        - goal (tuple): The location of the food goal
        - ghosts (List of Adversaries): The ghosts within the simulation
        
        Returns:
        - The utility of the given position
        """
        goal_distance = (abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))
        for ghost in ghosts:
            ghost_distance = (abs(pos[0] - ghost.y) + abs(pos[1] - ghost.x))
            #Completely avoid going in the same tile as a ghost
            if ghost_distance in (1,0):
                return float('-inf')
        return -goal_distance
    
    def game_end(self, pos, ghosts, goal):
        """
        Decides whether minimax should be terminated

        Parameters:
        - pos (tuple): The position to be evaluated
        - ghosts (List of Adversaries): The ghosts within the simulation
        - goal (tuple): The location of the food goal
        
        Returns:
        - Boolean specifying if the game/simulation has ended
        """
        for ghost in ghosts:
            if((pos[0], pos[1]) == (ghost.y, ghost.x)):
                return True
        if((pos[0], pos[1]) == (goal[0], goal[1])):
            return True
        return False
    
    def max_value(self, pos, ghosts, goal, screen, depth, maze):
        """
        Maximizes the value of Pac-Man's moves in the minimax algorithm.

        Parameters:
        - pos (tuple): The current position being evaluated.
        - ghosts (List of Adversaries): The ghosts within the simulation.
        - goal (tuple): The location of the food goal.
        - screen: The Pygame screen to update.
        - depth (int): The current depth in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
    
        Returns:
        - The maximum utility value of the Pac-Man's moves.
        """
        #Base case
        if self.game_end(pos, ghosts, goal) or depth == 0:
            #returns utility
            return self.eval_pos_pacman(pos, goal, ghosts)
        v = float('-inf')
        for move in self.get_moves(pos, maze, None):
            #Find maximum utility of all the moves
            v = max(v, self.min_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze))
        return v
    
    def min_value(self, pos, ghosts, goal, screen, depth, maze):
        """
        Minimises the value of the adversarial agent's moves in the minimax algorithm.

        Parameters:
        - pos (tuple): The current position being evaluated.
        - ghosts (List of Adversaries): The ghosts within the simulation.
        - goal (tuple): The location of the food goal.
        - screen: The Pygame screen to update.
        - depth (int): The current depth in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
    
        Returns:
        - The minimum utility value of the ghost's moves.
        """
        #Base Case
        if self.game_end(pos, ghosts, goal) or depth == 0:
            #returns utility
            return self.eval_pos_pacman(pos, goal, ghosts)
        v = float('inf')
        for move in self.get_moves(pos, maze, None):
            #Find minimum utility of all the moves
            v = min(v, self.max_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze))
        return v
    
    def minimax(self, goal, ghosts, screen, depth, maze):
        """
        Executes the minimax algorithm to calculate an optimal move for the Pac-Man agent.

        Parameters:
        - goal (tuple): The location of the food goal.
        - ghosts (list of Adversaries): The ghosts within the simulation.
        - screen: The Pygame screen to update.
        - depth (int): The maximum depth to search in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
        """
        best_moves = []
        best_value = float('-inf')
        for move in self.get_moves((self.y, self.x), maze, None):
            # Calculates the utility
            value = self.min_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze)
            # Best move has the maximum utility
            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)
        # If there are multiple best moves, choose one randomly
        if best_moves:
            best_move = random.choice(best_moves)
        # Execute the best move
        self.update(screen, best_move, False)

    def ab_max_value(self, pos, ghosts, goal, screen, depth, maze, alpha, beta):
        """
        Maximizes the value of Pac-Man's moves in the Alpha-Beta Pruning algorithm.

        Parameters:
        - pos (tuple): The current position being evaluated.
        - ghosts (List of Adversaries): The ghosts within the simulation.
        - goal (tuple): The location of the food goal.
        - screen: The Pygame screen to update.
        - depth (int): The current depth in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
        - alpha (float): The best utility that the maximizing player (Pacman) can have.
        - beta (float): The best utility that the minimizing player (ghosts) can have.
    
        Returns:
        - The maximum utility value of the Pac-Man's moves.
        """
        #Base Case
        if self.game_end(pos, ghosts, goal) or depth == 0:
            return self.eval_pos_pacman(pos, goal, ghosts)
        v = float('-inf')
        for move in self.get_moves(pos, maze, None):
            #Find maximum utility of all the moves
            v = max(v, self.ab_min_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze, alpha, beta))
            #Prunes unnecessary branches
            if beta <= alpha:
                break
        return v
    
    def ab_min_value(self, pos, ghosts, goal, screen, depth, maze, alpha, beta):
        """
        Minimises the value of the adversarial agent's moves in the Alpha-Beta Pruning algorithm.

        Parameters:
        - pos (tuple): The current position being evaluated.
        - ghosts (List of Adversaries): The ghosts within the simulation.
        - goal (tuple): The location of the food goal.
        - screen: The Pygame screen to update.
        - depth (int): The current depth in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
        - alpha (float): The best utility that the maximizing player (Pacman) can have.
        - beta (float): The best utility that the minimizing player (ghosts) can have.
    
        Returns:
        - The minimum utility value of the ghost's moves.
        """
        #Base Case
        if self.game_end(pos, ghosts, goal) or depth == 0:
            return self.eval_pos_pacman(pos, goal, ghosts)
        v = float('inf')
        for move in self.get_moves(pos, maze, None):
            #Find minimum utility of all the moves
            v = min(v, self.ab_max_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze, alpha, beta))
            #Prunes unnecessary branches
            if beta <= alpha:
                break
        return v
    
    def ab_minimax(self, goal, ghosts, screen, depth, maze):
        """
        Executes the minimax algorithm with alpha-beta prunin to calculate an optimal move for the Pac-Man agent.

        Parameters:
        - goal (tuple): The location of the food goal.
        - ghosts (list of Adversaries): The ghosts within the simulation.
        - screen: The Pygame screen to update.
        - depth (int): The maximum depth to search in the minimax tree.
        - maze (2D Array): The selected maze in the simulation.
        """
        best_moves = []
        best_value = float('-inf')
        #Initialises alpha and beta values to be used
        alpha = float('-inf')
        beta = float('inf')
        # Calculates the utility
        for move in self.get_moves((self.y, self.x), maze, None):
            value = self.ab_min_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze, alpha, beta)
            # Best move has the maximum utility
            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)
                #Updates the alpha to best move
                alpha = max(alpha, best_value)
        # If there are multiple best moves, choose one randomly
        if best_moves:
            best_move = random.choice(best_moves)
        #Executes best move
        self.update(screen, best_move, False)

    #I was not able to fully complete expectimax, however this is what I managed to complete so far, I am 
    #aware that this is not a true implementation as it does not take into account ghost turns and outcomes of random movemment.

    def expectimax_value(self, pos, ghosts, goal, screen, depth, maze):
        """
        Calculates the expected utility value for a given position in the Expectimax algorithm.

        Parameters:
        - pos (tuple): The current position being evaluated.
        - ghosts (List of Adversaries): The ghosts within the simulation.
        - goal (tuple): The location of the food goal.
        - screen: The Pygame screen to update.
        - depth (int): The current depth in the expectimax tree.
        - maze (2D Array): The selected maze in the simulation.

        Returns:
        - The expected utility value of the given position.
        """
        # Base case: if the game ends or depth is reached, return the utility of the tile
        if self.game_end(pos, ghosts, goal) or depth == 0:
            return self.eval_pos_pacman(pos, goal, ghosts)
    
        total_value = 0
        num_moves = len(self.get_moves(pos, maze, None))

        # Calculates and returns the mean utility value of all possible moves from the given position
        # Takes into account all possible moves???
        for move in self.get_moves(pos, maze, None):
            total_value += self.max_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze)
    
        return total_value / num_moves

    def expectimax(self, goal, ghosts, screen, depth, maze):
        """
        Executes the Expectimax algorithm to calculate an optimal move for the Pac-Man agent.

        Parameters:
        - goal (tuple): The location of the food goal.
        - ghosts (list of Adversaries): The ghosts within the simulation.
        - screen: The Pygame screen to update.
        - depth (int): The maximum depth to search in the expectimax tree.
        - maze (2D Array): The selected maze in the simulation.
        """
        best_moves = []
        best_value = float('-inf')

        # Calculates the utility for each possible move
        for move in self.get_moves((self.y, self.x), maze, None):
            value = self.expectimax_value(self.update(screen, move, True), ghosts, goal, screen, depth - 1, maze)
            # Selects the best move based on highest utility
            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)

        if best_moves:
            # If there are multiple best moves, choose one randomly
            best_move = random.choice(best_moves)
        # Executes the best move
        self.update(screen, best_move, False)