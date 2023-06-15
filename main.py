import pygame
import numpy as np

class SmokeParticle:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

class SmokeSimulation:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.smoke_particles = []
        self.vents = []
        self.windows = []

    def add_smoke_particle(self, x, y, vx, vy):
        self.smoke_particles.append(SmokeParticle(x, y, vx, vy))

    def add_vent(self, x, y):
        self.vents.append((x, y))

    def add_window(self, x, y):
        self.windows.append((x, y))

    def update(self):
        for smoke_particle in self.smoke_particles:
            if smoke_particle.x < 0 or smoke_particle.x >= self.width:
                continue
            if smoke_particle.y < 0 or smoke_particle.y >= self.height:
                continue
            for vent in self.vents:
                if smoke_particle.x == vent[0] and smoke_particle.y == vent[1]:
                    smoke_particle.vx = 0
                    smoke_particle.vy = 0
            for window in self.windows:
                if smoke_particle.x == window[0] and smoke_particle.y == window[1]:
                    smoke_particle.vx = 0
                    smoke_particle.vy = 0
            smoke_particle.update()

    def draw(self, screen):
        for smoke_particle in self.smoke_particles:
            screen.set_at((smoke_particle.x, smoke_particle.y), (0, 0, 0, 1))

def main():
    # Initialize pygame
    pygame.init()

    # Create a pygame window
    screen = pygame.display.set_mode((640, 480))

    # Create a smoke simulation
    simulation = SmokeSimulation(640, 480)

    # Run the simulation until the user quits
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            # Quit if the user closes the window
            if event.type == pygame.QUIT:
                running = False

            # Add a smoke particle if the user clicks the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                simulation.add_smoke_particle(x, y, np.random.randint(-1, 2), np.random.randint(-1, 2))

            # Add a vent if the user presses the `v` key
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                x, y = pygame.mouse.get_pos()
                simulation.add_vent(x, y)

            # Add a window if the user presses the `w` key
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                x, y = pygame.mouse.get_pos()
                simulation.add_window(x, y)

        # Update the simulation
        simulation.update()

        # Draw the simulation
        simulation.draw(screen)

        # Flip the display
        pygame.display.flip()

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()
