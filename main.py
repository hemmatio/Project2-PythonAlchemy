import sys
from typing import Optional

import pygame
import recipeloader
import random
from button import Button, ButtonStay


class Element():
    def __init__(self, x, y, width, height, text, font, text_color, rectangle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text.title()
        self.font = font
        self.text_surface = self.render_with_outline(text, font, text_color, pygame.Color('black'), 1)
        self.rectangle_color = rectangle_color
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rect, 2)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def move_ip(self, dx, dy):
        # Move the element based on deltas
        self.rect.move_ip(dx, dy)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def render_with_outline(self, text, font, text_color, outline_color, outline_width):
        base = font.render(text, True, text_color)
        # The size of the outline surface should be larger than the base by twice the outline width on all sides
        outline_size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
        outline = pygame.Surface(outline_size, pygame.SRCALPHA)

        # Get the positions to blit the base text onto the outline surface, centered
        base_pos = (outline_width, outline_width)

        # Render the outline by drawing the text in the outline color offset in all directions
        offsets = [(-outline_width, -outline_width), (-outline_width, outline_width),
                   (outline_width, -outline_width), (outline_width, outline_width)]
        for dx, dy in offsets:
            temp_surf = font.render(text, True, outline_color)
            outline.blit(temp_surf, (base_pos[0] + dx, base_pos[1] + dy))

        # Blit the base text onto the outline surface
        outline.blit(base, base_pos)
        return outline

pygame.init()

screen_width, screen_height = 1200, 700
Screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

BackGround = pygame.image.load("assets/background.png")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play(chemistry: bool):
    """
     This displays the main game for the classic mode of little alchemy.
     There are two text boxes to combine elements. The user types in the two
     elements they wish to combine, and the backend determines if its a valid combination.
     There will be a bar on the side containing the name of all of the elements found so far.
     """
    if not chemistry:
        with open('recipes.json') as file:
            g = recipeloader.Graph(file)
    else:
        with open('chemistry.json') as file:
            g = recipeloader.Graph(file)

    pygame.display.set_caption("Python Alchemy")

    # Colors and Font
    background_color = pygame.Color('#f7f6f1')
    text_color = pygame.Color("#bc259d")
    font = pygame.font.Font("assets/Roboto-Regular.ttf", 24)
    item_color = pygame.Color(0)

    #initializing the sidebar
    sidebar_width = 250
    sidebar = pygame.Rect(screen_width - sidebar_width, 0, sidebar_width, screen_height)

    # initializing the trash bin
    trash_bin_icon = pygame.image.load("assets/trash.png")  # Load the trash bin icon
    trash_bin_rect = trash_bin_icon.get_rect(
        topleft=(10, screen_height - trash_bin_icon.get_height() - 10))  # Position it at the bottom left

    # initilazing the logo
    logo_icon = pygame.image.load("assets/Logo.png")
    logo_rect = logo_icon.get_rect(
        topleft=(5, 2))

    # initilzazing the arrows
    up_icon = pygame.image.load("assets/up.png")
    up_rect = up_icon.get_rect(topleft=(screen_width - 134, 8))
    down_icon = pygame.image.load("assets/down.png")
    down_rect = down_icon.get_rect(topleft=(screen_width - 134, screen_height - 67))

    # initializing the sounds
    combine_sound1 = pygame.mixer.Sound("assets/combine1.wav")
    combine_sound2 = pygame.mixer.Sound("assets/combine2.wav")
    combine_sound3 = pygame.mixer.Sound("assets/combine3.wav")
    combine_sounds = [combine_sound1, combine_sound2, combine_sound3]
    click_sound = pygame.mixer.Sound("assets/click.wav")

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

        # drawing logo
        Screen.blit(logo_icon, logo_rect)

        # adding elements to sidebar and the little circles
        j = 0
        discovered = []
        for i, value in enumerate(g.discovered[k:(k + 10)], start=k + 1):  # Enumerate with start=k
            # Create text surface for index
            font2 = pygame.font.Font("assets/Roboto-Regular.ttf", 22)
            index_text = font2.render(str(i), True, pygame.Color(0))

            # Adjust position if the index is double-digit
            index_x = screen_width - 225 if i < 10 else screen_width - 232
            index_y = 50 + j
            pygame.draw.circle(Screen, (150, 150, 150, 50), (screen_width - 219, index_y + 14), 17)

            # Position index text beside the element
            index_rect = index_text.get_rect(topleft=(index_x, index_y))
            Screen.blit(index_text, index_rect)

            # Create and draw element
            element = Element(screen_width - 190, 40 + j, 140, 45, value.item.title(), font, text_color, item_color)
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
                    if k + 10 < len(g.discovered):
                        k = k + 1
                        pygame.mixer.Sound.play(click_sound)
                if event.key == pygame.K_UP:
                    if k - 1 >= 0:
                        k = k - 1
                        pygame.mixer.Sound.play(click_sound)

            # spawns the element in the middle of the screen or drags element
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # spawns in middle
                stock_index = None
                for discover in discovered:
                    if discover.is_clicked(event.pos):
                        pygame.mixer.Sound.play(click_sound)
                        elements.append(Element(400 + random.randint(-100, 100), 300 + random.randint(-100, 100), 140, 45, discover.text.title(), font, text_color, item_color))

                # drags the item
                for num, element in enumerate(elements):
                    if element.is_clicked(event.pos):
                        stock_index = num
                        holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                holding = False
            if event.type == pygame.MOUSEMOTION:
                if holding:
                    if len(elements) > 0:
                        elements[stock_index].move_ip(*event.rel)
                        letgo = 1

            # trash bin and arrow function and back to main menu
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if trash_bin_rect.collidepoint(event.pos):  # Check if the trash bin is clicked
                    pygame.mixer.Sound.play(click_sound)
                    elements = []
                    stock_index = None
                if up_rect.collidepoint(event.pos):
                    if k - 1 >= 0:
                        pygame.mixer.Sound.play(click_sound)
                        k = k - 1
                if down_rect.collidepoint(event.pos):
                    if k + 10 < len(g.discovered):
                        pygame.mixer.Sound.play(click_sound)
                        k = k + 1

                if logo_rect.collidepoint(event.pos):
                    if elements:
                        for element in elements:
                            if not logo_rect.colliderect(element.rect):
                                pygame.mixer.Sound.play(click_sound)
                                main_menu(chemistry)
                    else:
                        pygame.mixer.Sound.play(click_sound)
                        main_menu(chemistry)

            # Combine items if not holding
            if not holding and letgo == 1:
                for element in elements:
                    if (stock_index and
                            element != elements[stock_index] and pygame.Rect.colliderect(elements[stock_index].rect, element.rect)):
                        valid_combo, item_created = g.combine(element.text.lower(), elements[stock_index].text.lower())
                        if valid_combo:
                            x, y = pygame.mouse.get_pos()
                            elements.append(Element(x - 70, y - 25, 140,  45, item_created, font, text_color, item_color))
                            elements.remove(elements[stock_index])
                            elements.remove(element)
                            letgo = 0
                            pygame.mixer.Sound.play(combine_sounds[random.randint(0, 2)])
                            break

        # Draw the trash bin
        Screen.blit(trash_bin_icon, trash_bin_rect)

        # Draws the little arrows when you can go up and down
        if k - 1 >= 0:
            Screen.blit(up_icon, up_rect)
        if k + 10 < len(g.discovered):
            Screen.blit(down_icon, down_rect)


        pygame.display.flip()
