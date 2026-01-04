"""
Pac-Man Simulation Executable

This script runs the Pac-Man simulation. It first displays a main menu
that has options for different maze sizes and types for the Pac-Man to navigate through. Users can choose the maze size, which will lead them
to the customisation window, where they have the option to select they types/amounts of ghosts in the simulation, as well as the number of goals.
After selecting these, they will go to the simulation window, where they can run different search algorithms (DFS, BFS, UCS, A*, Minimax, Reflex, AB Pruning) to find the food goal.
The simulation also suppports resetting the environment, changing the speed and radomising locations of both the ghosts and goals.

Classes Used:
    - PacMan: Represents the Pac-Man character with movement and search algorithm implementations.
    - FoodGoal: Represents the randomly placed goals (food) that the Pac-Man agent needs to reach.
    - Adversary: Represents an adversary (ghost) agent that can be made as either sationary, random or tracking.

Usage:
    Run the script to start the Pac-Man simulation. Use the main menu to select maze size. Customise amount of goals by typing a number with the keyboard. 
    Use side menu in simulation window to execute search algorithms, or make adjustments to the environment.
    Control Pac-Man's movement manually using arrow keys.
    Reset once an algorithm has completed running and test another one.
    Amount of moves taken to reach an end goal will be displayed in the console if the algorithm executed succesfully
"""
#Imports required classes
from pacman import PacMan
from foodGoal import FoodGoal
from adversary import Adversary
import pygame
import sys
import time
import copy

pygame.init()

#Initial dimesions for main menu
window_width = 800
window_height = 800

#The tile size shrinks as the maze size grows to proportionise
tile_size_large = 50
tile_size_medium = 80
tile_size_small = 100

#I used variables here for ease of access
white = (255, 255, 255)
black = (0, 0, 0)
dark_blue = (0, 0, 128)

#Prevents the game loop from constantly executing algorithms and options
#All agent booleans
DFS = False
BFS = False
UCS = False
AStar = False
Reflex = False
Minimax = False
ABPruning = False
Expectimax = False

#Initial speed setting
speed: int = 1

#Resets changing variables
steps = 0
initial_food_locations = []
initial_ghost_locations = []

#Manages maintenance of the environment
goalFound = False
pathFound = False
selectedGhosts = []
Go = False
mazeCreated = False

#Prevents game loop form producing more than one of each variable
Ghost = False
goalCreated = False

screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Pac-Man AI Search Algorithm Simulator")

