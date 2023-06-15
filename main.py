import pygame
import random
import math

class Smoke:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 0)

    def move(self):
        # Choose a random direction to move in.
        direction = random.randint(0, 3)

        # Move in the chosen direction.
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x += 1
        else:
            self.y -= 1

class VentilationSystem:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = (width // 2) if width > 0 else 0

    def spread(self, smoke_particles):
        # Calculate the distance between the smoke and the ventilation system.
        distance = math.sqrt((self.x - smoke_particles[i].x) ** 2 + (self.y - smoke_particles[i].y) ** 2)

        # If the distance is less than the radius of the ventilation system, then the smoke will be sucked in.
        for i in range(len(smoke_particles)):
            if distance[i] < self.radius:
                smoke_particles[i].x = self.x
                smoke_particles[i].y = self.y

def main():
    # Initialize pygame.
    pygame.init()

    # Create a window to display the simulation.
    screen = pygame.display.set_mode((500, 500))

    # Create a grid to represent the floor.
    grid = [[0 for i in range(10)] for j in range(10)]

    # Create a number of smoke particles.
    smoke_particles = []
    for i in range(10):
        smoke_particles.append(Smoke(random.randint(0, 9), random.randint(0, 9), 10))

    # Create a ventilation system.
    ventilation_system = VentilationSystem(250, 250, 100, 100)

    # Create a GUI.
    main_window = pygame.display.set_mode((500, 500))

    # Create a button to add a window.
    add_window_button = pygame.Rect(100, 100, 100, 50)

    # Create a button to add a vent.
    add_vent_button = pygame.Rect(200, 100, 100, 50)

    running = True
    while running:
        # Update the GUI.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and add_window_button.collidepoint(event.pos):
                # Add a window to the room.
                x = random.randint(0, 499)
                y = random.randint(0, 499)
                grid[x][y] = 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and add_vent_button.collidepoint(event.pos):
                # Add a vent to the room.
                x = random.randint(0, 499)
                y = random.randint(0, 499)
                ventilation_system.x = x
                ventilation_system.y = y

        # Update the smoke particles.
        for smoke_particle in smoke_particles:
            smoke_particle.move()

            import pygame
import random
import math

class Smoke:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 0)

    def move(self):
        # Choose a random direction to move in.
        direction = random.randint(0, 3)

        # Move in the chosen direction.
        if direction == 0:
            self.x -= 1
        elif direction == 1:
            self.y += 1
        elif direction == 2:
            self.x += 1
        else:
            self.y -= 1

class VentilationSystem:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = (width // 2) if width > 0 else 0

    def spread(self, smoke_particles):
        # Calculate the distance between the smoke and the ventilation system.
        distance = math.sqrt((self.x - smoke_particles[i].x) ** 2 + (self.y - smoke_particles[i].y) ** 2)

        # If the distance is less than the radius of the ventilation system, then the smoke will be sucked in.
        for i in range(len(smoke_particles)):
            if distance[i] < self.radius:
                smoke_particles[i].x = self.x
                smoke_particles[i].y = self.y

def main():
    # Initialize pygame.
    pygame.init()

    # Create a window to display the simulation.
    screen = pygame.display.set_mode((500, 500))

    # Create a grid to represent the floor.
    grid = [[0 for i in range(10)] for j in range(10)]

    # Create a number of smoke particles.
    smoke_particles = []
    for i in range(10):
        smoke_particles.append(Smoke(random.randint(0, 9), random.randint(0, 9), 10))

    # Create a ventilation system.
    ventilation_system = VentilationSystem(250, 250, 100, 100)

    # Create a GUI.
    main_window = pygame.display.set_mode((500, 500))

    # Create a button to add a window.
    add_window_button = pygame.Rect(100, 100, 100, 50)

    # Create a button to add a vent.
    add_vent_button = pygame.Rect(200, 100, 100, 50)

    running = True
    while running:
        # Update the GUI.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and add_window_button.collidepoint(event.pos):
                # Add a window to the room.
                x = random.randint(0, 499)
                y = random.randint(0, 499)
                grid[x][y] = 1

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and add_vent_button.collidepoint(event.pos):
                # Add a vent to the room.
                x = random.randint(0, 499)
                y = random.randint(0, 499)
                ventilation_system.x = x
                ventilation_system.y = y

        # Update the smoke particles.
        for smoke_particle in smoke_particles:
            smoke_particle.move()