def options(chemistry: bool):
    click_sound = pygame.mixer.Sound("assets/click.wav")
    chemupdate = chemistry
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        Screen.fill("white")

        options_text = get_font(45).render("Options", True, "Black")
        options_rect = options_text.get_rect(center=(screen_width // 2 + 15, 35))
        Screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(screen_width - 100, screen_height - 40),
                              text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Green")
        options_back.changeColor(options_mouse_pos)
        options_back.update(Screen)

        # Chemistry buttons
        chemtext = get_font(40).render("Chemistry Mode:", True, "Black")
        chemrect = options_text.get_rect(center=(190, 170))
        Screen.blit(chemtext, chemrect)

        if chemupdate:
            chembutton = ButtonStay(image=None, pos=(screen_width - 100, 170),
                                    text_input="ON", font=get_font(40), base_color="Black", hovering_color="White", clicked=True)
        else:
            chembutton = ButtonStay(image=None, pos=(screen_width - 100, 170),
                                    text_input="OFF", font=get_font(40), base_color="Black", hovering_color="White", clicked=False)
        chembutton.changeColor(options_mouse_pos)
        chembutton.update(Screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    main_menu(chemupdate)
                if chembutton.checkForInput(options_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    if chembutton.clicked:
                        chembutton.clicked = False
                        chemupdate = False
                    else:
                        chembutton.clicked = True
                        chemupdate = True

        pygame.display.update()

def main_menu(chemistry: bool):
    """
    This displays the start screen. This will include a title, start button,
    game mode, and quit button.
    """
    click_sound = pygame.mixer.Sound("assets/click.wav")
    pygame.display.set_caption("Menu")
    while True:
        Screen.blit(BackGround, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(74).render("Python Alchemy", True, "#12CDEC")
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
                    pygame.mixer.Sound.play(click_sound)
                    play(chemistry)
                if options_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    options(chemistry)
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.Sound.play(click_sound)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


# g.combine("water", "earth")
# g.combine("air", "water")
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

main_menu(False)
