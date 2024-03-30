import sys

import pygame
import recipeloader
import random
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

BackGround = pygame.image.load("singed.jpeg")

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
    background_color = pygame.Color('#f7f6f1')
    text_color = pygame.Color('white')
    font = pygame.font.Font(None, 32)
    item_color = pygame.Color("blue")

    #initializing the sidebar
    sidebar_width = 250
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)

    # initializing the trash bin
    trash_bin_icon = pygame.image.load("trash.png")  # Load the trash bin icon
    trash_bin_rect = trash_bin_icon.get_rect(
        topleft=(10, screen_height - trash_bin_icon.get_height() - 10))  # Position it at the bottom left

    # initializing elementary elements
    elements = []
    k = 0
    holding = False
    letgo = 0
    stock_index = 0


    while True:
        Screen.fill(background_color)



        # drawing sidebar
        pygame.draw.rect(Screen, pygame.Color("#efebe0"), sidebar)

        # adding elements to sidebar
        j = 0
        discovered = []
        for value in recipeloader.g.discovered[k:(k + 10)]:
            element = Element(screen_width - 185, 40 + j, 140, 50, value.item, font, text_color, item_color)
            discovered.append(element)
            element.draw(Screen)
            j += 60
        #prints all elements on the screen
        for element in elements:
            element.draw(Screen)

        for event in pygame.event.get():

            # adding scroll when down arrow is clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if k + 10 < len(recipeloader.g.discovered):
                        k = k + 1
                if event.key == pygame.K_UP:
                    if k - 1 >= 0:
                        k = k - 1

            # spawns the element in the middle of the screen or drags element
            if event.type == pygame.MOUSEBUTTONDOWN:
                # spawns in middle
                stock_index = None
                for discover in discovered:
                    if discover.is_clicked(event.pos):
                        elements.append(Element(400 + random.randint(-100, 100), 300 + random.randint(-100, 100), 140, 50, discover.text, font, text_color, item_color))

                # drags the item
                for num, element in enumerate(elements):
                    if element.is_clicked(event.pos):
                        stock_index = num
                        holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                holding = False
            if event.type == pygame.MOUSEMOTION:
                if holding:
                    elements[stock_index].move_ip(*event.rel)
                    letgo = 1

            #trash bin function
            if event.type == pygame.MOUSEBUTTONDOWN:
                if trash_bin_rect.collidepoint(event.pos):  # Check if the trash bin is clicked
                    elements = []


            # Combine items if not holding
            if not holding and letgo == 1:
                for element in elements:
                    if (stock_index and
                            element != elements[stock_index] and pygame.Rect.colliderect(elements[stock_index].rect, element.rect)):
                        valid_combo, item_created = recipeloader.g.combine(element.text, elements[stock_index].text)
                        if valid_combo:
                            x, y = pygame.mouse.get_pos()
                            elements.append(Element(x - 70, y - 25, 140,  50, item_created, font, text_color, pygame.Color("blue")))
                            elements.remove(elements[stock_index])
                            elements.remove(element)
                            letgo = 0
                            break

        Screen.blit(trash_bin_icon, trash_bin_rect)  # Draw the trash bin icon


        pygame.display.flip()
    pygame.quit()
def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        Screen.fill("white")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        Screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_back.changeColor(options_mouse_pos)
        options_back.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    """
    This displays the start screen. This will include a title, start button,
    game mode, and quit button.
    """
    pygame.display.set_caption("Menu")

    while True:
        Screen.blit(BackGround, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640,100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY",font = get_font(75), base_color = "#d7fcd4", hovering_color = "White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                             text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        Screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


# recipeloader.g.combine("water", "earth")
# recipeloader.g.combine("air", "water")
# recipeloader.g.combine("fire","water")
# recipeloader.g.combine("earth","fire")
# recipeloader.g.combine("rain","rain")
# recipeloader.g.combine("rain","earth")
# recipeloader.g.combine("fire","mud")
# recipeloader.g.combine("brick","brick")
# recipeloader.g.combine("wall","wall")
# recipeloader.g.combine("house","house")
# recipeloader.g.combine("earth","air")
# recipeloader.g.combine("lava","water")
# recipeloader.g.combine("lava","air")
# recipeloader.g.combine("lava","earth")

main_menu()