#Maze sizes are stored in a dictionary, mazes are created using 2D Arrays
#Walls are denoted by "W" and empty spaces are denoted by 0
#Ghosts will be depicted by a 2, and its surrounding tiles by a 1
maze_sizes = {
    "Large": (tile_size_large, [
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", 0, 0, 0, 0, 0, 0, "W", 0, 0, 0, 0, 0, 0, 0, "W"],
    ["W", 0, "W", 0, "W", "W", 0, 0, 0, "W", "W", "W", 0, "W", 0, "W"],
    ["W", 0, "W", 0, "W", "W", 0, "W", 0, 0, 0, 0, 0, "W", 0, "W"],
    ["W", 0, "W", 0, 0, "W", 0, "W", "W", "W", 0, "W", 0, "W", 0, "W"],
    ["W", 0, "W", "W", 0, "W", 0, "W", 0, 0, 0, 0, 0, "W", 0, "W"],
    ["W", 0, 0, 0, 0, "W", 0, 0, 0, "W", 0, "W", 0, 0, 0, "W"],
    ["W", 0, "W", "W", 0, "W", 0, "W", 0, "W", 0, "W", "W", "W", 0, "W"],
    ["W", 0, "W", 0, 0, 0, 0, "W", 0, "W", 0, 0, 0, 0, 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W", "W", 0, "W", 0, "W", "W", "W", 0, "W"],
    ["W", 0, "W", 0, 0, 0, "W", 0, 0, 0, 0, 0, 0, 0, 0, "W"],
    ["W", 0, "W", "W", "W", 0, 0, 0, "W", "W", 0, "W", "W", 0, "W", "W"],
    ["W", 0, 0, 0, 0, 0, "W", 0, 0, "W", 0, 0, 0, 0, 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W", "W", 0, 0, 0, "W", 0, "W", 0, "W"],
    ["W", 0, 0, 0, 0, 0, 0, 0, 0, "W", 0, 0, 0, 0, 0, "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ]),
    "Medium": (tile_size_medium, [
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", 0, 0, "W", 0, 0, 0, 0, 0, "W"],
    ["W", "W", 0, "W", 0, "W", "W", "W", 0, "W"],
    ["W", 0, 0, 0, 0, 0, 0, "W", 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W", "W", 0, "W"],
    ["W", 0, "W", 0, "W", 0, 0, 0, 0, "W"],
    ["W", 0, "W", 0, 0, 0, "W", "W", 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W", "W", "W", "W"],
    ["W", 0, 0, 0, "W", 0, 0, 0, 0, "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ]),
    "Small": (tile_size_small, [
    ["W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", 0, "W", 0, 0, "W", 0, "W"],
    ["W", 0, "W", 0, "W", "W", 0, "W"],
    ["W", 0, 0, 0, "W", "W", 0, "W"],
    ["W", 0, "W", 0, 0, 0, 0, "W"],
    ["W", 0, "W", "W", 0, "W", 0, "W"],
    ["W", 0, 0, "W", 0, 0, 0, "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W"],
    ]),
    "MultiPath": (tile_size_medium, [
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", 0, 0, 0, 0, 0, 0, 0, "W", "W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W", "W"],
    ["W", 0, 0, 0, 0, 0, 0, 0, "W", "W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W", "W"],
    ["W", 0, 0, 0, 0, 0, 0, 0, "W", "W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W", "W"],
    ["W", 0, 0, 0, 0, 0, 0, 0, "W", "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
    ])
}

#The different speeds available in the simulation
speeds = {"Slow": 0.75, "Fast": 0.5, "Debug": 0}

#Sets initial state and speed of program
current_state = "MainMenu"
current_speed = "Slow"

#Defualt variables frequently used when making my interface consistent
button_x = 300
button_y = 360
button_spacing = 50
button_height = 40
button_width = 200

#Formatting Main Menu buttons
main_menu_buttons = {
    "Small": pygame.Rect(button_x, button_y, button_width, button_height),
    "Medium": pygame.Rect(button_x, button_y + button_spacing, button_width, button_height),
    "Large": pygame.Rect(button_x, button_y + 2 * button_spacing, button_width, button_height),
    "MultiPath": pygame.Rect(button_x, button_y + 3 * button_spacing, button_width, button_height),
    "Exit": pygame.Rect(button_x, button_y + 5 * button_spacing, button_width, button_height),
}

#Formatting Customisation Menu buttons
customise_buttons = {
    "Stationary": pygame.Rect(50, 275 + 3 * button_spacing, button_width, button_height),
    "Random": pygame.Rect(button_x, 275 + 3 * button_spacing, button_width, button_height),
    "Tracker": pygame.Rect(550, 275 + 3 * button_spacing, button_width, button_height),
    "Run": pygame.Rect(button_x, button_y + 4 * button_spacing, button_width, button_height),
    "Main Menu": pygame.Rect(button_x, button_y + 7 * button_spacing, button_width, button_height),
}

#Formatting Input box for entering an amount of goals
input_box = pygame.Rect(window_width // 2 - 100, window_height // 2 - 150 , 200, 40)
input_font = pygame.font.Font(None, 36)
input_color = black
num_goals_input = ""

#Formatting Simulation buttons
simulation_buttons = {
    "DFS": pygame.Rect(900, 25, button_width, button_height),
    "BFS": pygame.Rect(900, 25 + button_spacing, button_width, button_height),
    "UCS": pygame.Rect(900, 25 + button_spacing*2, button_width, button_height),
    "A*": pygame.Rect(900, 25 + button_spacing*3, button_width, button_height),
    "Reflex": pygame.Rect(900, 25 + button_spacing*4, button_width, button_height),
    "Minimax": pygame.Rect(900, 25 + button_spacing*5, button_width, button_height),
    "AB Pruning": pygame.Rect(900, 25 + button_spacing*6, button_width, button_height),
    "(WIP)Expectimax": pygame.Rect(900, 25 + button_spacing*7, button_width, button_height),
    "Speed": pygame.Rect(900, 725 - button_spacing*5, button_width, button_height),
    "Rand Goal": pygame.Rect(900, 725 - button_spacing*4, button_width, button_height),
    "Rand Ghost": pygame.Rect(900, 725 - button_spacing*3, button_width, button_height),
    "Reset": pygame.Rect(900, 725 - button_spacing*2, button_width, button_height),
    "Customisation": pygame.Rect(900, 725 - button_spacing, button_width, button_height),
    "Menu": pygame.Rect(900, 725, button_width, button_height),
}

#Game Loop
running = True
while running:
    #Allows for exit of game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if current_state == "MainMenu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                #All main menu maze buttons will progress game state to "Customisation"
                x, y = event.pos
                for choice, button in main_menu_buttons.items():
                    if button.collidepoint(x, y):
                        if(choice == "Exit"):
                            pygame.quit()
                            sys.exit()
                        #Initialises size of maze
                        current_size = choice
                        current_tile_size, current_maze = maze_sizes[current_size]
                        current_state = "Customise"

        if current_state == "Customise":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character if backspace is pressed
                    num_goals_input = num_goals_input[:-1]
                else:
                    # Append the entered character to the input
                    num_goals_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for choice, button in customise_buttons.items():
                    # Handles adding/removing types of ghosts
                    # Number of each ghost limited to 1
                    if button.collidepoint(x, y):
                        if(choice == "Tracker"):
                            if "tracker" not in selectedGhosts:
                                selectedGhosts.append("tracker")
                                print("Tracker Added!")
                            else:
                                selectedGhosts.remove("tracker")
                                print("Tracker Removed!")
                        elif(choice == "Random"):
                            if "random" not in selectedGhosts:
                                selectedGhosts.append("random")
                                print("Random Added!")
                            else:
                                selectedGhosts.remove("random")
                                print("Random Removed!")
                        elif(choice == "Stationary"):
                            if "stationary" not in selectedGhosts:
                                selectedGhosts.append("stationary")
                                print("Stationary Added!")
                            else:
                                selectedGhosts.remove("stationary")
                                print("Stationary Removed!")

                        #Returns to menu
                        elif(choice == "Main Menu"):
                            current_state = "MainMenu"

                        elif(choice == "Run"):
                            if not num_goals_input.isdigit():
                                #Error handling for non number
                                print("Please enter a positive numerical value for the number of goals.")
                            else:
                                num_goals = int(num_goals_input)
                                if current_size == "Small":
                                    goal_limit = 5
                                else:
                                    goal_limit = 10
                                #Error handling for no input
                                if(num_goals == 0):
                                    print("No input detected!")
                                #Limits maximum amount of goals
                                elif(num_goals > goal_limit):
                                    print("Exceeded maximum number of goals!")
                                else:
                                    #Pacman agent always starts at (1,1)
                                    pacman = PacMan(1, 1, current_tile_size)
                                    #Larger space so that there is room for side menu on right of screen
                                    screen = pygame.display.set_mode((1200, 800))
                                    #Breaks off console output to improve readability
                                    print("-------------------------------------------------------")
                                    print("Current Speed Set:", current_speed)
                                    current_state = "Simulation"
                                    #Makes ghosts if they are needed
                                    if selectedGhosts:
                                        Ghost = True
                        #Will always show an updated list of ghosts in console based on user selection
                        print("Ghosts Selected:", selectedGhosts)
        
        if current_state == "Simulation":
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for choice, button in simulation_buttons.items():
                    #Handles choice of algorithm/option
                    if button.collidepoint(x, y):
                        #All buttons not related to an algorithm do not need to start the simulation
                        if choice not in ("Speed", "Reset", "Rand Goal", "Menu", "Rand Ghost"):
                            Go = True

                        #Algorithm buttons
                        if(choice == "DFS"):
                            print("Executing Depth-First Search...")
                            DFS = True
                        elif(choice == "BFS"):
                            print("Executing Breadth-First Search...")
                            BFS = True
                        elif(choice == "UCS"):
                            print("Executing Uniform-Cost Search...")
                            UCS = True
                        elif(choice == "A*"):
                            print("Executing A*...")
                            AStar = True
                        elif(choice == "Reflex"):
                            print("Executing with a Reflex Agent...")
                            Reflex = True
                        elif(choice == "Minimax"):
                            print("Executing with a Minimax Agent...")
                            Minimax = True
                        elif(choice == "AB Pruning"):
                            print("Executing with an Alpha-Beta Pruning Agent...")
                            ABPruning = True
                        elif(choice == "(WIP)Expectimax"):
                            print("Executing with an Expecitmax Agent...")
                            Expectimax = True

                            #Maintenance and Environment buttons
                        elif(choice == "Speed"):
                            #Carousels between different speed tyoes
                            if(current_speed == "Slow"):
                                current_speed = "Fast"
                            elif(current_speed == "Fast"):
                                current_speed = "Debug"
                            elif(current_speed == "Debug"):
                                current_speed = "Slow"
                            speed = speeds[current_speed]
                            #Outputs choice and updates speed
                            print("Speed set to", current_speed)
                            pygame.display.flip()

                        elif(choice == "Rand Goal"):
                            print("Randomising Goals...")
                            #Recreates goals in different locations
                            goalCreated = False

                        elif(choice == 'Rand Ghost'):
                            print("Randomising Ghost Locations...")
                            if selectedGhosts:
                                ghostLocations = []
                                for ghost in selectedGhosts:
                                    #Randomises each ghost's coords and updates the internal map accordingly
                                    current_maze = ghost.update_ghost_costs(current_maze, False)
                                    current_maze = ghost.generate_random_position(current_maze, foodGoal.goals)
                                    ghostLocations.append((ghost.y, ghost.x))
                                    #Keep a backup of new locations if the positions need to be reset
                                    initial_ghost_locations = copy.deepcopy(ghostLocations)
                            else:
                                #Error handling if no ghosts were selected in customisation
                                print("No ghosts within the simulation! Add some in Customisation.")
                            #Rebuilds the maze with new ghosts
                            mazeCreated = False
                            
                        elif(choice == "Reset" or choice ==  "Menu" or choice ==  "Customisation"):
                            #All 3 choices reset all algorithms and maintenance
                            #Stops AI Algorithms
                            DFS = False
                            BFS = False
                            UCS = False
                            AStar = False
                            Reflex = False
                            AdvReflex = False
                            Minimax = False
                            ABPruning = False

                            #Stops and Resets Environment
                            Go = False
                            pathFound = False
                            goalFound = False
                            mazeCreated = False
                            steps = 0

                            #Resets Goal states and positions
                            foodGoal.goals = copy.deepcopy(initial_food_locations)

                            #Resets ghost positions
                            for i, ghost in enumerate(selectedGhosts):
                                current_maze = ghost.update_ghost_costs(current_maze, False)
                                (ghost.y, ghost.x) = initial_ghost_locations[i]

                            #Resets Internal Map and Pac-Man agent
                            current_tile_size, current_maze = maze_sizes[current_size]
                            pacman.reset(screen)

                            #End of Reset actions
                            if(choice == "Menu" or choice ==  "Customisation"):
                                selectedGhosts = []
                                goalCreated = False
                                #Practically resets entire state, so new maze size can be selected
                                screen = pygame.display.set_mode((800, 800))
                                if(choice == "Customisation"):
                                #Goes to selected window
                                    current_state = "Customise"
                                else:
                                    current_state = "MainMenu"

    #Creates Main Menu window, with correct titles and text
    if current_state == "MainMenu":
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        welcome_text = font.render("Welcome to the Pac-Man Simulator!", True, white)
        text_rect = welcome_text.get_rect(center=(window_width // 2, window_height // 2 - 200))
        sub_text = font.render("Please choose a maze to get started:", True, white)
        sub_text_rect = welcome_text.get_rect(center=(window_width // 2, window_height // 2 - 125))
        screen.blit(welcome_text, text_rect)
        screen.blit(sub_text, sub_text_rect)

        #Iterates over buttons in main menu dict and draws them accordingly
        for size, button in main_menu_buttons.items():
            pygame.draw.rect(screen, dark_blue, button)
            font = pygame.font.Font(None, 36)
            text = font.render(size, True, white)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

    #Creates Customisation window, with correct titles and text
    if current_state == "Customise":
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        customise_text = font.render("Please customise the environment for your simulation", True, white)
        goal_text = font.render("Number of Goals (Max: 10):", True, white)
        ghost_text = font.render("Select the ghosts you wish to be featured:", True, white)
        customise_rect = customise_text.get_rect(center=(window_width // 2, window_height // 2 - 300))
        goal_rect = goal_text.get_rect(center=(window_width // 2, window_height // 2 - 200))
        ghost_rect = ghost_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        screen.blit(customise_text, customise_rect)
        screen.blit(goal_text, goal_rect)
        screen.blit(ghost_text, ghost_rect)

        #Creates an input box to enter number of goals to be created
        input_box_center = input_box.center
        pygame.draw.rect(screen, white, input_box)
        input_render = input_font.render(num_goals_input, True, input_color)
        input_render_rect = input_render.get_rect(center=input_box_center)
        screen.blit(input_render, input_render_rect)

        #Iterates over buttons in customisation dict and draws them accordingly
        for size, button in customise_buttons.items():
            pygame.draw.rect(screen, dark_blue, button)
            font = pygame.font.Font(None, 36)
            text = font.render(size, True, white)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)        
        
        #Sets up Simulation window
    if current_state == "Simulation":

        #Creates the maze
        if not mazeCreated:
            screen.fill(black)
            for row in range(len(current_maze)):
                for col in range(len(current_maze[row])):
                    if current_maze[row][col] == "W":
                        pygame.draw.rect(screen, dark_blue, (col * current_tile_size, row * current_tile_size, current_tile_size, current_tile_size))
            mazeCreated = True
        
        #Creates the goals
        if not goalCreated:
            foodGoal = FoodGoal(current_tile_size)
            foodGoal.generate_random_position(current_maze, num_goals)
            initial_food_locations = copy.deepcopy(foodGoal.goals)
            mazeCreated = False
            goalCreated = True

        #Iterates over buttons in simulation dict and draws them accordingly
        for choice, button in simulation_buttons.items():                
            pygame.draw.rect(screen, white, button)
            font = pygame.font.Font(None, 36)
            text = font.render(choice, True, black)
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

        #Creates the ghosts
        if Ghost:
            ghostLocations = []
            for i, ghost in enumerate(selectedGhosts):
                #Each ghost is its own object
                selectedGhosts[i] = Adversary(1, 1, current_tile_size, ghost)
                current_maze = selectedGhosts[i].generate_random_position(current_maze, foodGoal.goals)
                ghostLocations.append((selectedGhosts[i].y, selectedGhosts[i].x))
                initial_ghost_locations = copy.deepcopy(ghostLocations)
            Ghost = False

        if selectedGhosts:
            for ghost in selectedGhosts:
                #Adds ghost costs to the internal map for agents and displays the ghost
                current_maze = ghost.update_ghost_costs(current_maze, True)
                ghost.display(screen)

        #Displays the pacman and food goals
        pacman.draw(screen)
        foodGoal.create(screen)

        #Initialises a local list to keep track of which goals are left
        goals = foodGoal.goals

        #Handles algorithm selections
        if Go:
            #Increases number of moves counter
            steps += 1
            #Checks if the Pac-Man runs into a ghost, stops the simulation if it has been caught
            if current_maze[pacman.y][pacman.x] == 2:
                print("Pacman was caught!")
                Go = False
            
            #DFS, BFS, UCS, AStar
            if DFS or BFS or UCS or AStar and goals:
                if goalFound == False:
                    #Finds closest goal to current position
                    goals = pacman.goal_sorter(goals, current_maze)
                    goal = goals[0]
                    goalFound = True
                #Calculates path using chosen algorithm
                if not pathFound:
                    if DFS:
                        path = pacman.dfs(current_maze, goal)
                    elif BFS:
                        path = pacman.bfs(current_maze, goal)
                    elif UCS:
                        path = pacman.ucs(current_maze, goal)
                    elif AStar:
                        path = pacman.a_star(current_maze, goal)
                    pathFound = True
                #Executes path step-by-step
                if path:
                    move = path.pop(0)
                    pacman.update(screen, move, False)
                    if((pacman.y, pacman.x) == goal):
                        #If goal is reached, calculate path to next nearest goal
                        goals.remove(goal)
                        goalFound = False
                        pathFound = False
                        if not goals:
                            #Returns number of moves taken to complete
                            print("Beaten in", steps, "steps!")
                            DFS = False
                            BFS = False
                            UCS = False
                            AStar = False
                            Go = False
                    elif((pacman.y, pacman.x) in goals):
                        #If a goal is found whilst reaching another point, it is also classed as eaten
                        goals.remove((pacman.y, pacman.x))
            
            #Reflex
            if Reflex and goals:
                if goalFound == False:
                    #Finds closest goal to current position
                    goals = pacman.goal_sorter(goals, current_maze)
                    goal = goals[0]
                    goalFound = True
                
                x, y = pacman.x, pacman.y
                #Checks if a ghost is near, reacts appropriately
                pacman.detect(current_maze, goal, screen)

                #Checks if the agent has already made a move
                if ((pacman.y, pacman.x) == (y,x)):
                    #If not, use A* to move towards the goal
                    move = pacman.a_star(current_maze, goal)
                    if move:
                        pacman.update(screen, move.pop(0), False)

                #If goal is reached, calculate path to next nearest goal
                if (pacman.y, pacman.x) == goal:
                    goals.remove(goal)
                    goalFound = False

                    if not goals:
                        #Returns number of moves taken to complete
                        print("Beaten in", steps, "steps!")
                        Reflex = False
                        Go = False

                elif((pacman.y, pacman.x) in goals):
                    #If a goal is found whilst reaching another point, it is also classed as eaten
                    goals.remove((pacman.y, pacman.x))

            #Minimax, AB Pruning, Expectimax
            if Minimax or ABPruning or Expectimax:
                #Error handling when there are no ghosts present within the maze
                if selectedGhosts == []:
                    print("Minimax, Expectimax and AB Pruning require at least 1 ghost to function, please add a type of ghost in Customisation.")
                    Minimax = False
                    ABPruning = False
                    Expectimax = False
                    Go = False
                    continue
                if goals:
                    if goalFound == False:
                        #Finds closest goal to current position
                        goals = pacman.goal_sorter(goals, current_maze)
                        goal = goals[0]
                        goalFound = True

                    #Executes selected algorithm
                    if Minimax:
                        pacman.minimax(goal, selectedGhosts, screen, 15, current_maze)
                    elif ABPruning:
                        pacman.ab_minimax(goal, selectedGhosts, screen, 15, current_maze)
                    elif Expectimax:
                        pacman.expectimax(goal, selectedGhosts, screen, 15, current_maze)
                    #Redraws goals if they were affected during computation
                    foodGoal.create(screen)
                    if (pacman.y, pacman.x) == goal:
                        #If goal is reached, calculate path to next nearest goal
                        goals.remove(goal)
                        goalFound = False
                        pathFound = False
                        if not goals:
                            #Returns number of moves taken to complete
                            print("Beaten in", steps, "steps!")
                            Minimax = False
                            ABPruning = False
                            Expectimax = False
                            Go = False
                    elif((pacman.y, pacman.x) in goals):
                        #If a goal is found whilst reaching another point, it is also classed as eaten
                        goals.remove((pacman.y, pacman.x))

            if(current_maze == None):
                #Handles event where maze gets wiped
                continue
                
            #Moves any ghost incremently during each iteration
            if selectedGhosts and Go:
                for ghost in selectedGhosts:
                    current_maze = ghost.update_ghost_costs(current_maze, False)
                    if ghost.type == "tracker":
                        current_maze = ghost.a_star(current_maze, (pacman.y, pacman.x), screen)
                    elif ghost.type == "random":
                        current_maze = ghost.random_move(screen, current_maze)
                if current_maze == None:
                    current_tile_size, current_maze = maze_sizes[current_size]
                #Updates ghost costs within internal map
                current_maze = ghost.update_ghost_costs(current_maze, True)

            #Slows down simulation so that the user has time to follow paths
            time.sleep(speed)

        #Adds functionality for manually moving the pacman around the maze using arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.move("up", current_maze, screen)
        elif keys[pygame.K_DOWN]:
            pacman.move("down", current_maze, screen)
        elif keys[pygame.K_LEFT]:
            pacman.move("left", current_maze, screen)
        elif keys[pygame.K_RIGHT]:
            pacman.move("right", current_maze, screen)
        else:
            pacman.moving = False

    pygame.display.flip()

pygame.quit()
sys.exit()