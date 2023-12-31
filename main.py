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

# Particle count font
particle_font = pygame.font.Font(None, 24)

def create_particle():
    """Create a new smoke particle."""
    x = random.uniform(room_x, room_x + room_width)
    y = random.uniform(room_y, room_y + room_height)
    particle = pygame.Rect(x, y, 4, 4)

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

def update_particle_count():
    """Update the particle count based on the number of windows and vents."""
    global num_particles

    reduction_factor = 1.0

    # Calculate reduction factor based on the number of windows
    for _ in windows:
        reduction_factor *= 0.8  # Reduce particle count by 20% for each window

    # Calculate reduction factor based on the number of vents
    for _ in vents:
        reduction_factor *= 0.5  # Reduce particle count by 50% for each vent

    # Calculate the final particle count
    num_particles = max(int(num_particles * reduction_factor), 0)

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
add_particle_button_rect = pygame.Rect(260, 20, 160, 40)

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
                update_particle_count()
            elif remove_window_button_rect.collidepoint(mouse_pos):
                remove_window()
                update_particle_count()
            elif add_vent_button_rect.collidepoint(mouse_pos):
                add_vent()
                update_particle_count()
            elif remove_vent_button_rect.collidepoint(mouse_pos):
                remove_vent()
                update_particle_count()
            elif add_particle_button_rect.collidepoint(mouse_pos):
                particles.append(create_particle())
                num_particles += 1
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == slider:
                    simulation_speed = event.value

        gui_manager.process_events(event)

    # Update
    if running:
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

    # Add Particle Button
    add_particle_button = pygame_gui.elements.UIButton(
        relative_rect=add_particle_button_rect,
        text="Add Particle",  # Button notation: Add a particle to the room
        manager=gui_manager
    )

    particle_count_text = particle_font.render(
        f"Particle Count: {num_particles}", True, SMOKE_COLOR
    )
    window.blit(particle_count_text, (260, 80))

    # Update GUI manager
    gui_manager.update(FPS / 1000)

    # Draw GUI elements
    gui_manager.draw_ui(window)

    pygame.display.update()
    clock.tick(FPS)