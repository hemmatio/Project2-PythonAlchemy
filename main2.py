import pygame
import recipeloader
from button import Button
class Element():
    def __init__(self, x, y, width, height, text, font, text_color, rectangle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_surface = font.render(text, True, text_color)
        self.rectangle_color = rectangle_color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def move_ip(self, dx, dy):
        # Move the element based on deltas
        self.rect.move_ip(dx, dy)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

pygame.init()

screen_width, screen_height = 1200, 700
Screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    """
     This displays the main game for the classic mode of little alchemy.
     There are two text boxes to combine elements. The user types in the two
     elements they wish to combine, and the backend determines if its a valid combination.
     There will be a bar on the side containing the name of all of the elements found so far.
     """
    #bla
    pygame.display.set_caption("Little Alchemist")

    # Colors and Font
    background_color = pygame.Color("#f7f6f2")
    text_color = pygame.Color('white')
    font = pygame.font.Font(None, 32)
