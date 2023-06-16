import pygame
import sys

def init():
    pygame.init()
    pygame.font.init()

class SmokeSimulation:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Create a list of smoke particles
        self.smoke_particles = []

        # Create a list of vents
        self.vents = []

        # Create a list of windows
        self.windows = []

    def add_vent(self, x, y):
        self.vents.append((x, y))

    def add_window(self, x, y):
        self.windows.append((x, y))

    def update(self):
        # Update the position of the smoke particles
        for smoke_particle in self.smoke_particles:
            smoke_particle.x += smoke_particle.velocity[0]
            smoke_particle.y += smoke_particle.velocity[1]

            # Check for collisions with vents
            for vent in self.vents:
                if smoke_particle.x == vent[0] and smoke_particle.y == vent[1]:
                    smoke_particle.velocity[0] = -smoke_particle.velocity[0]
                    smoke_particle.velocity[1] = -smoke_particle.velocity[1]

            # Check for collisions with windows
            for window in self.windows:
                if smoke_particle.x >= window[0] and smoke_particle.x <= window[0] + window[2] and smoke_particle.y >= window[1] and smoke_particle.y <= window[1] + window[3]:
                    smoke_particle.velocity[0] = -smoke_particle.velocity[0]
                    smoke_particle.velocity[1] = -smoke_particle.velocity[1]

    def draw(self, window):
        # Draw the smoke particles
        for smoke_particle in self.smoke_particles:
            window.set_at((smoke_particle.x, smoke_particle.y), (0, 0, 0, 1))

        # Draw the vents
        for vent in self.vents:
            pygame.draw.circle(window, (0, 0, 255), vent, 5)

        # Draw the windows
        for window in self.windows:
            pygame.draw.rect(window, (255, 0, 0), window)


class SmokeSimulationGUI:

    def __init__(self, simulation):
        self.simulation = simulation

        # Create a window
        self.window = pygame.display.set_mode((640, 480))

        # Create a label to display the simulation's status
        self.status_label = pygame.Surface((640, 20))
        self.status_label.fill((255, 255, 255))
        self.status_label.set_alpha(128)
        self.status_label.blit(pygame.font.SysFont("Arial", 16).render("Simulation Status:", True, (0, 0, 0)), (0, 0))

        # Create a button to add a vent
        self.add_vent_button = pygame.Surface((100, 20))
        self.add_vent_button.fill((0, 0, 255))
        self.add_vent_button.set_alpha(128)
        self.add_vent_button.blit(pygame.font.SysFont("Arial", 16).render("Add Vent", True, (255, 255, 255)), (0,0))

        # Create a button to add a window
        self.add_window_button = pygame.Surface((100, 20))
        self.add_window_button.fill((255, 0, 0))
        self.add_window_button.set_alpha(128)
        self.add_window_button.blit(pygame.font.SysFont("Arial", 16).render("Add Window", True, (255, 255, 255)), (0, 0))

    # Handle events
    def handle_event(self, event):
        # Quit if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Add a vent if the user clicks on the "Add Vent" button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.add_vent_button.collidepoint(event.pos):
            self.simulation.add_vent(event.pos[0], event.pos[1])

        # Add a window if the user clicks on the "Add Window" button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.add_window_button.collidepoint(event.pos):
            self.simulation.add_window(event.pos[0], event.pos[1])

    def update(self):
        self.simulation.update()

    def draw(self):
        # Draw the simulation
        self.simulation.draw(self.window)

        # Draw the label and buttons
        self.window.blit(self.status_label, (0, 0))
        self.window.blit(self.add_vent_button, (0, 20))
        self.window.blit(self.add_window_button, (100, 20))

        # Flip the display
        pygame.display.flip()


if __name__ == "__main__":
    # Create a simulation
    simulation = SmokeSimulation(640, 480)

    # Create a GUI
    gui = SmokeSimulationGUI(simulation)

    # Run the GUI
    while True:
        # Handle events
        gui.handle_event(pygame.event.wait())

        # Update the simulation
        gui.update()

        # Draw the simulation
        gui.draw()