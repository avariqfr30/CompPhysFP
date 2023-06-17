import pygame
import random
import pygame_gui
import sys
import math

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ROOM_COLOR = (220, 220, 220)
SMOKE_COLOR = (0, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fire Smoke Simulation")
clock = pygame.time.Clock()

# Room dimensions and features
room_width = 600
room_height = 400
room_x = (WINDOW_WIDTH - room_width) // 2
room_y = (WINDOW_HEIGHT - room_height) // 2
room_rect = pygame.Rect(room_x, room_y, room_width, room_height)
windows = []
vents = []

# Smoke particles
particles = []
num_particles = 100

# GUI manager
gui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

# Simulation state
running = False
simulation_speed = 1.0

def create_particle():
    """Create a new smoke particle."""
    x = random.uniform(room_x, room_x + room_width)
    y = random.uniform(room_y, room_y + room_height)
    particle = pygame.Rect(x, y, 4, 4)

    # Adjust particle position to avoid windows and vents
    for window_rect in windows:
        if particle.colliderect(window_rect):
            # Calculate the direction away from the window
            dx = particle.x - (window_rect.x + window_rect.width / 2)
            dy = particle.y - (window_rect.y + window_rect.height / 2)
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > 0:
                dx /= distance
                dy /= distance

            # Move the particle away from the window
            particle.x += dx * 20
            particle.y += dy * 20
            break

    for vent_rect in vents:
        if particle.colliderect(vent_rect):
            # Calculate the direction towards the vent
            dx = (vent_rect.x + vent_rect.width / 2) - particle.x
            dy = (vent_rect.y + vent_rect.height / 2) - particle.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance > 0:
                dx /= distance
                dy /= distance

            # Move the particle towards the vent
            particle.x += dx * 20
            particle.y += dy * 20
            break

    return particle

def draw_room():
    """Draw the room and its features."""
    pygame.draw.rect(window, ROOM_COLOR, room_rect)

    for window_rect in windows:
        pygame.draw.rect(window, WHITE, window_rect)
        # Highlight the area affected by the window
        pygame.draw.rect(window, (255, 255, 255, 100), room_rect.clip(window_rect))

    for vent_rect in vents:
        pygame.draw.rect(window, GREEN, vent_rect)
        # Highlight the area affected by the vent
        pygame.draw.rect(window, (0, 255, 0, 100), room_rect.clip(vent_rect))

def draw_particles():
    """Draw the smoke particles."""
    for particle in particles:
        pygame.draw.rect(window, SMOKE_COLOR, particle)

def update_particles():
    """Update the smoke particles' positions based on the simulation speed."""
    for particle in particles:
        particle.x += random.uniform(-0.5, 0.5) * simulation_speed * 0.1
        particle.y += random.uniform(-0.5, 0.5) * simulation_speed * 0.1

def add_window():
    """Add a window to the room."""
    window_x = random.uniform(room_x + 20, room_x + room_width - 20)
    window_y = random.choice([room_y, room_y + room_height - 20])
    window_rect = pygame.Rect(window_x, window_y, 20, 20)
    windows.append(window_rect)

def remove_window():
    """Remove a window from the room."""
    if windows:
        windows.pop()

def add_vent():
    """Add a vent to the room."""
    vent_x = random.uniform(room_x + 20, room_x + room_width - 20)
    vent_y = random.uniform(room_y + 20, room_y + room_height - 20)
    vent_rect = pygame.Rect(vent_x, vent_y, 20, 20)
    vents.append(vent_rect)

def remove_vent():
    """Remove a vent from the room."""
    if vents:
        vents.pop()

# Create a slider to control simulation speed
slider_width = 200
slider_height = 20
slider_x = 20
slider_y = 200
slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
slider_range = (0.1, 5.0)
slider_value = 1.0
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=slider_rect,
    start_value=slider_value,
    value_range=slider_range,
    manager=gui_manager
)

# Create GUI buttons and their rectangles
start_button_rect = pygame.Rect(20, 20, 100, 40)
stop_button_rect = pygame.Rect(140, 20, 100, 40)
add_window_button_rect = pygame.Rect(20, 80, 100, 40)
remove_window_button_rect = pygame.Rect(140, 80, 100, 40)
add_vent_button_rect = pygame.Rect(20, 140, 100, 40)
remove_vent_button_rect = pygame.Rect(140, 140, 100, 40)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                running = True
            elif stop_button_rect.collidepoint(mouse_pos):
                running = False
            elif add_window_button_rect.collidepoint(mouse_pos):
                add_window()
            elif remove_window_button_rect.collidepoint(mouse_pos):
                remove_window()
            elif add_vent_button_rect.collidepoint(mouse_pos):
                add_vent()
            elif remove_vent_button_rect.collidepoint(mouse_pos):
                remove_vent()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider:
                    simulation_speed = event.value
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider:
                    # Update simulation speed based on the slider value
                    simulation_speed = event.value

        gui_manager.process_events(event)

    # Update
    if running:
        # Update particles' positions based on the simulation speed
        for _ in range(int(simulation_speed)):
            particles = [create_particle() for _ in range(num_particles)]
            update_particles()

    # Draw
    window.fill(WHITE)
    draw_room()
    draw_particles()

    # Create buttons with notations

    # Start Button
    start_button = pygame_gui.elements.UIButton(
        relative_rect=start_button_rect,
        text="Start",  # Button notation: Start the simulation
        manager=gui_manager
    )

    # Stop Button
    stop_button = pygame_gui.elements.UIButton(
        relative_rect=stop_button_rect,
        text="Stop",  # Button notation: Stop the simulation
        manager=gui_manager
    )

    # Add Window Button
    add_window_button = pygame_gui.elements.UIButton(
        relative_rect=add_window_button_rect,
        text="Add Window",  # Button notation: Add a window to the room
        manager=gui_manager
)

    # Remove Window Button
    remove_window_button = pygame_gui.elements.UIButton(
        relative_rect=remove_window_button_rect,
        text="Remove Window",  # Button notation: Remove a window from the room
        manager=gui_manager
)

    # Add Vent Button
    add_vent_button = pygame_gui.elements.UIButton(
        relative_rect=add_vent_button_rect,
        text="Add Vent",  # Button notation: Add a vent to the room
        manager=gui_manager
    )

    # Remove Vent Button
    remove_vent_button = pygame_gui.elements.UIButton(
        relative_rect=remove_vent_button_rect,
        text="Remove Vent",  # Button notation: Remove a vent from the room
        manager=gui_manager
    )

    # Update GUI manager
    gui_manager.update(FPS)

    # Draw GUI elements
    gui_manager.draw_ui(window)

    # Display
    pygame.display.flip()
    clock.tick(FPS)