import pygame
import startScreen
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1500, 800])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


# Done! Time to quit.
pygame.quit()
