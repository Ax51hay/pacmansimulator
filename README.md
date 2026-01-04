## Development Process
This project was developed iteratively over several months as assessed
university coursework. Version control was used extensively on a
university-managed GitHub account.

The repository hosted here is a cleaned and documented mirror intended
for portfolio review. A detailed development log outlining algorithm
implementation, testing, refactoring, and release milestones is
available on request.

------------------------------------------------------
Welcome to my Pac-Man AI Search Algorithm Simulator!
------------------------------------------------------
Overview:
This program is a customisable Pac-Man simulator implemented in Python using the Pygame library. It uses a Pac-Man agent, several end goals (food pellets), and different types of adversarial agents (ghosts). The simulator allows the Pac-Man to use different AI search algorithms and reactive measures (DFS, BFS, UCS, AStar, Reflex, Minimax, AB Pruning, Expectimax (WIP)) to calculate optimal paths that lead to end goals within different sizes and types of mazes.

Features:
 - 4 types and sizes of maze environments are available to be selected from the main menu
 - The Pac-Man agent is able to be controlled manually via keyboard input
 - Amount of food goals and ghosts included within the simulation are fully customisable
 - 3 types of ghosts are available to use: Stationary (Orange), Random (Cyan) and Tracker (Light Pink)
 - The Food goal and ghost locations are randomly generated upon each run through, and can either be reset or randomly replaced upon selection from the side bar
 - Support for Single and Multi-Agent environments
 - Support for static and non static environments
 - Search algorithms implemented: DFS, BFS, UCS, A*, Minimax, Alpha-Beta Pruning, Expectimax (WIP)
 - Extensions of search algorithms implemented - Reflex Agent (Using A*)

Prerequisites:

This program requires the installation of Pygame

Currently supports Python 3

Running the Program:

Ensure all files are within the same directory

Run the maze.py file

Unit Tests can be run individually

Using the Program:

1 - Select a size or type of maze


2.1 - Use the keyboard to type the number of goals you wish to be implemented

2.2 - Click on the adversary types that you wish to be included, these can be selected or deselected, and the result of your actions are displayed within the console

2.3 - Once you are happy with your decisions, click 'Run'


3.0.1 - If you wish to change the number of agents or goals within the simulation, click 'Customisation'

3.0.2 - Upon launch, the speed will be set to Slow, to change this click on the 'Speed' button, and it will update in the console

3.0.3 - If you wish to change the layout of the goals/ghosts, you can select the 'Rand Goal' and 'Rand Ghost' buttons, any changes are updated on screen and in the console

3.1 - Use the arrow keys to move the Pac-Man agent to a preferred space

3.2.1 - Select an algorithm or mode from the side menu to start the simulation

3.2.2 - If a suitable path is found, the simularion will visualise the agents steps taken on screen

3.2.3 - Should the Pac-Man be caught, the simulation will stop and a message will be returned in the console

      - Otherwise, upon completion the number of steps taken for the pacman to clear the maze will be returned in the console


4 - Reset the maze to test a different algorithm under the same conditions


5 - Select Menu to select a different size maze, and to go through Customisations again

Examples:
Below are suggested environment formats that will showcase each algorithm's traditional performances:

DFS:

Maze = Any

Ghosts = None

Food = Any


BFS:

Maze = Any

Ghosts = None

Food = Any


UCS:

Maze = Any

Ghosts = Stationary

Food = Any


AStar:

Maze = Any

Ghosts = Stationary

Food = Any


Reflex:

Maze = Any

Ghosts = Stationary, Random, Tracker

Food = Any


Minimax:

Maze = Any

Ghosts = Random, Tracker, Stationary (Optional)

Food = Any


AB Pruning:

Maze = Any

Ghosts = Random, Tracker, Stationary (Optional)

Food = Any

Expectimax (WIP):

Maze = Any

Ghosts = Random, Tracker, Stationary (Optional)

Food = Any


**NOTES**
This program is a simulator, which gives users flexibility in how they create the environments in which they wish to test different AI Algorithms. This means that there will be cases where algorithms will perform adversely if executed in non-traditional environments. For examples on which environments are suggested for use with each algorithm, please see EXAMPLES.

Minimax and AB Pruning require at least 1 ghost agent in order to run

Expectimax is not fully functional, and does not reflect how the algorithm is meant to work.

Thank you for using!
