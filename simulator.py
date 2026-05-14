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
    Amount of moves taken to reach an end goal will be displayed in the simulation window if the algorithm executed succesfully.
"""
from pacman import PacMan
from foodGoal import FoodGoal
from adversary import Adversary
import pygame
import sys
import time
import copy

pygame.init()

# ── Display ──────────────────────────────────────────────────────────────────
window_width  = 800
window_height = 800

tile_size_large  = 50
tile_size_medium = 80
tile_size_small  = 100

# ── Colour palette ───────────────────────────────────────────────────────────
black       = (0,   0,   0  )
white       = (255, 255, 255)
dark_blue   = (0,   0,   128)   # maze walls
yellow      = (255, 215, 0  )   # Pac-Man yellow — borders, titles, accents
navy        = (15,  15,  50 )   # button / panel fill
info_bg     = (10,  10,  38 )   # info panel fill
dim_white   = (180, 180, 210)   # label text inside info panel
green_fill  = (0,   110, 0  )   # active / selected button fill
green_bdr   = (0,   210, 0  )   # active / selected button border
red_text    = (255, 90,  90 )   # "caught" status
green_text  = (100, 255, 100)   # "beaten" status
amber_text  = (255, 200, 0  )   # neutral status / warnings

# ── Maze definitions ─────────────────────────────────────────────────────────
maze_sizes = {
    "Large": (tile_size_large, [
    ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
    ["W", 0,  0,  0,  0,  0,  0, "W", 0,  0,  0,  0,  0,  0,  0, "W"],
    ["W", 0, "W", 0, "W","W", 0,  0,  0, "W","W","W", 0, "W", 0, "W"],
    ["W", 0, "W", 0, "W","W", 0, "W", 0,  0,  0,  0,  0, "W", 0, "W"],
    ["W", 0, "W", 0,  0, "W", 0, "W","W","W", 0, "W", 0, "W", 0, "W"],
    ["W", 0, "W","W", 0, "W", 0, "W", 0,  0,  0,  0,  0, "W", 0, "W"],
    ["W", 0,  0,  0,  0, "W", 0,  0,  0, "W", 0, "W", 0,  0,  0, "W"],
    ["W", 0, "W","W", 0, "W", 0, "W", 0, "W", 0, "W","W","W", 0, "W"],
    ["W", 0, "W", 0,  0,  0,  0, "W", 0, "W", 0,  0,  0,  0,  0, "W"],
    ["W", 0, "W", 0, "W", 0, "W","W", 0, "W", 0, "W","W","W", 0, "W"],
    ["W", 0, "W", 0,  0,  0, "W", 0,  0,  0,  0,  0,  0,  0,  0, "W"],
    ["W", 0, "W","W","W", 0,  0,  0, "W","W", 0, "W","W", 0, "W","W"],
    ["W", 0,  0,  0,  0,  0, "W", 0,  0, "W", 0,  0,  0,  0,  0, "W"],
    ["W", 0, "W", 0, "W", 0, "W","W", 0,  0,  0, "W", 0, "W", 0, "W"],
    ["W", 0,  0,  0,  0,  0,  0,  0,  0, "W", 0,  0,  0,  0,  0, "W"],
    ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
    ]),
    "Medium": (tile_size_medium, [
    ["W","W","W","W","W","W","W","W","W","W"],
    ["W", 0,  0, "W", 0,  0,  0,  0,  0, "W"],
    ["W","W", 0, "W", 0, "W","W","W", 0, "W"],
    ["W", 0,  0,  0,  0,  0,  0, "W", 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W","W", 0, "W"],
    ["W", 0, "W", 0, "W", 0,  0,  0,  0, "W"],
    ["W", 0, "W", 0,  0,  0, "W","W", 0, "W"],
    ["W", 0, "W", 0, "W", 0, "W","W","W","W"],
    ["W", 0,  0,  0, "W", 0,  0,  0,  0, "W"],
    ["W","W","W","W","W","W","W","W","W","W"],
    ]),
    "Small": (tile_size_small, [
    ["W","W","W","W","W","W","W","W"],
    ["W", 0, "W", 0,  0, "W", 0, "W"],
    ["W", 0, "W", 0, "W","W", 0, "W"],
    ["W", 0,  0,  0, "W","W", 0, "W"],
    ["W", 0, "W", 0,  0,  0,  0, "W"],
    ["W", 0, "W","W", 0, "W", 0, "W"],
    ["W", 0,  0, "W", 0,  0,  0, "W"],
    ["W","W","W","W","W","W","W","W"],
    ]),
    "MultiPath": (tile_size_medium, [
    ["W","W","W","W","W","W","W","W","W","W"],
    ["W", 0,  0,  0,  0,  0,  0,  0, "W","W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W","W"],
    ["W", 0,  0,  0,  0,  0,  0,  0, "W","W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W","W"],
    ["W", 0,  0,  0,  0,  0,  0,  0, "W","W"],
    ["W", 0, "W", 0, "W", 0, "W", 0, "W","W"],
    ["W", 0,  0,  0,  0,  0,  0,  0, "W","W"],
    ["W","W","W","W","W","W","W","W","W","W"],
    ["W","W","W","W","W","W","W","W","W","W"],
    ])
}

speeds = {"Slow": 0.75, "Fast": 0.5, "Debug": 0}

# ── Button layout ─────────────────────────────────────────────────────────────
# Main menu  (800 × 800, buttons centred at x = 400)
main_menu_buttons = {
    "Small":     pygame.Rect(250, 238, 300, 44),
    "Medium":    pygame.Rect(250, 292, 300, 44),
    "Large":     pygame.Rect(250, 346, 300, 44),
    "MultiPath": pygame.Rect(250, 400, 300, 44),
    "Exit":      pygame.Rect(250, 494, 300, 44),
}

# Customise  (800 × 800)
customise_buttons = {
    "Stationary": pygame.Rect(110, 300, 180, 44),
    "Random":     pygame.Rect(310, 300, 180, 44),
    "Tracker":    pygame.Rect(510, 300, 180, 44),
    "Run":        pygame.Rect(270, 380, 260, 50),
    "Main Menu":  pygame.Rect(300, 660, 200, 40),
}

input_box   = pygame.Rect(290, 198, 220, 44)
input_font  = pygame.font.Font(None, 32)

# Simulation sidebar  (1200 × 800 window; sidebar occupies x = 800–1200)
# Buttons centred at x = 1000: left edge = 860, width = 280
_SX = 860
_SW = 280
_SH = 40

simulation_buttons = {
    # ── Algorithms  (label "ALGORITHMS" sits above at y = 8) ──
    "DFS":             pygame.Rect(_SX,  28, _SW, _SH),
    "BFS":             pygame.Rect(_SX,  73, _SW, _SH),
    "UCS":             pygame.Rect(_SX, 118, _SW, _SH),
    "A*":              pygame.Rect(_SX, 163, _SW, _SH),
    "Reflex":          pygame.Rect(_SX, 208, _SW, _SH),
    "Minimax":         pygame.Rect(_SX, 253, _SW, _SH),
    "AB Pruning":      pygame.Rect(_SX, 298, _SW, _SH),
    "(WIP)Expectimax": pygame.Rect(_SX, 343, _SW, _SH),
    # ── Info panel occupies y = 388–500 ──
    # ── Controls  (label "CONTROLS" sits above at y = 504) ──
    "Speed":           pygame.Rect(_SX, 522, _SW, _SH),
    "Rand Goal":       pygame.Rect(_SX, 567, _SW, _SH),
    "Rand Ghost":      pygame.Rect(_SX, 612, _SW, _SH),
    "Reset":           pygame.Rect(_SX, 657, _SW, _SH),
    "Customisation":   pygame.Rect(_SX, 702, _SW, _SH),
    "Menu":            pygame.Rect(_SX, 747, _SW, _SH),
}

# Maps sidebar button labels → state flag keys (algorithm buttons only)
ALGO_FLAGS = {
    "DFS": "DFS", "BFS": "BFS", "UCS": "UCS", "A*": "AStar",
    "Reflex": "Reflex", "Minimax": "Minimax",
    "AB Pruning": "ABPruning", "(WIP)Expectimax": "Expectimax",
}

# ── Shared UI helpers ─────────────────────────────────────────────────────────

def draw_button(screen, rect, label, active=False, font_size=26):
    """Draws a styled button with a yellow border and navy fill.
       Active buttons use a green colour scheme instead."""
    border = green_bdr if active else yellow
    fill   = green_fill if active else navy
    pygame.draw.rect(screen, border, rect, border_radius=6)
    pygame.draw.rect(screen, fill, rect.inflate(-4, -4), border_radius=5)
    font = pygame.font.Font(None, font_size)
    surf = font.render(label, True, white)
    screen.blit(surf, surf.get_rect(center=rect.center))


def draw_ghost_button(screen, rect, label, selected=False):
    """Like draw_button but glows green when the ghost type is selected."""
    draw_button(screen, rect, label, active=selected, font_size=26)


def draw_section_label(screen, text, center_x, y):
    """Small uppercase label used as a section heading."""
    font = pygame.font.Font(None, 20)
    surf = font.render(text, True, yellow)
    screen.blit(surf, (center_x - surf.get_width() // 2, y))


def draw_pellet_row(screen, y, x_start, x_end, spacing=28, radius=4):
    """Draws a row of Pac-Man pellet dots as a decorative separator."""
    x = x_start
    while x <= x_end:
        pygame.draw.circle(screen, white, (int(x), y), radius)
        x += spacing


def draw_title(screen, cx, cy):
    """Renders the PAC-MAN title in yellow with a dark drop shadow."""
    font = pygame.font.Font(None, 80)
    shadow = font.render("PAC-MAN", True, (80, 70, 0))
    screen.blit(shadow, shadow.get_rect(center=(cx + 3, cy + 3)))
    title  = font.render("PAC-MAN", True, yellow)
    screen.blit(title,  title.get_rect(center=(cx, cy)))


def draw_sidebar(screen):
    """Draws the navy sidebar background and the yellow left-edge separator."""
    pygame.draw.rect(screen, navy, pygame.Rect(800, 0, 400, 800))
    pygame.draw.line(screen, yellow, (800, 0), (800, 800), 2)


# ── State ─────────────────────────────────────────────────────────────────────

def init_state(screen):
    return {
        'screen':         screen,
        'current_state':  'MainMenu',
        'current_speed':  'Slow',
        'speed':          1,
        'steps':          0,
        'initial_food_locations':  [],
        'initial_ghost_locations': [],
        'goalFound':    False,
        'pathFound':    False,
        'selectedGhosts': [],
        'Go':           False,
        'mazeCreated':  False,
        'Ghost':        False,
        'goalCreated':  False,
        'DFS':          False,
        'BFS':          False,
        'UCS':          False,
        'AStar':        False,
        'Reflex':       False,
        'Minimax':      False,
        'ABPruning':    False,
        'Expectimax':   False,
        'num_goals_input':    '',
        'num_goals':          0,
        'current_size':       None,
        'current_tile_size':  None,
        'current_maze':       None,
        'pacman':             None,
        'foodGoal':           None,
        'path':               None,
        'goal':               None,
        'status_message':     '',
        'current_algorithm':  'None',
    }


def set_status(state, msg):
    state['status_message'] = msg


# ── Screen renderers ──────────────────────────────────────────────────────────

def draw_main_menu(screen):
    screen.fill(black)
    pygame.draw.rect(screen, yellow, pygame.Rect(10, 10, window_width - 20, window_height - 20), 2)
    draw_title(screen, window_width // 2, 90)
    sub_font = pygame.font.Font(None, 30)
    sub = sub_font.render("AI Search Algorithm Simulator", True, white)
    screen.blit(sub, sub.get_rect(center=(window_width // 2, 145)))
    draw_pellet_row(screen, 175, 40, window_width - 40)
    draw_section_label(screen, "SELECT MAZE", window_width // 2, 215)
    for size, button in main_menu_buttons.items():
        draw_button(screen, button, size, font_size=30)


def draw_customise(screen, state):
    screen.fill(black)
    pygame.draw.rect(screen, yellow, pygame.Rect(10, 10, window_width - 20, window_height - 20), 2)
    draw_title(screen, window_width // 2, 70)
    sub_font = pygame.font.Font(None, 28)
    sub = sub_font.render("Customise Your Environment", True, white)
    screen.blit(sub, sub.get_rect(center=(window_width // 2, 120)))
    draw_pellet_row(screen, 148, 40, window_width - 40)

    # Goals section
    draw_section_label(screen, "NUMBER OF GOALS  (max 10, or 5 for Small)", window_width // 2, 175)
    pygame.draw.rect(screen, yellow, input_box, border_radius=6)
    pygame.draw.rect(screen, (30, 30, 70), input_box.inflate(-4, -4), border_radius=5)
    inp = input_font.render(state['num_goals_input'], True, white)
    screen.blit(inp, inp.get_rect(center=input_box.center))

    # Ghost section
    draw_section_label(screen, "GHOST TYPES  —  click to toggle", window_width // 2, 278)
    for choice, button in customise_buttons.items():
        ghost_key = choice.lower()
        if ghost_key in ('stationary', 'random', 'tracker'):
            draw_ghost_button(screen, button, choice, selected=ghost_key in state['selectedGhosts'])
        else:
            draw_button(screen, button, choice, font_size=28)

    # Status / validation message
    if state['status_message']:
        sf = pygame.font.Font(None, 26)
        ss = sf.render(state['status_message'], True, amber_text)
        screen.blit(ss, ss.get_rect(center=(window_width // 2, 460)))


# ── Event handlers ────────────────────────────────────────────────────────────

def handle_main_menu_event(event, state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for choice, button in main_menu_buttons.items():
            if button.collidepoint(x, y):
                if choice == "Exit":
                    pygame.quit()
                    sys.exit()
                state['current_size'] = choice
                state['current_tile_size'], state['current_maze'] = maze_sizes[choice]
                state['current_state'] = "Customise"


def handle_customise_event(event, state):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            state['num_goals_input'] = state['num_goals_input'][:-1]
        else:
            state['num_goals_input'] += event.unicode
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for choice, button in customise_buttons.items():
            if button.collidepoint(x, y):
                if choice == "Tracker":
                    if "tracker" not in state['selectedGhosts']:
                        state['selectedGhosts'].append("tracker")
                    else:
                        state['selectedGhosts'].remove("tracker")
                elif choice == "Random":
                    if "random" not in state['selectedGhosts']:
                        state['selectedGhosts'].append("random")
                    else:
                        state['selectedGhosts'].remove("random")
                elif choice == "Stationary":
                    if "stationary" not in state['selectedGhosts']:
                        state['selectedGhosts'].append("stationary")
                    else:
                        state['selectedGhosts'].remove("stationary")
                elif choice == "Main Menu":
                    state['current_state'] = "MainMenu"
                elif choice == "Run":
                    if not state['num_goals_input'].isdigit():
                        set_status(state, "Please enter a number for goals.")
                    else:
                        num_goals = int(state['num_goals_input'])
                        goal_limit = 5 if state['current_size'] == "Small" else 10
                        if num_goals == 0:
                            set_status(state, "Please enter a number of goals.")
                        elif num_goals > goal_limit:
                            set_status(state, f"Maximum {goal_limit} goals for this maze size.")
                        else:
                            state['pacman'] = PacMan(1, 1, state['current_tile_size'])
                            state['screen'] = pygame.display.set_mode((1200, 800))
                            state['status_message'] = ''
                            state['current_state'] = "Simulation"
                            state['num_goals'] = num_goals
                            if state['selectedGhosts']:
                                state['Ghost'] = True


def reset_simulation(state):
    state['DFS']          = False
    state['BFS']          = False
    state['UCS']          = False
    state['AStar']        = False
    state['Reflex']       = False
    state['Minimax']      = False
    state['ABPruning']    = False
    state['Expectimax']   = False
    state['Go']           = False
    state['pathFound']    = False
    state['goalFound']    = False
    state['mazeCreated']  = False
    state['steps']        = 0
    state['status_message']    = ''
    state['current_algorithm'] = 'None'
    state['foodGoal'].goals = copy.deepcopy(state['initial_food_locations'])
    for i, ghost in enumerate(state['selectedGhosts']):
        state['current_maze'] = ghost.update_ghost_costs(state['current_maze'], False)
        ghost.y, ghost.x = state['initial_ghost_locations'][i]
    state['current_tile_size'], state['current_maze'] = maze_sizes[state['current_size']]
    state['pacman'].reset(state['screen'])


def handle_simulation_event(event, state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        for choice, button in simulation_buttons.items():
            if button.collidepoint(x, y):
                if choice not in ("Speed", "Reset", "Rand Goal", "Menu", "Rand Ghost"):
                    state['Go'] = True
                if choice == "DFS":
                    state['current_algorithm'] = 'DFS'
                    state['DFS'] = True
                elif choice == "BFS":
                    state['current_algorithm'] = 'BFS'
                    state['BFS'] = True
                elif choice == "UCS":
                    state['current_algorithm'] = 'UCS'
                    state['UCS'] = True
                elif choice == "A*":
                    state['current_algorithm'] = 'A*'
                    state['AStar'] = True
                elif choice == "Reflex":
                    state['current_algorithm'] = 'Reflex'
                    state['Reflex'] = True
                elif choice == "Minimax":
                    state['current_algorithm'] = 'Minimax'
                    state['Minimax'] = True
                elif choice == "AB Pruning":
                    state['current_algorithm'] = 'AB Pruning'
                    state['ABPruning'] = True
                elif choice == "(WIP)Expectimax":
                    state['current_algorithm'] = 'Expectimax'
                    state['Expectimax'] = True
                elif choice == "Speed":
                    if state['current_speed'] == "Slow":
                        state['current_speed'] = "Fast"
                    elif state['current_speed'] == "Fast":
                        state['current_speed'] = "Debug"
                    elif state['current_speed'] == "Debug":
                        state['current_speed'] = "Slow"
                    state['speed'] = speeds[state['current_speed']]
                    pygame.display.flip()
                elif choice == "Rand Goal":
                    set_status(state, "Goals randomised.")
                    state['goalCreated'] = False
                elif choice == "Rand Ghost":
                    if state['selectedGhosts']:
                        ghostLocations = []
                        for ghost in state['selectedGhosts']:
                            state['current_maze'] = ghost.update_ghost_costs(state['current_maze'], False)
                            state['current_maze'] = ghost.generate_random_position(state['current_maze'], state['foodGoal'].goals)
                            ghostLocations.append((ghost.y, ghost.x))
                        state['initial_ghost_locations'] = copy.deepcopy(ghostLocations)
                        set_status(state, "Ghost locations randomised.")
                    else:
                        set_status(state, "No ghosts! Add some in Customisation.")
                    state['mazeCreated'] = False
                elif choice in ("Reset", "Menu", "Customisation"):
                    reset_simulation(state)
                    if choice in ("Menu", "Customisation"):
                        state['selectedGhosts'] = []
                        state['goalCreated'] = False
                        state['screen'] = pygame.display.set_mode((800, 800))
                        state['current_state'] = "Customise" if choice == "Customisation" else "MainMenu"


# ── Simulation rendering ──────────────────────────────────────────────────────

def draw_info_panel(screen, state):
    """Draws the status panel between the algorithm and controls sections."""
    panel = pygame.Rect(_SX, 388, _SW, 112)
    pygame.draw.rect(screen, yellow,   panel, border_radius=6)
    pygame.draw.rect(screen, info_bg,  panel.inflate(-4, -4), border_radius=5)

    lbl_font = pygame.font.Font(None, 18)
    val_font = pygame.font.Font(None, 22)

    def row(label, value, y, val_color=white):
        lbl = lbl_font.render(label, True, dim_white)
        val = val_font.render(value, True, val_color)
        screen.blit(lbl, (_SX + 10, y))
        screen.blit(val, (_SX + 10 + lbl.get_width() + 6, y - 1))

    row("ALGORITHM", state['current_algorithm'], 397, yellow)
    row("SPEED",     state['current_speed'],     421)
    row("STEPS",     str(state['steps']),        445)

    if state['status_message']:
        msg = state['status_message']
        if   "caught" in msg.lower(): color = red_text
        elif "beaten" in msg.lower(): color = green_text
        else:                         color = amber_text
        sf = pygame.font.Font(None, 19)
        ss = sf.render(msg, True, color)
        screen.blit(ss, (_SX + 10, 470))


def setup_simulation(state):
    screen = state['screen']

    # Draw maze walls (only when the maze needs rebuilding)
    if not state['mazeCreated']:
        screen.fill(black)
        for row in range(len(state['current_maze'])):
            for col in range(len(state['current_maze'][row])):
                if state['current_maze'][row][col] == "W":
                    pygame.draw.rect(
                        screen, dark_blue,
                        (col * state['current_tile_size'],
                         row * state['current_tile_size'],
                         state['current_tile_size'],
                         state['current_tile_size'])
                    )
        state['mazeCreated'] = True

    # Place food goals (only when needed)
    if not state['goalCreated']:
        state['foodGoal'] = FoodGoal(state['current_tile_size'])
        state['foodGoal'].generate_random_position(state['current_maze'], state['num_goals'])
        state['initial_food_locations'] = copy.deepcopy(state['foodGoal'].goals)
        state['mazeCreated'] = False
        state['goalCreated'] = True

    # ── Sidebar (redrawn every frame) ────────────────────────────────────────
    draw_sidebar(screen)

    draw_section_label(screen, "ALGORITHMS", 1000, 10)
    for choice, button in simulation_buttons.items():
        flag_key  = ALGO_FLAGS.get(choice)
        is_active = bool(flag_key and state[flag_key])
        draw_button(screen, button, choice, active=is_active, font_size=24)

    draw_info_panel(screen, state)
    draw_section_label(screen, "CONTROLS", 1000, 506)

    # Place ghosts (only on first frame after entering simulation)
    if state['Ghost']:
        ghostLocations = []
        for i, ghost in enumerate(state['selectedGhosts']):
            state['selectedGhosts'][i] = Adversary(1, 1, state['current_tile_size'], ghost)
            state['current_maze'] = state['selectedGhosts'][i].generate_random_position(
                state['current_maze'], state['foodGoal'].goals)
            ghostLocations.append((state['selectedGhosts'][i].y, state['selectedGhosts'][i].x))
        state['initial_ghost_locations'] = copy.deepcopy(ghostLocations)
        state['Ghost'] = False

    if state['selectedGhosts']:
        for ghost in state['selectedGhosts']:
            state['current_maze'] = ghost.update_ghost_costs(state['current_maze'], True)
            ghost.display(screen)

    state['pacman'].draw(screen)
    state['foodGoal'].create(screen)


# ── Simulation logic ──────────────────────────────────────────────────────────

def run_simulation_step(state):
    screen = state['screen']
    goals  = state['foodGoal'].goals
    pacman = state['pacman']

    if not state['Go']:
        return

    state['steps'] += 1

    if state['current_maze'][pacman.y][pacman.x] == 2:
        set_status(state, "Pacman was caught!")
        state['Go'] = False
        return

    # ── Search algorithms (DFS / BFS / UCS / A*) ────────────────────────────
    if (state['DFS'] or state['BFS'] or state['UCS'] or state['AStar']) and goals:
        if not state['goalFound']:
            goals = pacman.goal_sorter(goals, state['current_maze'])
            state['goal'] = goals[0]
            state['goalFound'] = True
        if not state['pathFound']:
            if state['DFS']:
                state['path'] = pacman.dfs(state['current_maze'], state['goal'])
            elif state['BFS']:
                state['path'] = pacman.bfs(state['current_maze'], state['goal'])
            elif state['UCS']:
                state['path'] = pacman.ucs(state['current_maze'], state['goal'])
            elif state['AStar']:
                state['path'] = pacman.a_star(state['current_maze'], state['goal'])
            state['pathFound'] = True
        if state['path']:
            move = state['path'].pop(0)
            pacman.update(screen, move, False)
            if (pacman.y, pacman.x) == state['goal']:
                goals.remove(state['goal'])
                state['goalFound'] = False
                state['pathFound'] = False
                if not goals:
                    set_status(state, f"Beaten in {state['steps']} steps!")
                    state['DFS'] = state['BFS'] = state['UCS'] = state['AStar'] = state['Go'] = False
            elif (pacman.y, pacman.x) in goals:
                goals.remove((pacman.y, pacman.x))

    # ── Reflex agent ─────────────────────────────────────────────────────────
    if state['Reflex'] and goals:
        if not state['goalFound']:
            goals = pacman.goal_sorter(goals, state['current_maze'])
            state['goal'] = goals[0]
            state['goalFound'] = True
        x, y = pacman.x, pacman.y
        pacman.detect(state['current_maze'], state['goal'], screen)
        if (pacman.y, pacman.x) == (y, x):
            move = pacman.a_star(state['current_maze'], state['goal'])
            if move:
                pacman.update(screen, move.pop(0), False)
        if (pacman.y, pacman.x) == state['goal']:
            goals.remove(state['goal'])
            state['goalFound'] = False
            if not goals:
                set_status(state, f"Beaten in {state['steps']} steps!")
                state['Reflex'] = state['Go'] = False
        elif (pacman.y, pacman.x) in goals:
            goals.remove((pacman.y, pacman.x))

    # ── Adversarial algorithms (Minimax / AB Pruning / Expectimax) ───────────
    if state['Minimax'] or state['ABPruning'] or state['Expectimax']:
        if not state['selectedGhosts']:
            set_status(state, "Minimax/AB/Expectimax needs at least 1 ghost!")
            state['Minimax'] = state['ABPruning'] = state['Expectimax'] = state['Go'] = False
            return
        if goals:
            if not state['goalFound']:
                goals = pacman.goal_sorter(goals, state['current_maze'])
                state['goal'] = goals[0]
                state['goalFound'] = True
            if state['Minimax']:
                pacman.minimax(state['goal'], state['selectedGhosts'], screen, 15, state['current_maze'])
            elif state['ABPruning']:
                pacman.ab_minimax(state['goal'], state['selectedGhosts'], screen, 15, state['current_maze'])
            elif state['Expectimax']:
                pacman.expectimax(state['goal'], state['selectedGhosts'], screen, 15, state['current_maze'])
            state['foodGoal'].create(screen)
            if (pacman.y, pacman.x) == state['goal']:
                goals.remove(state['goal'])
                state['goalFound'] = False
                state['pathFound'] = False
                if not goals:
                    set_status(state, f"Beaten in {state['steps']} steps!")
                    state['Minimax'] = state['ABPruning'] = state['Expectimax'] = state['Go'] = False
            elif (pacman.y, pacman.x) in goals:
                goals.remove((pacman.y, pacman.x))

    if state['current_maze'] is None:
        return

    # ── Ghost movement ────────────────────────────────────────────────────────
    if state['selectedGhosts'] and state['Go']:
        for ghost in state['selectedGhosts']:
            state['current_maze'] = ghost.update_ghost_costs(state['current_maze'], False)
            if ghost.type == "tracker":
                state['current_maze'] = ghost.a_star(state['current_maze'], (pacman.y, pacman.x), screen)
            elif ghost.type == "random":
                state['current_maze'] = ghost.random_move(screen, state['current_maze'])
        if state['current_maze'] is None:
            state['current_tile_size'], state['current_maze'] = maze_sizes[state['current_size']]
        state['current_maze'] = ghost.update_ghost_costs(state['current_maze'], True)

    time.sleep(state['speed'])


def handle_manual_movement(state):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        state['pacman'].move("up",    state['current_maze'], state['screen'])
    elif keys[pygame.K_DOWN]:
        state['pacman'].move("down",  state['current_maze'], state['screen'])
    elif keys[pygame.K_LEFT]:
        state['pacman'].move("left",  state['current_maze'], state['screen'])
    elif keys[pygame.K_RIGHT]:
        state['pacman'].move("right", state['current_maze'], state['screen'])
    else:
        state['pacman'].moving = False


# ── Main loop ─────────────────────────────────────────────────────────────────

def main():
    pygame.display.set_caption("Pac-Man AI Search Algorithm Simulator")
    screen = pygame.display.set_mode((window_width, window_height))
    state  = init_state(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state['current_state'] == "MainMenu":
                handle_main_menu_event(event, state)
            elif state['current_state'] == "Customise":
                handle_customise_event(event, state)
            elif state['current_state'] == "Simulation":
                handle_simulation_event(event, state)

        if state['current_state'] == "MainMenu":
            draw_main_menu(state['screen'])
        elif state['current_state'] == "Customise":
            draw_customise(state['screen'], state)
        elif state['current_state'] == "Simulation":
            setup_simulation(state)
            run_simulation_step(state)
            handle_manual_movement(state)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
